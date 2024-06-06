from Katna.image import Image
from image_processing.manipulation import ImageManipulation
from typing import Tuple


class SmartCrop(ImageManipulation):
    def process_directory(self) -> Tuple[str, str]:
        file_name, file_ext = self.filename.split(".")
        file_name = self.filename.split("/")[1].split(".")[0]
        file_ext = self.filename.split(".")[1]

        return (file_name, f".{file_ext}")

    def save(self, width: int, height: int):
        img_module = Image()
        crop_list = img_module.resize_image(
            file_path=self.filename,
            target_width=width,
            target_height=height,
            down_sample_factor=2
        )

        file_name, file_ext = self.process_directory()

        img_module.save_image_to_disk(
            crop_list,
            file_path="uploads/",
            file_name=file_name,
            file_ext=file_ext,
        )
