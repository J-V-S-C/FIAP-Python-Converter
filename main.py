from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, status
from fastapi.responses import StreamingResponse
from converters import process_file_conversion, EXPORTERS

app = FastAPI(title="File Converter API")


@app.post("/convert")
async def convert_file(
    file: UploadFile = File(...),
    target_format: str = Form(...),
):
    try:
        content = await file.read()
        file_ext = Path(file.filename).suffix

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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}",
        )
