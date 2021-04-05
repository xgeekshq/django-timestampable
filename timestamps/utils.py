from distutils.util import strtobool


def str2bool(value: str = 0) -> bool:
    if value is None:
        return False

    try:
        return strtobool(value) == 1
    except ValueError:
        return False
