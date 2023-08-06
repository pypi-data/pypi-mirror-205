import logging
import os
import shutil
import pathlib
import typing

import toml
from optilibre import supported_config_version_min


def ensure_folder_exists(path: pathlib.Path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except PermissionError:
        logging.exception("Can't create path {}. No Permission.".format(str(path)))


def get_conf_version(conf):
    """return main config file version"""
    try:
        version = conf['optilibre']['version']
    except KeyError:
        logging.warning("Version of the main config file could not be found. Assuming we are at least at %s. " % str(supported_config_version_min))
        version = supported_config_version_min

    return version


def get_local_conf_version(conf):
    """return local (sub) config file versiob"""
    try:
        if 'optiimage' in conf:
            version = conf['optiimage']['version']
        elif 'optivideo' in conf:
            version = conf['optivideo']['version']
        else:
            raise KeyError

    except KeyError:
        logging.warning("Version of the local config file could not be found. Assuming we are at least at %s. " % str(supported_config_version_min))
        logging.debug(conf)
        version = supported_config_version_min

    return version


def get_escaped_path(path: typing.Union[str, pathlib.Path]) -> pathlib.Path:
    """
    Return a Path from provided path (it helps convert str with escape char (\\) to a valid Path)
    """
    if type(path) is str and '\\' in path:
        return pathlib.Path(path.replace('\\', ''))
    else:
        return pathlib.Path(path)


def get_path_as_escaped_str(path: pathlib.Path) -> str:
    return str(path).replace(" ", "\\ ")


def check_version(conf_version):
    if conf_version < supported_config_version_min:
        raise ValueError("Config version ({}) mismatched minimum supported version ({})".format(
            conf_version, supported_config_version_min
        ))
    else:
        logging.debug("Config file version ({}) is supported".format(conf_version))


def check_local_version(local_conf):
    conf_version = get_local_conf_version(conf=local_conf)
    if conf_version < supported_config_version_min:
        raise ValueError("Config version ({}) mismatched minimum supported version ({})".format(
            conf_version, supported_config_version_min
        ))
    else:
        logging.debug("Local config file version ({}) is supported".format(conf_version))


def is_config_enabled(config):
    if "enabled" in config:
        return config["enabled"]
    else:
        logging.debug("No enabled line found. Assuming it is.")
        return True


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    return shutil.which(name) is not None


def path_exist(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        logging.error("Path (%s) doesn't exist or is not a directory." % path)
        # RETURN
        return False
    else:
        # RETURN
        return True


def _get_or_raise_path(folder_config, key: str) -> pathlib.Path:
    if key in folder_config:
        path = get_escaped_path(folder_config[key])
    else:
        logging.error("_get_or_raise_path: there is no key named {} in folder_config: {}".format(key, folder_config))
        raise FileNotFoundError("%s is not in configuration." % key)
    if not path_exist(path):
        logging.error("_get_or_raise_path: {} is not a valid path. folder_config: {}".format(path, folder_config))
        raise FileNotFoundError("%s not a valid path." % path)
    else:
        return path


def get_or_raise_in_path(folder_config):
    return _get_or_raise_path(folder_config=folder_config, key="in_path")


def get_or_raise_out_path(folder_config):
    return _get_or_raise_path(folder_config=folder_config, key="out_path")


def get_local_config(conf) -> dict:
    """
    Open and merge local (folder specific) config file if configured
    :param conf: main config file
    :return: local config file
    """
    local_config = conf

    if 'config_file' in conf:
        local_conf_file = os.path.join(conf['config_file'])
    elif 'path' in conf:
        logging.warning("Path= is not supported anymore. Migrate to config_file")
        raise KeyError("Path= is not supported anymore. Migrate to config_file=")
    else:
        logging.debug("No local config file given. Assuming the configuration is in main config file.")
        local_conf_file = None

    if local_conf_file is not None:
        try:
            with open(local_conf_file, 'r') as f:
                file_data = toml.load(f)

            # Add content from file
            for type_ in ("optiimage", "optivideo"):
                if type_ in file_data:
                    local_config[type_] = file_data[type_]

        except OSError or FileNotFoundError:
            logging.exception("Could not find {} conf file for {}.".format(local_conf_file, local_config))
            local_config = None
            exit(13)  # EXIT

    logging.debug("get_local_config: Current configuration: {}".format(
        local_config
    ))
    check_local_version(local_conf=local_config)

    return local_config
