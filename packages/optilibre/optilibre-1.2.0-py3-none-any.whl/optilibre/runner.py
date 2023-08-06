import filetype
import logging
import os
import re
import optilibre
import optilibre.core
import optilibre.enums as enums
import optilibre.helpers as helpers
import optilibre.models as models
import optilibre.utils.parsers as parsers
from multiprocessing import Pool
from pathlib import Path

from optilibre.core import build_cmdline_video


def convert_img(file: Path, shell_cmdline: str, local_config: dict, subdir_relative: Path):
    logging.debug("Converting " + str(file))

    # TODO move file extension / output
    logging.info(shell_cmdline)
    exit_code = os.WEXITSTATUS(os.system(shell_cmdline))
    logging.debug("Exit code: %s" % exit_code)
    optilibre.core.do_src_on_done(exit_code=exit_code, file=file, local_config=local_config, subdir_relative=subdir_relative)


def process_image_folder(folder: models.ImageFolder, subdir: Path = None):
    """
    This function recursively process an "optilibre" folder and its subdir.
    For each subdir encountered, call itself with subdir as arg.
    For the subdir in argument, create the subdir in the dest folders.
    """
    in_path = folder.get_in_path()

    subdir_msg = ""
    if subdir:
        subdir_msg = "(subdir: {})".format(subdir.relative_to(in_path))
    logging.info("Treating folder: {} {}".format(folder.get_name(), subdir_msg))

    local_config = folder.get_config()
    out_path = folder.get_out_path()
    codec = folder.get_codec()

    relative_subdir = None
    if subdir:
        # If we are working with a sub dir. Append it to out_path.
        relative_subdir = subdir.relative_to(in_path)  # for src_on_done
        out_path = out_path.joinpath(relative_subdir)  # get subdir from absolute path and join it with out_path
        in_path = subdir
        helpers.ensure_folder_exists(path=out_path)

    # Set default options for JPEGoptim
    if codec == enums.ImageCodec.jpeg:
        # Remove dest if provided (otherwise subdir won't work because of arg as reference)
        local_config[codec.name.lower()].pop('d', None)
        local_config[codec.name.lower()].pop('dest', None)
        #if "d" not in local_config[codec.name.lower()] and "dest" not in local_config[codec.name.lower()]:
        local_config[codec.name.lower()]['d'] = helpers.get_path_as_escaped_str(out_path)

    # Build cmdline options
    cmdline_codec_opts = ""
    if codec.name.lower() in local_config:
        for opt in local_config[codec.name.lower()].items():
            cmdline_codec_opts += " -" + str(opt[0]) + " " + str(opt[1])
    else:
        logging.debug("No config for %s found. Using default codec values." % codec.name)

    arg_list = []  # [(file1, shell1, local_config, subdir), (...)] we split arg_list to processes
    for file in Path(in_path).glob('*'):
        if file.is_file():
            kind = filetype.guess_mime(str(file))
            if bool(re.match("image/+", str(kind))):
                logging.debug("Building cmd line for: %s" % str(file))
                file_mime = filetype.guess_mime(str(file))

                if file.suffix not in optilibre.supported_img_ext or not bool(re.match('image/+', str(file_mime))):
                    # TODO Jpeg-XL can convert non jpeg format.
                    logging.warning("Filetype: %s not supported: for file: %s. Won't convert it." % (str(file_mime), str(file)))
                    # CONTINUE
                    continue

                # JPEG jpegoptim
                if codec == enums.ImageCodec.jpeg:
                    encoder_cmdline = "jpegoptim"
                    out_file = ""

                # JPEG XL
                elif codec == enums.ImageCodec.jpegxl:
                    # TODO implement recursive
                    encoder_cmdline = "cjxl"
                    out_file = os.path.join(out_path, os.path.splitext(os.path.basename(file))[0] + ".jxl")
                else:
                    logging.error("Codec type not supported %s" % str(codec))
                    # CONTINUE
                    continue

                shell_cmdline = "{encoder} {in_file} {options} {outfile}".format(
                    encoder=encoder_cmdline, in_file=helpers.get_path_as_escaped_str(file), options=cmdline_codec_opts, outfile=out_file)

                arg_list.append((file, shell_cmdline, local_config, relative_subdir))
            else:
                # Changing suffix
                logging.debug("Filetype: %s for file: %s isn't an image file." % (str(kind), str(file)))
        elif file.is_dir():
            logging.debug("{} is a directory. Recursively entering it.".format(str(file)))
            process_image_folder(folder=folder, subdir=Path(file))
        else:
            logging.debug("{} is not a file neither a dir. Ignoring it.".format(str(file)))

    # multiprocess call
    if arg_list:
        with Pool() as p:
            p.starmap(convert_img, arg_list)


def process_video_folder(folder: models.VideoFolder, subdir: Path = None):
    """
    This function recursively process an "optilibre" folder and its subdir.
    For each subdir encountered, call itself with subdir as arg.
    For the subdir in argument, create the subdir in the dest folders.
    """
    in_path = folder.get_in_path()

    subdir_msg = ""
    if subdir:
        subdir_msg = "(subdir: {})".format(subdir.relative_to(in_path))
    logging.info("Treating folder: {} {}".format(folder.get_name(), subdir_msg))

    local_config = folder.get_config()
    out_path = folder.get_out_path()

    relative_subdir = None
    if subdir:
        # If we are working with a sub dir. Append it to out_path.
        relative_subdir = subdir.relative_to(in_path)  # for src_on_done
        out_path = out_path.joinpath(relative_subdir)  # get subdir from absolute path and join it with out_path
        in_path = subdir
        helpers.ensure_folder_exists(path=out_path)

    cmdline = build_cmdline_video(folder=folder)

    for file in Path(in_path).glob('*'):  # Path(Path() = Path()
        if file.is_file():
            kind = filetype.guess_mime(str(file))

            if bool(re.match("video/+", str(kind))):
                logging.debug("Processing " + str(file))

                if file.suffix in optilibre.supported_video_ext:
                    out_file = os.path.join(out_path, os.path.basename(
                        file.with_suffix('.' + str(folder.get_format_container()))
                    ))

                    ffmpeg_cmdline = cmdline.format(file, out_file)

                    logging.info(ffmpeg_cmdline)
                    exit_code = os.WEXITSTATUS(os.system(ffmpeg_cmdline))
                    optilibre.core.do_src_on_done(exit_code=exit_code, file=file, local_config=local_config, subdir_relative=relative_subdir)

                else:
                    logging.info("Filetype {} for {} is not (yet) supported.".format(str(file.suffix), str(file)))
            else:
                # Changing suffix
                logging.debug("Filetype: %s for file: %s isn't a video file. Ignoring it." % (str(kind), str(file)))
        elif file.is_dir():
            logging.debug("{} is a directory. Recursively entering it.".format(str(file)))
            process_video_folder(folder=folder, subdir=Path(file))
        else:
            logging.debug("{} is not a file. Ignoring it.".format(str(file)))


def main(config_file):
    global_config = parsers.parse_config_file(config_file_path=config_file)

    logging.info("Processing image files.")
    image_folder: models.ImageFolder
    for image_folder in global_config.get_image_folders():
        process_image_folder(folder=image_folder)

    logging.info("Processing video files.")
    video_folder: models.VideoFolder
    for video_folder in global_config.get_video_folders():
        process_video_folder(folder=video_folder)

