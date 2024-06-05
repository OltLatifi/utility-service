from rembg import remove
from PIL import Image
from io import BytesIO
from .image import BaseImage


class ImageManipulation(BaseImage):
    def __init__(self, filename: str, data: BytesIO) -> None:
        super().__init__(filename, data)
        self.handle_errors()
        self.delete_one_image()

    def compress(self):
        with Image.open(self.data) as image:
            image = image.resize(
                (image.width, image.height), Image.LANCZOS)
            image.save(self.filename, optimize=True, quality=90)

    def remove_bg(self):
        with Image.open(self.data) as image:
            imageWithoutBg = remove(image)
            imageWithoutBg.save(self.filename)
