from enum import Enum


class ImageCodec(Enum):
    jpeg = "jpeg"
    jpegxl = "jpegxl"

    def __str__(self):
        return self.value

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__


class AudioCodec(Enum):
    aac = "aac"
    ogg = "ogg"

    def __str__(self):
        return self.value

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__


class VideoCodec(Enum):
    libx264 = "libx264"
    libx265 = "libx265"

    def __str__(self):
        return self.value

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__


class VideoContainer(Enum):
    avi = "avi"
    mkv = "mkv"
    mp4 = "mp4"

    def __str__(self):
        return self.value

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__
