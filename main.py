from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from exceptions.custom_exceptions import ImageValidationException
from image_processing.manipulation import ImageManipulation

import os


app = FastAPI()

upload_directory = "uploads"
os.makedirs(upload_directory, exist_ok=True)


@app.post("/compress/")
async def upload_file(image: UploadFile = File(...)):
    if image.size == 0:
        raise HTTPException(status_code=400, detail="IMAGE-FIELD-EMPTY")

    file_location = os.path.join(upload_directory, image.filename)
    with open(file_location, "wb") as f:
        f.write(await image.read())

        try:
            image = ImageManipulation(file_location)
        except ImageValidationException as e:
            raise HTTPException(status_code=400, detail=str(e))

        image.compress()

        if not os.path.exists(file_location):
            raise HTTPException(
                status_code=400, detail="Compressed file not found")

        return FileResponse(file_location)


@app.post("/smart-crop/")
async def smart_crop(image: UploadFile = File(...), width: int = 200, height: int = 200, compression: bool = False):
    if image.size == 0:
        raise HTTPException(status_code=400, detail="IMAGE-FIELD-EMPTY")

    file_location = os.path.join(upload_directory, image.filename)
    with open(file_location, "wb") as f:
        f.write(await image.read())

        try:
            image = ImageManipulation(file_location)
        except ImageValidationException as e:
            raise HTTPException(status_code=400, detail=str(e))

        image.smart_crop(width, height, compression)

        if not os.path.exists(file_location):
            raise HTTPException(
                status_code=400, detail="Compressed file not found")

        return FileResponse(file_location)
