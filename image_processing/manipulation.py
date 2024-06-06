from exceptions.custom_exceptions import QualityValueExceeded
from rembg import remove
from PIL import Image
from io import BytesIO

from .image import BaseImage
import os


class ImageManipulation(BaseImage):
    def __init__(self, filename: str, data: BytesIO) -> None:
        super().__init__(filename, data)
        self.handle_errors()
        self.delete_one_image()

    def compress(self, quality: int = 80, webp: bool = True):
        if quality < 10 or quality > 100:
            raise QualityValueExceeded(
                "Quality should be a value between 10 and 100")

        with Image.open(self.data) as image:
            width = int(image.width * 0.8)
            height = int(image.height * 0.8)
            image = image.resize(
                (width, height), Image.LANCZOS)
            image.save(self.filename, optimize=True, quality=int(quality))

    def remove_bg(self) -> str:
        """
        Forcing png as an extention for
        Images without a background
        """
        base = os.path.splitext(self.filename)[0]
        derived_filename = base + ".png"

        with Image.open(self.data) as image:
            imageWithoutBg = remove(image)
            imageWithoutBg.save(derived_filename)

        return derived_filename
