from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, status
from fastapi.responses import StreamingResponse
from converters import process_file_conversion

app = FastAPI(title="File Converter API")
MAX_FILE_SIZE = 10 * 1024 * 1024


@app.post("/convert")
async def convert_file(
    file: UploadFile = File(...),
    target_format: str = Form(...),
):
    try:
        if not file.filename:
            raise ValueError("O arquivo enviado não possui nome.")

        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise ValueError("O arquivo excede o limite de 10 MB.")

        file_ext = Path(file.filename).suffix
        target_format = target_format.strip().lower()

        output_buffer, media_type = process_file_conversion(
            content, file_ext, target_format
        )

        output_filename = f"{Path(file.filename).stem}.{target_format.lower()}"
        return StreamingResponse(
            output_buffer,
            media_type=media_type,
            headers={
                "Content-Disposition": f'attachment; filename="{output_filename}"'
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UnicodeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Arquivo com codificação inválida: {e}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}",
        )
