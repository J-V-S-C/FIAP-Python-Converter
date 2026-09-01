import streamlit as st

st.set_page_config(page_title="Conversor de arquivos", layout="centered")

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
        "Digite seu dict", placeholder='{"nome": "João", "idade": 20}', height=200
    )

elif operacao == "Dict → CSV":
    st.subheader("Python Dict → CSV")

    dados = st.text_area(
        "Digite seu dict", placeholder='{"nome": "João", "idade": 20}', height=200
    )

elif operacao == "JSON → CSV":
    st.subheader("JSON → CSV")

    arquivo = st.file_uploader("Envie seu arquivo JSON", type=["json"])

elif operacao == "CSV → JSON":
    st.subheader("CSV → JSON")

    arquivo = st.file_uploader("Envie seu arquivo CSV", type=["csv"])

elif operacao == "XLSX → CSV":
    st.subheader("XLSX → CSV")

    arquivo = st.file_uploader("Envie seu arquivo XLSX", type=["xlsx"])

elif operacao == "CSV → XLSX":
    st.subheader("CSV → XLSX")

    arquivo = st.file_uploader("Envie seu arquivo CSV", type=["csv"])

st.divider()

st.button("Converter", type="primary", use_container_width=True)
