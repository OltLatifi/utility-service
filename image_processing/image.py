from PIL import Image


class BaseImage:
    def __init__(self, filename) -> None:
        self.filename = filename

    def validate(self) -> bool:
        try:
            Image.open(self.filename)
        except AttributeError:
            return (False, "IMAGE-FIELD-EMPTY")
        except:
            return (False, "FILE-NOT-IMAGE")
        return (True, "")
