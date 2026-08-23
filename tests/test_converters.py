import pytest

from converters import process_file_conversion


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