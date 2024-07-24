from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import boto3
import os
from botocore.exceptions import NoCredentialsError

app = FastAPI()

s3 = boto3.client('s3')

bucket_name = os.getenv('S3_BUCKET_NAME')


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        s3.upload_fileobj(file.file, bucket_name, file.filename)
        return {"filename": file.filename}
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="Credentials not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    try:
        s3.download_file(bucket_name, filename, filename)
        return FileResponse(path=filename, filename=filename)
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="Credentials not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
