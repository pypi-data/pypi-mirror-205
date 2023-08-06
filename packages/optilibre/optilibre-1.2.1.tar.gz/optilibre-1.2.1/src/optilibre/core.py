import logging
import os
import optilibre.helpers as helpers

from optilibre import models as models, enums as enums
from optilibre.helpers import path_exist, get_path_as_escaped_str
from pathlib import Path


def cmd_src_on_success_failure(config, subdir_relative: Path, on_success_failure: 'success, failure'):
    """
    Return shell cmd to execute on success or failure for the src file.
    :param config:
    :param subdir_relative:
    :param on_success_failure:
    :return:
    """
    src_on_keyword = 'src_on_' + on_success_failure
    src_on_keyword_dest = src_on_keyword + '_dest'
    if src_on_keyword not in config:
        logging.info("%s is not defined, default back to 'keep'" % src_on_keyword)
        config[src_on_keyword] = 'keep'

    on_success_failure = config[src_on_keyword]
    cmd_on_success_failure = ""
    if on_success_failure == 'keep':
        pass
    elif on_success_failure == 'move':
        if src_on_keyword_dest not in config:
            logging.warning("%s was defined as 'move' but not %s was defined. Default back to 'keep'." %
                            (src_on_keyword, src_on_keyword_dest))

        dest = config[src_on_keyword_dest]
        if subdir_relative:
            dest = os.path.join(dest, subdir_relative)
            helpers.ensure_folder_exists(dest)
        if not path_exist(dest):
            logging.warning("Default back to keep for %s" % on_success_failure)
        else:
            cmd_on_success_failure = "mv {0} " + get_path_as_escaped_str(path=dest) + "/{1}"
            logging.debug("CMD on success failure (move) {}".format(cmd_on_success_failure))
    elif on_success_failure == 'delete':
        cmd_on_success_failure = "rm {0}"

    return cmd_on_success_failure


def do_src_on_done(exit_code: int, file, local_config, subdir_relative: Path):
    """
    Launch shell cmd to execute on success or failure, to move, delete ... src file.
    :param subdir_relative: (if subdir) subdir where the file was located (relative to in_path)
    :param local_config:
    :param exit_code:
    :param file:
    :return:
    """

    if exit_code == 0:
        cmd = cmd_src_on_success_failure(config=local_config, subdir_relative=subdir_relative, on_success_failure='success')
        logging.debug("Exit code was successful.")
    else:
        cmd = cmd_src_on_success_failure(config=local_config, subdir_relative=subdir_relative, on_success_failure='failure')
        logging.debug("Exit code was not successful %s" % str(exit_code))

    cmd = cmd.format(get_path_as_escaped_str(path=file), get_path_as_escaped_str(path=os.path.basename(file)))
    logging.debug("Execute post convert (empty if 'keep'): %s" % cmd)
    os.system(cmd)

    return None


def build_cmdline_video(folder: models.VideoFolder) -> str:
    """
    Build cmdline options
    :param folder:
    :return: cmdline (without in and out files)
    """

    codec_video = folder.get_video_codec()
    local_config = folder.get_config()

    # Set default options if not already set
    if "map_metadata" not in local_config['meta']:
        local_config['meta']['map_metadata'] = 0
    if "n" not in local_config['meta'] or "y" not in local_config['meta']:
        local_config['meta']['n'] = ''
    if codec_video == enums.VideoCodec.libx265 and "dst_range" not in local_config[codec_video.name]:
        # enable full color range for x265 per default
        local_config[codec_video.name]['dst_range'] = 1

    # Build cmdline
    cmdline_meta = ""
    if 'meta' in local_config:
        for opt in local_config['meta'].items():
            cmdline_meta += " -" + str(opt[0]) + " " + str(opt[1])

    cmdline_audio = ""
    if local_config['audio']['enabled']:
        cmdline_audio = "-c:a " + str(folder.get_audio_codec())

    cmdline_video = ""
    if local_config['video']['enabled']:
        cmdline_video = "-c:v " + codec_video.name
        for opt in local_config[local_config['video']['codec']].items():
            cmdline_video += " -" + str(opt[0]) + " " + str(opt[1])

    return "ffmpeg -i " + "'{}'" + cmdline_meta + " " + cmdline_audio + " " + cmdline_video + " " + "'{}'"
