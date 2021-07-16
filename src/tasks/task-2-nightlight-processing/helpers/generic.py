import os
import shutil
from datetime import datetime


def create_directory(path):
    """Create a directory if it does not exists yet"""
    try:
        os.mkdir(path)
    except OSError as err:
        print("warning: {}".format(err))

    return path


def print_start_time(func):
    """Print start time of process"""
    print_wrapper()
    start = datetime.now()
    print("start: {}: {}".format(func, start))
    print_wrapper()
    return start


def print_wrapper():
    """Print dash line"""
    print("{}".format("-" * 70))


def print_end_time(func, start):
    """Print run time of process"""
    print_wrapper()
    end = datetime.now() - start
    print("end: {}: {}".format(func, end))
    print_wrapper()


def remove_directory(path):
    """Remove directory"""
    try:
        shutil.rmtree(path, ignore_errors=True)
    except OSError as err:
        print("warning: {}".format(err))


def validate_file(file):
    """Assert file exist and is a file"""
    assert os.path.exists(file) and os.path.isfile(file)
