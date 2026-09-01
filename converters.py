import io
import json
from typing import Any, Callable

import pandas as pd


def parse_csv(buffer: io.BytesIO) -> pd.DataFrame:
    try:
        return pd.read_csv(buffer, encoding="utf-8-sig")
    except (
        UnicodeDecodeError,
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
    ) as error:
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
        raise ValueError(
            "O arquivo JSON é inválido ou possui uma codificação incompatível."
        ) from error

    if isinstance(data, list):
        if not all(isinstance(item, dict) for item in data):
            raise ValueError("A lista JSON deve conter apenas objetos.")

        return pd.json_normalize(data)

    if isinstance(data, dict):
        return pd.json_normalize([data])

    raise ValueError("O JSON deve conter um objeto ou uma lista de objetos.")


def parse_xlsx(buffer: io.BytesIO) -> pd.DataFrame:
    try:
        return pd.read_excel(buffer)
    except Exception as error:
        raise ValueError("Não foi possível ler o arquivo XLSX.") from error


def export_csv(df: pd.DataFrame) -> tuple[io.BytesIO, str]:
    buffer = io.BytesIO()

    df.to_csv(
        buffer,
        index=False,
        encoding="utf-8",
        lineterminator="\n",
    )

    buffer.seek(0)

    return buffer, "text/csv"


def export_json(df: pd.DataFrame) -> tuple[io.BytesIO, str]:
    buffer = io.BytesIO()

    data = df.to_json(
        orient="records",
        force_ascii=False,
        indent=4,
    )

    buffer.write(data.encode("utf-8"))
    buffer.seek(0)

    return buffer, "application/json"


def export_xlsx(df: pd.DataFrame) -> tuple[io.BytesIO, str]:
    buffer = io.BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl",
    ) as writer:
        df.to_excel(
            writer,
            index=False,
        )

    buffer.seek(0)

    return (
        buffer,
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def dict_to_dataframe(data: dict[str, Any]) -> pd.DataFrame:
    if not isinstance(data, dict):
        raise ValueError("A entrada deve ser um dicionário Python.")

    return pd.json_normalize([data])


def export_data_json(
    data: dict[str, Any],
) -> tuple[io.BytesIO, str]:
    buffer = io.BytesIO()

    buffer.write(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=4,
        ).encode("utf-8")
    )

    buffer.seek(0)

    return buffer, "application/json"


def export_data_csv(
    data: dict[str, Any],
) -> tuple[io.BytesIO, str]:
    return export_csv(dict_to_dataframe(data))


def process_data_conversion(
    data: dict[str, Any],
    target_format: str,
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


PARSERS: dict[str, Callable[[io.BytesIO], pd.DataFrame]] = {
    ".csv": parse_csv,
    ".json": parse_json,
    ".xlsx": parse_xlsx,
}


EXPORTERS: dict[str, Callable[[pd.DataFrame], tuple[io.BytesIO, str]]] = {
    "csv": export_csv,
    "json": export_json,
    "xlsx": export_xlsx,
}


def process_file_conversion(
    file_bytes: bytes,
    file_ext: str,
    target_format: str,
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
