import streamlit as st
import requests


# Configuração da página inicial da interface Streamlit.
st.set_page_config(
    page_title="File Converter",
    page_icon="🔄",
    layout="centered"
)


# CSS para ajustar a aparência da interface e centralizar os elementos.
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


# Título principal da aplicação.
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


# Área para selecionar o arquivo a ser convertido.
st.markdown(
    '<div class="section-title">📁 Arquivo:</div>',
    unsafe_allow_html=True
)

arquivo = st.file_uploader(
    "Selecione o arquivo que deseja converter",
    type=["json", "csv", "txt"]
)


# Seletor de formato de saída desejado.
st.markdown(
    '<div class="section-title">📤 Formato de saída:</div>',
    unsafe_allow_html=True
)

formato_saida = st.selectbox(
    "Converter para:",
    ["CSV", "JSON", "TXT"]
)


# Botão que dispara a conversão.
st.write("")

converter = st.button(
    "🔄 Converter arquivo",
    use_container_width=True
)


# Fluxo principal de conversão.
if converter:

    if arquivo is None:
        # Valida se o usuário selecionou um arquivo antes de chamar a API.
        st.warning(
            "⚠️ Selecione um arquivo antes de converter."
        )

    else:
        with st.spinner("Convertendo arquivo..."):
            try:
                # Faz a requisição para a API FastAPI com o arquivo e o formato de destino.
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

                # Caso a API responda com sucesso, exibe mensagem e botão de download.
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

                # Se a API retornar erro, mostra a mensagem recebida.
                else:
                    try:
                        erro = response.json()["detail"]
                    except Exception:
                        erro = "Erro ao converter o arquivo."

                    st.error(f"❌ {erro}")

            except requests.exceptions.Timeout:
                # API demorou demais para responder.
                st.error(
                    "❌ A API demorou mais de 30 segundos para responder."
                )

            except requests.exceptions.ConnectionError:
                # Serviço da API está indisponível.
                st.error(
                    "❌ Não foi possível conectar à API."
                )

                st.info(
                    "Verifique se o FastAPI está rodando "
                    "em http://127.0.0.1:8000"
                )

            except requests.exceptions.RequestException as error:
                # Falha genérica de comunicação com a API.
                st.error(f"❌ Erro na comunicação com a API: {error}")