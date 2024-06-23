import os
from io import BytesIO
from image_processing.schemas import CompressionIn, SmartCropIn
from processing.smart_crop import SmartCrop
from processing.manipulation import ImageManipulation
from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from imagecompressor.exceptions import ImageValidationException, QualityValueExceeded, ThrottleError
from django.http import FileResponse
from ninja.errors import HttpError
from authentication.token import AuthBearer

api = NinjaAPI()

upload_directory = "uploads"
os.makedirs(upload_directory, exist_ok=True)


@api.exception_handler(ThrottleError)
def on_throttle(request, exc):
    return api.create_response(request, {"detail": "Request denied, too many requests"}, status=429)


@api.post("/compress/", auth=AuthBearer(), tags=['Image'])
def compress(request, body: CompressionIn, image: UploadedFile = File(...)):
    if image.size == 0:
        raise HttpError(status_code=400, message="IMAGE-FIELD-EMPTY")

    file_location = os.path.join(upload_directory, image.name)
    data = BytesIO(image.read())

    try:
        image = ImageManipulation(file_location, data)
        image.compress(body.quality)
    except (ImageValidationException, QualityValueExceeded) as e:
        raise HttpError(status_code=400, message=str(e))

    image_file = open(file_location, 'rb')
    return FileResponse(image_file)


@api.post("/smart-crop/", auth=AuthBearer(), tags=['Image'])
def smart_crop(request, body: SmartCropIn, image: UploadedFile = File(...)):
    if image.size == 0:
        raise HttpError(status_code=400, message="IMAGE-FIELD-EMPTY")

    file_location = os.path.join(upload_directory, image.name)
    with open(file_location, "wb") as f:
        f.write(image.read())

        try:
            image = SmartCrop(file_location, None)
        except ImageValidationException as e:
            raise HttpError(status_code=400, message=str(e))

        image.save(body.width, body.height)

        image_file = open(file_location, 'rb')
        return FileResponse(image_file)


@api.post("/remove-bg/", auth=AuthBearer(), tags=['Image'])
def remove_bg(request, image: UploadedFile = File(...)):
    if image.size == 0:
        raise HttpError(status_code=400, detail="IMAGE-FIELD-EMPTY")

    file_location = os.path.join(upload_directory, image.name)
    data = BytesIO(image.read())

    try:
        image = ImageManipulation(file_location, data)
    except ImageValidationException as e:
        raise HttpError(status_code=400, message=str(e))

    file_location = image.remove_bg()
    image_file = open(file_location, 'rb')

    return FileResponse(image_file)
