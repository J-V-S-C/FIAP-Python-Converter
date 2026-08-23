import io
import json
import pandas as pd
from typing import Callable


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


def parse_json(buffer: io.BytesIO) -> pd.DataFrame:
    try:
        data = json.loads(buffer.getvalue().decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("O arquivo JSON é inválido ou possui uma codificação incompatível.") from error

    if not isinstance(data, (dict, list)):
        raise ValueError("O JSON deve conter um objeto ou uma lista de objetos.")

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


def export_csv(df: pd.DataFrame) -> tuple[io.BytesIO, str]:
    buf = io.BytesIO()
    df.to_csv(buf, index=False, encoding="utf-8")
    buf.seek(0)
    return buf, "text/csv"


def export_json(df: pd.DataFrame) -> tuple[io.BytesIO, str]:
    buf = io.BytesIO()
    buf.write(df.to_json(orient="records", force_ascii=False, indent=4).encode("utf-8"))
    buf.seek(0)
    return buf, "application/json"


def export_txt(df: pd.DataFrame) -> tuple[io.BytesIO, str]:
    buf = io.BytesIO()
    rows = df.fillna("").astype(str).apply("\t".join, axis=1)
    buf.write("\n".join(rows).encode("utf-8"))
    buf.seek(0)
    return buf, "text/plain"


PARSERS: dict[str, Callable[[io.BytesIO], pd.DataFrame]] = {
    ".csv": parse_csv,
    ".json": parse_json,
    ".txt": parse_txt,
}

EXPORTERS: dict[str, Callable[[pd.DataFrame], tuple[io.BytesIO, str]]] = {
    "csv": export_csv,
    "json": export_json,
    "txt": export_txt,
}


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
