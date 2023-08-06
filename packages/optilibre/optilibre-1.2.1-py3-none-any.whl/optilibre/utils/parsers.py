import toml
import logging
import optilibre.models as models
import optilibre.helpers as helpers


def parse_config_file(config_file_path):
    """
    Parse the config file to build and store configuration in a global_config object.
    @param config_file_path: path to optilibre.conf
    """
    logging.info("Parsing " + config_file_path)
    logging.debug("Any error will be fatal.")
    with open(config_file_path, 'r') as f:
        config = toml.load(f)

    version = helpers.get_conf_version(conf=config)
    global_config = models.GlobalConfig(version=version)

    # Check which type are defined
    types_ = []
    if "image" in config['convert']:
        types_.append("image")
    if "video" in config['convert']:
        types_.append("video")

    # Build image and video "folders"
    for type_ in types_:
        logging.debug("Folders {}".format(config['convert'][type_]))
        for folder_name in config['convert'][type_]:
            logging.info("Parsing {}".format(folder_name))
            folder_config = helpers.get_local_config(conf=config['convert'][type_][folder_name])
            enabled = helpers.is_config_enabled(config=folder_config)
            if not enabled:
                logging.info("The folder {} is disabled. Continue with the next folder.".format(folder_name))
                continue

            try:
                if type_ == "image":
                    folder_name = models.ImageFolder(name=folder_name, enabled=enabled, config_as_json=folder_config["optiimage"])
                    global_config.image_folder_list.append(folder_name)
                elif type_ == "video":
                    folder_name = models.VideoFolder(name=folder_name, enabled=enabled, config_as_json=folder_config["optivideo"])
                    global_config.video_folder_list.append(folder_name)
                else:
                    raise TypeError("{} unknown.".format(type_))
            except Exception:
                logging.debug("folder_config: {}".format(folder_config))
                # Forward current stack trace
                raise

    return global_config




