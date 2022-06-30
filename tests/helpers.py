import os

from geocluster.io import read_csv_file


def get_fixture_path(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, "fixtures", filename)


def read_fixture_csv(filename):
    return read_csv_file(get_fixture_path(filename))


def read_fixture_content(filename):
    with open(get_fixture_path(filename)) as f:
        return f.read()
