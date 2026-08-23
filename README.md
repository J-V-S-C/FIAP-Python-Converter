# File Converter

Conversor de arquivos entre CSV, JSON e TXT, com API FastAPI e interface Streamlit.

## Instalação

No PowerShell, dentro da pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Execução

Abra dois terminais com o ambiente virtual ativado.

Terminal da API:

```powershell
uvicorn main:app --reload
```

Terminal da interface:

```powershell
streamlit run streamlit_app.py
```

A interface estará disponível em `http://localhost:8501` e a API em `http://127.0.0.1:8000`.

## Testes

```powershell
python -m pytest
```
