import os
from io import BytesIO
from processing.smart_crop import SmartCrop
from processing.manipulation import ImageManipulation
from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from imagecompressor.exceptions import ImageValidationException, QualityValueExceeded
from django.http import FileResponse
from ninja.errors import HttpError

api = NinjaAPI()

upload_directory = "uploads"
os.makedirs(upload_directory, exist_ok=True)


@api.post("/compress/")
def upload(request, quality: int = 20, image: UploadedFile = File(...)):
    if image.size == 0:
        raise HttpError(status_code=400, message="IMAGE-FIELD-EMPTY")

    file_location = os.path.join(upload_directory, image.name)
    with open(file_location, "wb") as f:
        data = BytesIO(image.read())

        try:
            image = ImageManipulation(file_location, data)
            image.compress(quality)
        except (ImageValidationException, QualityValueExceeded) as e:
            raise HttpError(status_code=400, message=str(e))

        image_file = open(file_location, 'rb')
        return FileResponse(image_file)


@api.post("/smart-crop/")
def smart_crop(request, width: int = 400, height: int = 400, image: UploadedFile = File(...)):
    if image.size == 0:
        raise HttpError(status_code=400, message="IMAGE-FIELD-EMPTY")

    file_location = os.path.join(upload_directory, image.name)
    with open(file_location, "wb") as f:
        f.write(image.read())

        try:
            image = SmartCrop(file_location, None)
        except ImageValidationException as e:
            raise HttpError(status_code=400, message=str(e))

        image.save(width, height)

        image_file = open(file_location, 'rb')
        return FileResponse(image_file)


@api.post("/remove-bg/")
def remove_bg(request, image: UploadedFile = File(...)):
    if image.size == 0:
        raise HttpError(status_code=400, detail="IMAGE-FIELD-EMPTY")

    file_location = os.path.join(upload_directory, image.name)
    with open(file_location, "wb") as f:
        data = BytesIO(image.read())

        try:
            image = ImageManipulation(file_location, data)
        except ImageValidationException as e:
            raise HttpError(status_code=400, message=str(e))

        file_location = image.remove_bg()
        image_file = open(file_location, 'rb')

        return FileResponse(image_file)
