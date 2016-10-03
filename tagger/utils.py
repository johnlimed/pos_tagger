import os.path
import json


def check_file(filename):
    return os.path.isfile(os.path.join(os.getcwd(), filename))


def write_out_file(to_write_out, outfile_name):
    with open(outfile_name, 'w') as outfile:
        json.dump(to_write_out, outfile, indent=4)


def read_file(in_filename):
    data = open(in_filename).read()
    return json.loads(data)
