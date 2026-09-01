from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, status
from fastapi.responses import StreamingResponse
from converters import process_file_conversion

# Aplicação principal da API de conversão de arquivos.
app = FastAPI(title="File Converter API")

# Limite máximo do arquivo enviado em bytes.
MAX_FILE_SIZE = 10 * 1024 * 1024


# Recebe um arquivo uploadado e o formato de destino e retorna o conteúdo convertido.
@app.post("/convert")
async def convert_file(
    file: UploadFile = File(...),
    target_format: str = Form(...),
):
    try:
        # Verifica se o nome do arquivo foi informado.
        if not file.filename:
            raise ValueError("O arquivo enviado não possui nome.")

        # Lê o conteúdo do arquivo e valida tamanho.
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise ValueError("O arquivo excede o limite de 10 MB.")

        # Pega a extensão e normaliza o formato de destino.
        file_ext = Path(file.filename).suffix
        target_format = target_format.strip().lower()

        # Realiza a conversão usando a lógica centralizada em converters.py.
        output_buffer, media_type = process_file_conversion(
            content, file_ext, target_format
        )

        # Define o nome do arquivo final no download.
        output_filename = f"{Path(file.filename).stem}.{target_format.lower()}"
        return StreamingResponse(
            output_buffer,
            media_type=media_type,
            headers={
                "Content-Disposition": f'attachment; filename="{output_filename}"'
            },
        )
    except ValueError as e:
        # Erros de validação de entrada do cliente.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UnicodeError as e:
        # Erros de codificação do arquivo.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Arquivo com codificação inválida: {e}",
        )
    except Exception as e:
        # Qualquer erro inesperado da aplicação.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}",
        )
