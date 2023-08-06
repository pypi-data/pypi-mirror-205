import coloredlogs
import logging
import importlib.metadata

__version__ = "Unknown"
try:
    __version__ = importlib.metadata.version('optilibre')
except importlib.metadata.PackageNotFoundError:
    # package is not installed
    logging.warning("Optilibre (unknown version). Is the package installed ?")

coloredlogs.install(level=logging.DEBUG)

supported_config_version_min = 1.0
supported_img_ext = [".jpeg", ".jpg", ".jpegxl", ".jxl"]
supported_video_ext = [".mp4", ".mkv", ".webm"]
