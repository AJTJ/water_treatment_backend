from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict
from app.services.s3_service import upload_file_to_s3
import os

router: APIRouter = APIRouter()

MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    Upload a file to S3 and return the CloudFront URL.

    :param file: File to be uploaded.
    :return: The CloudFront URL of the uploaded file.
    """
    try:
        file_content: bytes = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size ({len(file_content)}) exceeds the limit of {MAX_FILE_SIZE}bytes",
            )
        base_filename: str = os.path.basename(file.filename or "default_filename")
        print("filename", base_filename)

        cloudfront_url: str = upload_file_to_s3(file_content, base_filename)
        return {"message": f"File uploaded successfully.", "url": cloudfront_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
