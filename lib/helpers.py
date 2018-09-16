import os


def create_abs_path(file, relative):
    file_dir = os.path.dirname(file)
    rel_path = os.path.join(file_dir, relative)
    return os.path.abspath(rel_path)
