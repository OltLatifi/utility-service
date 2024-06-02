import os
from PIL import Image
from .image import BaseImage
from exceptions.custom_exceptions import ImageValidationException


class ImageCompression(BaseImage):
    def compress(self):
        image_valid, validation_problem = self.validate()

        if not image_valid:
            os.remove(self.filename)
            raise ImageValidationException(validation_problem)

        with Image.open(self.filename) as image:
            image = image.resize(
                (image.width, image.height), Image.NEAREST)
            image.save(self.filename)
