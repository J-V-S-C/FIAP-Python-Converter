# FIAP Python Converter

Aplicação desenvolvida em Python para conversão de dados entre os formatos JSON, CSV e XLSX, utilizando uma interface simples com Streamlit.

Projeto desenvolvido para o Checkpoint 4 – Computational Thinking With Python.

## Funcionalidades

A aplicação realiza as seguintes conversões:
```text 
Dict → JSON
Dict → CSV
JSON → CSV
CSV → JSON
XLSX → CSV
CSV → XLSX
```
Para conversões com dict, os dados são informados como texto no formato JSON.

Para conversões de arquivos, o usuário realiza o upload diretamente pela interface.

## Lógica da solução

A aplicação separa a interface da lógica de conversão.

O streamlit_app.py é responsável pela interação com o usuário, enquanto o converters.py concentra a lógica de processamento e conversão dos dados.

Para arquivos, o fluxo é:
```text
Arquivo
   ↓
Parser
   ↓
DataFrame
   ↓
Exporter
   ↓
Arquivo convertido
```

O DataFrame do Pandas é utilizado como estrutura intermediária, permitindo reutilizar a mesma lógica para diferentes formatos.

Para dict, o fluxo é:
```
Texto
   ↓
dict Python
   ↓
Conversão
   ↓
JSON ou CSV
```

Isso evita a duplicação de código e facilita a adição de novos formatos no futuro.

Para os dicts, a aplicação recebe o conteúdo como texto e utiliza json.loads() para transformá-lo em um dict Python antes da conversão.

Na conversão para JSON, o dict é exportado diretamente, preservando sua estrutura original.

Na conversão para CSV, o dict é transformado em um DataFrame antes da exportação.

## Tratamento de erros

A aplicação possui tratamento de erros para situações como:
```
Arquivos vazios;
JSON inválido;
CSV inválido;
XLSX inválido;
Codificação de arquivo incompatível;
Formato de entrada não suportado;
Formato de saída não suportado;
Entrada que não representa um dict.
```
Os erros são tratados com exceções e apresentados ao usuário através da interface.

```
Tecnologias
Python
Streamlit
Pandas
OpenPyXL
```

O Pandas é utilizado para leitura, manipulação e transformação dos dados através de DataFrame.

O OpenPyXL é utilizado para trabalhar com arquivos .xlsx.


Estrutura
```
FIAP-Python-Converter/
├── streamlit_app.py
├── converters.py
├── requirements.txt
├── README.md
└── tests/
    └── test_converters.py
```

### streamlit_app.py

Responsável pela interface, entrada de dados, upload dos arquivos e download dos resultados.

### converters.py

Contém a lógica de leitura, conversão e exportação dos dados.

### requirements.txt

Contém as dependências necessárias para executar o projeto.

## Como executar

### Clone o repositório:
```bash
git clone git@github.com:J-V-S-C/FIAP-Python-Converter.git
cd FIAP-Python-Converter
```

### Crie o ambiente virtual:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### Instale as dependências:

```bash
pip install -r requirements.txt
```

### Execute a aplicação:

```bash
streamlit run streamlit_app.py
```

## Integrantes
```
João Cortabitart
João Barbon
João Freitas
```
