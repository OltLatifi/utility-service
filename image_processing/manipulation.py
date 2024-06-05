import cv2
import numpy as np
from PIL import Image
from .image import BaseImage


class ImageManipulation(BaseImage):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self.handle_errors()
        self.delete_one_image()

    def compress(self):
        with Image.open(self.filename) as image:
            image = image.resize(
                (image.width, image.height), Image.NEAREST)
            image.save(self.filename)
