import io
import json
import streamlit as st
import pandas as pd
from converters import (
    parse_csv,
    parse_json,
    export_csv,
    export_json,
    process_data_conversion,
)
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Configuração da página
st.set_page_config(
    page_title="Conversor de Arquivos",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": " Conversor profissional de arquivos - FIAP"
    }
)

# CSS customizado para estilo moderno
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* Cores principais */
        :root {
            --primary-color: #7c3aed;
            --secondary-color: #3b82f6;
            --success-color: #06b6d4;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
        }
        
        /* Forçar background da página com gradiente roxo */
        body, [data-testid="stAppViewContainer"], [data-testid="stRoot"], .main {
            background: linear-gradient(135deg, #f3e8ff 0%, #ddd6fe 100%) !important;
        }
        
        /* Headers */
        h1 {
            color: #7c3aed !important;
            font-weight: 700;
            text-align: center;
            margin-bottom: 10px;
        }
        
        .subtitle {
            text-align: center;
            color: #000000;
            font-size: 1.1em;
            margin-bottom: 30px;
        }
        
        /* Cards */
        .conversion-card {
            
            background: white;
            border-radius: 10px;
            padding: 20px;
            border-left: 5px solid #7c3aed;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .info-box {
            background: #ede9fe;
            border-left: 4px solid #7c3aed;
            padding: 12px;
            border-radius: 6px;
            margin: 10px 0;
        }
        
        .success-box {
            background: #cffafe;
            border-left: 4px solid #06b6d4;
            padding: 12px;
            border-radius: 6px;
            margin: 10px 0;
        }
        
        .error-box {
            background: #fee2e2;
            border-left: 4px solid #ef4444;
            padding: 12px;
            border-radius: 6px;
            margin: 10px 0;
        }
        
        /* Forçar cores de texto preto */
        h3 {
            color: #000000 !important;
        }
        
        p, [data-testid="stMarkdownContainer"] p {
            color: #000000 !important;
        }
        
        [data-testid="stCaption"] {
            color: #000000 !important;
        }
        
        .stCaption {
            color: #000000 !important;
        }
        
        /* Garantir texto preto em labels */
        label {
            color: #000000 !important;
        }
        
        /* Estilo do Footer */
        .footer-container {
            background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
            padding: 30px 20px;
            border-radius: 12px;
            margin-top: 20px;
        }
        
        .footer-container [data-testid="stCaption"] {
            color: #1f1f1f !important;
            font-weight: 600;
        }
        
        .footer-container p {
            color: #1f1f1f !important;
        }
        
        /* Ícones do footer mais escuros */
        .footer-container i {
            color: #2d2d2d !important;
            margin-right: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# Header estilizado
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1> Conversor de Arquivos</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='subtitle'>Converta seus dados e arquivos entre diferentes formatos com facilidade</p>",
        unsafe_allow_html=True
    )

st.divider()

# Mapeamento de operações com emojis
operacoes_emojis = {
    " Dict → JSON": "Dict → JSON",
    " Dict → CSV": "Dict → CSV",
    " JSON → CSV": "JSON → CSV",
    " CSV → JSON": "CSV → JSON",
    " XLSX → CSV": "XLSX → CSV",
    " CSV → XLSX": "CSV → XLSX",
}

# Seletor de conversão com layout melhorado
st.subheader(" Escolha o tipo de conversão")
operacao_display = st.selectbox(
    "Tipo de conversão",
    list(operacoes_emojis.keys()),
    label_visibility="collapsed"
)
operacao = operacoes_emojis[operacao_display]

# Dicas em baixo
col1, col2 = st.columns(2)
with col1:
    st.info("💡 **Dica:** Selecione a conversão desejada acima")
with col2:
    st.info("💡 **Dica:** O peso máximo do upload do arquivo é de 10MB")

st.divider()

# Container principal para conteúdo
input_col, preview_col = st.columns([1.5, 1])

with input_col:
    if operacao == "Dict → JSON":
        st.markdown("###  Python Dict → JSON", unsafe_allow_html=True)
        dados = st.text_area(
            "Digite seu dicionário Python",
            placeholder='{"nome": "João", "idade": 20, "ativo": true}',
            height=250,
            key="dict_input"
        )
        
        if st.button(" Converter para JSON", use_container_width=True, type="primary"):
            try:
                dict_data = json.loads(dados)
                json_output, _ = process_data_conversion(dict_data, "json")
                st.markdown("<div class='success-box'>✅ Conversão realizada com sucesso!</div>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Baixar JSON",
                    data=json_output,
                    file_name="dados.json",
                    mime="application/json",
                    use_container_width=True
                )
                with preview_col:
                    st.json(dict_data, expanded=True)
            except json.JSONDecodeError:
                st.markdown("<div class='error-box'>❌ Erro: JSON inválido!</div>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"<div class='error-box'>❌ Erro: {str(e)}</div>", unsafe_allow_html=True)

    elif operacao == "Dict → CSV":
        st.markdown("###  Python Dict → CSV", unsafe_allow_html=True)
        dados = st.text_area(
            "Digite seu dicionário Python",
            placeholder='{"nome": "João", "idade": 20, "ativo": true}',
            height=250,
            key="dict_input_csv"
        )
        
        if st.button(" Converter para CSV", use_container_width=True, type="primary"):
            try:
                dict_data = json.loads(dados)
                csv_output, _ = process_data_conversion(dict_data, "csv")
                st.markdown("<div class='success-box'>✅ Conversão realizada com sucesso!</div>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Baixar CSV",
                    data=csv_output,
                    file_name="dados.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                with preview_col:
                    df = pd.read_csv(csv_output)
                    st.dataframe(df, use_container_width=True)
            except json.JSONDecodeError:
                st.markdown("<div class='error-box'>❌ Erro: JSON inválido!</div>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"<div class='error-box'>❌ Erro: {str(e)}</div>", unsafe_allow_html=True)

    elif operacao == "JSON → CSV":
        st.markdown("###  JSON → CSV", unsafe_allow_html=True)
        arquivo = st.file_uploader("Envie seu arquivo JSON", type=["json"], key="json_upload")
        
        if arquivo and st.button(" Converter para CSV", use_container_width=True, type="primary"):
            try:
                buffer = io.BytesIO(arquivo.getvalue())
                df = parse_json(buffer)
                csv_output, _ = export_csv(df)
                st.markdown("<div class='success-box'>✅ Conversão realizada com sucesso!</div>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Baixar CSV",
                    data=csv_output,
                    file_name=f"{arquivo.name.replace('.json', '')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                with preview_col:
                    st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.markdown(f"<div class='error-box'>❌ Erro: {str(e)}</div>", unsafe_allow_html=True)

    elif operacao == "CSV → JSON":
        st.markdown("###  CSV → JSON", unsafe_allow_html=True)
        arquivo = st.file_uploader("Envie seu arquivo CSV", type=["csv"], key="csv_upload")
        
        if arquivo and st.button(" Converter para JSON", use_container_width=True, type="primary"):
            try:
                buffer = io.BytesIO(arquivo.getvalue())
                df = parse_csv(buffer)
                json_output, _ = export_json(df)
                st.markdown("<div class='success-box'>✅ Conversão realizada com sucesso!</div>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Baixar JSON",
                    data=json_output,
                    file_name=f"{arquivo.name.replace('.csv', '')}.json",
                    mime="application/json",
                    use_container_width=True
                )
                with preview_col:
                    st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.markdown(f"<div class='error-box'>❌ Erro: {str(e)}</div>", unsafe_allow_html=True)

    elif operacao == "XLSX → CSV":
        st.markdown("###  XLSX → CSV", unsafe_allow_html=True)
        arquivo = st.file_uploader("Envie seu arquivo XLSX", type=["xlsx"], key="xlsx_upload")
        
        if arquivo and st.button(" Converter para CSV", use_container_width=True, type="primary"):
            try:
                df = pd.read_excel(arquivo)
                csv_output, _ = export_csv(df)
                st.markdown("<div class='success-box'>✅ Conversão realizada com sucesso!</div>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Baixar CSV",
                    data=csv_output,
                    file_name=f"{arquivo.name.replace('.xlsx', '')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                with preview_col:
                    st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.markdown(f"<div class='error-box'>❌ Erro: {str(e)}</div>", unsafe_allow_html=True)

    elif operacao == "CSV → XLSX":
        st.markdown("###  CSV → XLSX", unsafe_allow_html=True)
        arquivo = st.file_uploader("Envie seu arquivo CSV", type=["csv"], key="csv_xlsx_upload")
        
        if arquivo and st.button(" Converter para XLSX", use_container_width=True, type="primary"):
            try:
                df = pd.read_csv(arquivo)
                output = io.BytesIO()
                df.to_excel(output, index=False, engine='openpyxl')
                output.seek(0)
                st.markdown("<div class='success-box'>✅ Conversão realizada com sucesso!</div>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Baixar XLSX",
                    data=output,
                    file_name=f"{arquivo.name.replace('.csv', '')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                with preview_col:
                    st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.markdown(f"<div class='error-box'>❌ Erro: {str(e)}</div>", unsafe_allow_html=True)

# Footer com informações
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("📌 **Formatos Suportados**")
    st.caption("CSV, JSON, XLSX, TXT")
with col2:
    st.caption("💾 **Máximo de Upload**")
    st.caption("10 MB")
with col3:
    st.caption("🔒 **Segurança**")
    st.caption("Nenhum dado é armazenado")
