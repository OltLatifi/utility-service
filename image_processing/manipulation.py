import cv2
import numpy as np
from PIL import Image
from .image import BaseImage


class ImageManipulation(BaseImage):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self.handle_errors()

    def compress(self):
        with Image.open(self.filename) as image:
            image = image.resize(
                (image.width, image.height), Image.NEAREST)
            image.save(self.filename)

    def smart_crop(self, crop_width: int, crop_height: int, compress: bool = False):
        """
        Turns Image to grayscale to reduce computational complexity, finds edges and 
        cuts the image outside of that box.
        """
        with Image.open(self.filename) as image:
            img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)

            contours, _ = cv2.findContours(
                edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
            else:
                x, y, w, h = 0, 0, img.shape[1], img.shape[0]

            crop_x = max(0, x + w // 2 - crop_width // 2)
            crop_y = max(0, y + h // 2 - crop_height // 2)
            crop_x = min(crop_x, img.shape[1] - crop_width)
            crop_y = min(crop_y, img.shape[0] - crop_height)

            cropped_image = image.crop(
                (crop_x, crop_y, crop_x + crop_width, crop_y + crop_height))
            cropped_image.save(self.filename)

            if compress:
                self.compress()
