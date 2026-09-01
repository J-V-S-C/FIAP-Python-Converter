import io
import json
import zipfile
import pandas as pd


# Lê um arquivo CSV e transforma em DataFrame para padronizar o processamento.
def parse_csv(buffer: io.BytesIO) -> pd.DataFrame:
    try:
        return pd.read_csv(buffer, encoding="utf-8-sig")
    except (UnicodeDecodeError, pd.errors.EmptyDataError, pd.errors.ParserError) as error:
        if isinstance(error, UnicodeDecodeError):
            message = "O arquivo CSV possui uma codificação incompatível."
        elif isinstance(error, pd.errors.EmptyDataError):
            message = "O arquivo CSV está vazio."
        else:
            message = "O arquivo CSV possui um formato inválido."
        raise ValueError(message) from error


# Lê um arquivo JSON, valida o conteúdo e normaliza para DataFrame.
def parse_json(buffer: io.BytesIO) -> pd.DataFrame:
    try:
        data = json.loads(buffer.getvalue().decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("O arquivo JSON é inválido ou possui uma codificação incompatível.") from error

    # O JSON de entrada precisa ser um objeto ou uma lista, para manter o fluxo consistente.
    if not isinstance(data, (dict, list)):
        raise ValueError("O JSON deve conter um objeto ou uma lista de objetos.")

    # Caso o JSON venha organizado em uma chave 'usuarios', a lógica trata esse caso específico.
    if isinstance(data, dict) and "usuarios" in data:
        if not isinstance(data["usuarios"], list):
            raise ValueError("O campo 'usuarios' deve ser uma lista.")

        df = pd.json_normalize(
            data["usuarios"]
        )

        if "metadados" in data:
            if not isinstance(data["metadados"], dict):
                raise ValueError("O campo 'metadados' deve ser um objeto.")

            for chave, valor in data["metadados"].items():

                if not isinstance(valor, (dict, list)):
                    df[f"meta_{chave}"] = valor

        return df

    return pd.json_normalize(data)




# Converte texto simples em uma tabela com uma coluna única, mantendo cada linha como um registro.
def parse_txt(buffer: io.BytesIO) -> pd.DataFrame:
    try:
        lines = [
            line.strip()
            for line in buffer.getvalue().decode("utf-8-sig").splitlines()
            if line.strip()
        ]
    except UnicodeDecodeError as error:
        raise ValueError("O arquivo TXT possui uma codificação incompatível.") from error
    return pd.DataFrame({"conteudo": lines})

def parse_xlsx(buffer: io.BytesIO) -> pd.DataFrame:
    try:
        df = pd.read_excel(buffer, engine="openpyxl")
    except ValueError as error:
        raise ValueError("O arquivo XLSX possui um formato inválido.") from error
    except zipfile.BadZipFile as error:
        raise ValueError("O arquivo XLSX está corrompido ou não é um formato .xlsx válido.") from error
    if df.empty:
        raise ValueError("O arquivo XLSX está vazio.")
    return df


# Exporta um DataFrame para CSV em bytes, com linha final padronizada para ambiente Windows/Linux.
def export_csv(df: pd.DataFrame) -> tuple[io.BytesIO, str]:
    buf = io.BytesIO()
    df.to_csv(buf, index=False, encoding="utf-8", lineterminator="\n")
    buf.seek(0)
    return buf, "text/csv"


# Exporta para JSON usando registros em formato orientado por linha.
def export_json(df: pd.DataFrame) -> tuple[io.BytesIO, str]:
    buf = io.BytesIO()
    buf.write(df.to_json(orient="records", force_ascii=False, indent=4).encode("utf-8"))
    buf.seek(0)
    return buf, "application/json"


# Converte um dicionário Python em DataFrame para reaproveitar a mesma lógica de exportação.
def dict_to_dataframe(data: dict[str, Any]) -> pd.DataFrame:
    if not isinstance(data, dict):
        raise ValueError("A entrada deve ser um dicionário Python.")

    if "usuarios" in data:
        if not isinstance(data["usuarios"], list):
            raise ValueError("O campo 'usuarios' deve ser uma lista.")

        df = pd.json_normalize(data["usuarios"])

        if "metadados" in data:
            if not isinstance(data["metadados"], dict):
                raise ValueError("O campo 'metadados' deve ser um objeto.")

            for chave, valor in data["metadados"].items():
                if not isinstance(valor, (dict, list)):
                    df[f"meta_{chave}"] = valor

        return df

    return pd.json_normalize([data])


# Exporta diretamente um dicionário em JSON, preservando a estrutura original.
def export_data_json(data: dict[str, Any]) -> tuple[io.BytesIO, str]:
    buf = io.BytesIO()
    buf.write(json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8"))
    buf.seek(0)
    return buf, "application/json"


# Converte dicionário em CSV usando a conversão intermediária para DataFrame.
def export_data_csv(data: dict[str, Any]) -> tuple[io.BytesIO, str]:
    return export_csv(dict_to_dataframe(data))


# Função pública para converter dicionário Python em outro formato sem depender de arquivo.
def process_data_conversion(
    data: dict[str, Any], target_format: str
) -> tuple[io.BytesIO, str]:
    if not isinstance(data, dict):
        raise ValueError("A entrada deve ser um dicionário Python.")

    target = target_format.lower().strip()
    exporters = {
        "csv": export_data_csv,
        "json": export_data_json,
    }

    exporter = exporters.get(target)
    if not exporter:
        raise ValueError(f"Formato de saída não suportado: {target_format}")

    return exporter(data)


# Exporta um DataFrame em texto simples, usando tabulação entre colunas.
def export_txt(df: pd.DataFrame) -> tuple[io.BytesIO, str]:
    buf = io.BytesIO()
    rows = df.fillna("").astype(str).apply("\t".join, axis=1)
    buf.write("\n".join(rows).encode("utf-8"))
    buf.seek(0)
    return buf, "text/plain"

def export_xlsx(df: pd.DataFrame) -> tuple[io.BytesIO, str]:
    buf = io.BytesIO()
    df.to_excel(buf, index=False, engine="openpyxl")
    buf.seek(0)
    return buf,"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

# Mapeia extensão de arquivo para função de leitura.
PARSERS: dict[str, Callable[[io.BytesIO], pd.DataFrame]] = {
    ".csv": parse_csv,
    ".json": parse_json,
    ".txt": parse_txt,
    ".xlsx": parse_xlsx,
}

# Mapeia formato de destino para função de escrita.
EXPORTERS: dict[str, Callable[[pd.DataFrame], tuple[io.BytesIO, str]]] = {
    "csv": export_csv,
    "json": export_json,
    "txt": export_txt,
    "xlsx": export_xlsx,
}


# Orquestra a leitura do arquivo, validação e exportação para o destino desejado.
def process_file_conversion(
    file_bytes: bytes, file_ext: str, target_format: str
) -> tuple[io.BytesIO, str]:
    if not file_bytes:
        raise ValueError("O arquivo enviado está vazio.")

    parser = PARSERS.get(file_ext.lower().strip())
    if not parser:
        raise ValueError(f"Extensão de entrada não suportada: {file_ext}")

    exporter = EXPORTERS.get(target_format.lower().strip())
    if not exporter:
        raise ValueError(f"Formato de saída não suportado: {target_format}")

    df = parser(io.BytesIO(file_bytes))
    return exporter(df)
