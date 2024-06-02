from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from exceptions.custom_exceptions import ImageValidationException
from image_processing.compress import ImageCompression

import os


app = FastAPI()

upload_directory = "uploads"
os.makedirs(upload_directory, exist_ok=True)


@app.post("/compress/")
async def upload_file(image: UploadFile = File(...)):
    print("image ->", image)
    if image.size == 0:
        raise HTTPException(status_code=400, detail="IMAGE-FIELD-EMPTY")

    file_location = os.path.join(upload_directory, image.filename)
    with open(file_location, "wb") as f:
        f.write(await image.read())

        image = ImageCompression(file_location)

        try:
            image.compress()
        except ImageValidationException as e:
            raise HTTPException(status_code=400, detail=str(e))

        if not os.path.exists(file_location):
            raise HTTPException(
                status_code=400, detail="Compressed file not found")

        return FileResponse(file_location)
