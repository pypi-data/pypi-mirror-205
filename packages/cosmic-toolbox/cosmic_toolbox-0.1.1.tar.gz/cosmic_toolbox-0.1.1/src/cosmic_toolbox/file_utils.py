# Copyright (C) 2017 ETH Zurich
# Cosmology Research Group
# Author: Joerg Herbel


import os
import shutil
import subprocess
import shlex
import pickle
import yaml
from cosmic_toolbox.logger import get_logger


LOGGER = get_logger(__file__)


def robust_remove(path):
    if is_remote(path):
        LOGGER.info("Removing remote directory {}".format(path))
        host, path = path.split(":")
        cmd = 'ssh {} "rm -rf {}"'.format(host, path)
        subprocess.call(shlex.split(cmd))

    else:
        if os.path.isfile(path):
            os.remove(path)

        elif os.path.isdir(path):
            shutil.rmtree(path)

        else:
            LOGGER.info(f"Cannot remove {path} because it does not exist")


def write_to_pickle(filepath, obj, compression="none"):
    if compression.lower() == "none":
        with open(filepath, "wb") as f:
            pickle.dump(obj, f)
    elif compression.lower() == "lzf":
        import lzf

        with lzf.open(filepath, "wb") as f:
            pickle.dump(obj, f)
    elif compression.lower() == "bz2":
        import bz2

        with bz2.open(filepath, "wb") as f:
            pickle.dump(obj, f)

    else:
        raise Exception(f"uknown compression {compression} [none, lzf, bz2]")


def read_from_pickle(filepath, compression="none"):
    if compression.lower() == "none":
        with open(filepath, "rb") as f:
            obj = pickle.load(f)
    elif compression.lower() == "lzf":
        import lzf

        with lzf.open(filepath, "rb") as f:
            obj = pickle.load(f)
    elif compression.lower() == "bz2":
        import bz2

        with bz2.open(filepath, "rb") as f:
            obj = pickle.load(f)

    else:
        raise Exception(f"uknown compression {compression} [none, lzf, bz2]")

    return obj


def get_abs_path(path):
    if "@" in path and ":/" in path:
        abs_path = path

    elif os.path.isabs(path):
        abs_path = path

    else:
        if "SUBMIT_DIR" in os.environ:
            parent = os.environ["SUBMIT_DIR"]
        else:
            parent = os.getcwd()

        abs_path = os.path.join(parent, path)

    return abs_path


def robust_makedirs(path):
    if is_remote(path):
        LOGGER.info("Creating remote directory {}".format(path))
        host, path = path.split(":")
        cmd = 'ssh {} "mkdir -p {}"'.format(host, path)
        subprocess.call(shlex.split(cmd))

    elif not os.path.isdir(path):
        os.makedirs(path)
        LOGGER.info("Created directory {}".format(path))


def robust_copy(
    src,
    dst,
    n_max_connect=10,
    n_max_attempts_remote=10,
    time_between_attempts=10,
    method="CopyGuardian",
    **kwargs,
):
    from . import copy_guardian

    # In case of a remote destination, rsync will create the directory itself
    if not is_remote(dst):
        robust_makedirs(os.path.dirname(dst))

    if method == "CopyGuardian":
        copy_guard = copy_guardian.CopyGuardian(
            n_max_connect,
            n_max_attempts_remote,
            time_between_attempts,
            **kwargs,
        )
        copy_guard(src, dst)

    # elif method == 'system_cp':

    #    system_copy(sources=src, dest=dst, **kwargs)

    else:
        raise Exception(f"Unknown copy method {method}")


def is_remote(path):
    return "@" in path and ":/" in path


def read_yaml(filename):
    with open(filename) as f:
        file = yaml.load(f, Loader=yaml.Loader)
    return file
