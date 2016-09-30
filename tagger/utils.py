import os.path


def check_file(filename):
    return os.path.isfile(os.path.join(os.getcwd(), filename))
