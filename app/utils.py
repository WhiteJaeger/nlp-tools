from os import path, listdir, remove

import random
import string


def generate_salt() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def purge_old_files(dir_with_files: str):
    old_files = listdir(dir_with_files)
    if len(old_files) > 20:
        for old_file in old_files:
            remove(path.join(dir_with_files, old_file))
