import os
import platform
import yaml
import sys

def read_config(config_path):
    if not os.path.exists(config_path):
        print(f"Fatal: Config File ({config_path}) does not exist")
        sys.exit(1)
    yaml_versions = yaml.__version__.split(".")
    major = int(yaml_versions[0])
    minor = int(yaml_versions[1])
    use_full_load_syntax = False
    if major == 5 and minor > 1:
        use_full_load_syntax = True
    if major >= 6:
        use_full_load_syntax = True

    with open(config_path) as fh:
        if use_full_load_syntax:
            config = yaml.load(fh, Loader=yaml.FullLoader)
        else:
            config = yaml.load(fh)

    return config

# def find_tmp_path():
#     system_val = platform.system()

#     if system_val == 'Linux' or sytem_val == :
#         return '/tmp/'