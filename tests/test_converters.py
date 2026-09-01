import json

import pytest

from converters import process_data_conversion, process_file_conversion


def test_dict_para_json_retorna_json_valido():
    payload = {"usuarios": [{"nome": "Ana", "idade": 30}, {"nome": "Bruno", "idade": 28}]}
    output, media_type = process_data_conversion(payload, "json")

    assert media_type == "application/json"
    assert json.loads(output.getvalue().decode("utf-8")) == payload


def test_dict_para_csv_retorna_colunas_e_dados():
    output, media_type = process_data_conversion(
        {"nome": "Ana", "idade": 30},
        "csv",
    )

    assert media_type == "text/csv"
    assert output.getvalue().decode("utf-8") == "nome,idade\nAna,30\n"


def test_txt_preserva_linhas_sem_cabecalho():
    output, media_type = process_file_conversion(
        b"Ana\n\nBruno\n", ".txt", "txt"
    )

    assert media_type == "text/plain"
    assert output.getvalue().decode("utf-8") == "Ana\nBruno"


def test_csv_para_txt_gera_linhas_sem_indice():
    output, _ = process_file_conversion(
        b"nome,idade\nAna,30\n", ".csv", "txt"
    )

    assert output.getvalue().decode("utf-8") == "Ana\t30"


@pytest.mark.parametrize(
    ("content", "extension", "target"),
    [
        (b"", ".csv", "json"),
        (b"{invalido", ".json", "csv"),
        (b"\xff\xfe", ".txt", "csv"),
        (b"\"texto\"", ".json", "csv"),
    ],
)
def test_rejeita_entradas_invalidas(content, extension, target):
    with pytest.raises(ValueError):
        process_file_conversion(content, extension, target)


def test_normaliza_formato_de_saida():
    output, media_type = process_file_conversion(
        b"nome\nAna\n", ".TXT", " JSON "
    )

    assert media_type == "application/json"
    assert b'"conteudo":"nome"' in output.getvalue()
    assert b'"conteudo":"Ana"' in output.getvalue()