import os
from io import BytesIO
from PIL import Image
from typing import Tuple
from exceptions.custom_exceptions import ImageValidationException


class BaseImage:
    def __init__(self, filename: str, data: BytesIO) -> None:
        self.filename = filename
        self.data = data

    def get_extension(self) -> str:
        base, extension = os.path.splitext(self.filename)
        return extension

    def validate(self) -> Tuple[bool, str]:
        try:
            Image.open(self.data)
        except AttributeError:
            return (False, "IMAGE-FIELD-EMPTY")
        except:
            return (False, "FILE-NOT-IMAGE")
        return (True, "")

    def handle_errors(self) -> None:
        image_valid, validation_problem = self.validate()

        if not image_valid:
            raise ImageValidationException(validation_problem)

    def delete_one_image(self) -> None:
        files = os.listdir("uploads/")
        files = [f for f in files if f != os.path.basename(self.filename)]

        if len(files) < 2:
            return None

        try:
            os.remove(os.path.join("uploads", files[0]))
        except:
            pass
