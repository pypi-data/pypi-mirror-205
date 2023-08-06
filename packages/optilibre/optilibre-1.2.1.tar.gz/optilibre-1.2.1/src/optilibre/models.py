import json
import logging
import optilibre.enums as enums
import optilibre.helpers as helpers
from pathlib import Path


class Folder:
    def __init__(self, name, enabled, config_as_json):
        self.name: str = name
        self.enabled: bool = enabled
        self.config: json = config_as_json  # json located in 'optiimage' or 'optivideo'

        self.in_path: Path = helpers.get_or_raise_in_path(folder_config=self.get_config())
        self.out_path: Path = helpers.get_or_raise_out_path(folder_config=self.get_config())

    def get_config(self) -> dict:
        return self.config

    def get_name(self) -> str:
        return self.name

    def get_in_path(self) -> Path:
        return self.in_path

    def get_out_path(self) -> Path:
        return self.out_path

    def get_on_success_path(self) -> [Path, None]:
        if 'src_on_success_dest' not in self.config:
            logging.debug("src_on_success_dest is not defined for {}".format(self.name))
            return None
        return Path(self.config['src_on_success_dest'])

    def get_on_failure_path(self) -> [Path, None]:
        if 'src_on_failure_dest' not in self.config:
            logging.debug("src_on_failure_dest is not defined for {}".format(self.name))
            return None
        return Path(self.config['src_on_failure_dest'])


class ImageFolder(Folder):
    def get_codec(self):
        codec_str = self.get_config()["codec"]
        try:
            codec = enums.ImageCodec[codec_str.lower()]
        except KeyError:
            logging.error("%s is not a supported video codec." % codec_str)
            raise KeyError

        return codec

    @staticmethod
    def get_opti_type():
        return "optiimage"


class VideoFolder(Folder):
    def get_audio_codec(self) -> enums.AudioCodec:
        codec_str = self.get_config()['audio']['codec']
        try:
            codec = enums.AudioCodec(codec_str.lower())
        except KeyError:
            logging.error("%s is not a supported video codec." % codec_str)
            raise KeyError

        return codec

    def get_video_codec(self) -> enums.VideoCodec:
        codec_str = self.get_config()['video']['codec']
        try:
            codec = enums.VideoCodec[codec_str.lower()]
        except KeyError:
            logging.error("%s is not a supported video codec." % codec_str)
            raise KeyError

        return codec

    def get_format_container(self) -> enums.VideoContainer:
        if 'container' in (config := self.get_config()):
            container = config['container']
        else:
            # if no container is defined or is invalid
            video_codec = self.get_video_codec()
            if video_codec in [enums.VideoCodec.libx264, enums.VideoCodec.libx265]:
                container = enums.VideoContainer.mp4
            else:
                logging.error("Could not find a suitable container for codec {}".format(video_codec))
                container = None

        try:
            container = enums.VideoContainer(container)
        except ValueError:
            logging.error("Desired container format ({}) is not supported.")
            raise

        return container

    @staticmethod
    def get_opti_type():
        return "optivideo"


class GlobalConfig:
    def __init__(self, version):
        self.version = version
        self.image_folder_list = []
        self.video_folder_list = []

        helpers.check_version(conf_version=self.get_version())

    def get_image_folders(self) -> [ImageFolder]:
        return self.image_folder_list

    def get_video_folders(self) -> [VideoFolder]:
        return self.video_folder_list

    def get_version(self) -> float:
        return self.version
