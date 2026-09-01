import streamlit as st
import requests



# Configuração da pagina


st.set_page_config(
    page_title="File Converter",
    page_icon="🔄",
    layout="centered"
)



# CSS gambiarra!


st.markdown("""
<style>

    .main {
        max-width: 900px;
        margin: auto;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #888;
        font-size: 18px;
        margin-bottom: 40px;
    }

    .section-title {
        font-size: 20px;
        font-weight: bold;
        margin-top: 20px;
    }

</style>
""", unsafe_allow_html=True)



# Titulo

st.markdown(
    '<div class="title">🔄 File Converter</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Converta seus arquivos entre JSON, CSV e TXT'
    '</div>',
    unsafe_allow_html=True
)



# UPLOAD

st.markdown(
    '<div class="section-title">📁 Arquivo:</div>',
    unsafe_allow_html=True
)

arquivo = st.file_uploader(
    "Selecione o arquivo que deseja converter",
    type=["json", "csv", "txt"]
)



# Formato de saída

st.markdown(
    '<div class="section-title">📤 Formato de saída:</div>',
    unsafe_allow_html=True
)

formato_saida = st.selectbox(
    "Converter para:",
    ["CSV", "JSON", "TXT"]
)



# Converter

st.write("")

converter = st.button(
    "🔄 Converter arquivo",
    use_container_width=True
)


if converter:

    if arquivo is None:

        st.warning(
            "⚠️ Selecione um arquivo antes de converter."
        )

    else:

        with st.spinner("Convertendo arquivo..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/convert",
                    files={
                        "file": (
                            arquivo.name,
                            arquivo.getvalue()
                        )
                    },
                    data={
                        "target_format": formato_saida.lower()
                    },
                    timeout=30,
                )


                
                # Sucesso!
        

                if response.status_code == 200:

                    st.success(
                        "✅ Arquivo convertido com sucesso!"
                    )

                    nome_original = arquivo.name.rsplit(
                        ".", 1
                    )[0]

                    nome_download = (
                        f"{nome_original}."
                        f"{formato_saida.lower()}"
                    )


                   
                    # Download
                    

                    st.download_button(
                        label="⬇️ Baixar arquivo",
                        data=response.content,
                        file_name=nome_download,
                        mime=response.headers.get(
                            "content-type",
                            "application/octet-stream"
                        ),
                        use_container_width=True
                    )


                
                # ERRO da API!
                

                else:

                    try:
                        erro = response.json()["detail"]
                    except Exception:
                        erro = "Erro ao converter o arquivo."

                    st.error(f"❌ {erro}")


            except requests.exceptions.Timeout:
                st.error(
                    "❌ A API demorou mais de 30 segundos para responder."
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Não foi possível conectar à API."
                )

                st.info(
                    "Verifique se o FastAPI está rodando "
                    "em http://127.0.0.1:8000"
                )

            except requests.exceptions.RequestException as error:
                st.error(f"❌ Erro na comunicação com a API: {error}")