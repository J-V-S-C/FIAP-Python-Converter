import io
import pandas as pd
from typing import Callable


def parse_csv(buffer: io.BytesIO) -> pd.DataFrame:
    return pd.read_csv(buffer)


def parse_json(buffer: io.BytesIO) -> pd.DataFrame:
    return pd.read_json(buffer)


def parse_txt(buffer: io.BytesIO) -> pd.DataFrame:
    lines = [
        line.strip()
        for line in buffer.getvalue().decode("utf-8").splitlines()
        if line.strip()
    ]
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
    buf.write(df.to_string(index=False).encode("utf-8"))
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
    parser = PARSERS.get(file_ext.lower())
    if not parser:
        raise ValueError(f"Extensão de entrada não suportada: {file_ext}")

    exporter = EXPORTERS.get(target_format.lower())
    if not exporter:
        raise ValueError(f"Formato de saída não suportado: {target_format}")

    df = parser(io.BytesIO(file_bytes))
    return exporter(df)
