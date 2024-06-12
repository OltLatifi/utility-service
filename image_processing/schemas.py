from ninja import Schema


class ManipulationIn(Schema):
    compression: int = 0
    invert: int = 0
    blur: int = 0
    smooth: int = 0
    sharpen: int = 0
    grayscale: int = 0
    rotate: int = 0
