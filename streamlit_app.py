import json
from pathlib import Path

import streamlit as st

from converters import (
    process_data_conversion,
    process_file_conversion,
)


st.set_page_config(
    page_title="Conversor de arquivos",
    layout="centered",
)

st.title("Conversor de Arquivos")
st.caption("Converta seus dados e arquivos entre diferentes formatos.")

st.divider()

st.subheader("Escolha uma conversão")

operacao = st.selectbox(
    "Tipo de conversão",
    [
        "Dict → JSON",
        "Dict → CSV",
        "JSON → CSV",
        "CSV → JSON",
        "XLSX → CSV",
        "CSV → XLSX",
    ],
)

st.divider()


if operacao == "Dict → JSON":
    st.subheader("Python Dict → JSON")

    dados = st.text_area(
        "Digite seu dict",
        placeholder='{"nome": "João", "idade": 20}',
        height=200,
    )

    if st.button(
        "Converter",
        type="primary",
        use_container_width=True,
    ):
        try:
            data = json.loads(dados)

            if not isinstance(data, dict):
                raise ValueError("A entrada deve ser um dict.")

            output, media_type = process_data_conversion(
                data,
                "json",
            )

            st.download_button(
                "Baixar JSON",
                output,
                "resultado.json",
                media_type,
                use_container_width=True,
            )

            st.success("Conversão realizada com sucesso!")

        except (json.JSONDecodeError, ValueError) as error:
            st.error(str(error))


elif operacao == "Dict → CSV":
    st.subheader("Python Dict → CSV")

    dados = st.text_area(
        "Digite seu dict",
        placeholder='{"nome": "João", "idade": 20}',
        height=200,
    )

    if st.button(
        "Converter",
        type="primary",
        use_container_width=True,
    ):
        try:
            data = json.loads(dados)

            if not isinstance(data, dict):
                raise ValueError("A entrada deve ser um dict.")

            output, media_type = process_data_conversion(
                data,
                "csv",
            )

            st.download_button(
                "Baixar CSV",
                output,
                "resultado.csv",
                media_type,
                use_container_width=True,
            )

            st.success("Conversão realizada com sucesso!")

        except (json.JSONDecodeError, ValueError) as error:
            st.error(str(error))


else:
    input_formats = {
        "JSON → CSV": ("json", "csv"),
        "CSV → JSON": ("csv", "json"),
        "XLSX → CSV": ("xlsx", "csv"),
        "CSV → XLSX": ("csv", "xlsx"),
    }

    input_format, output_format = input_formats[operacao]

    st.subheader(operacao)

    arquivo = st.file_uploader(
        f"Envie seu arquivo {input_format.upper()}",
        type=[input_format],
    )

    if st.button(
        "Converter",
        type="primary",
        use_container_width=True,
    ):
        if not arquivo:
            st.warning("Envie um arquivo antes de converter.")
            st.stop()

        try:
            output, media_type = process_file_conversion(
                arquivo.getvalue(),
                Path(arquivo.name).suffix,
                output_format,
            )

            output_filename = f"{Path(arquivo.name).stem}.{output_format}"

            st.download_button(
                f"Baixar {output_format.upper()}",
                output,
                output_filename,
                media_type,
                use_container_width=True,
            )

            st.success("Conversão realizada com sucesso!")

        except ValueError as error:
            st.error(str(error))
