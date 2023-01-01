import argparse
import contextlib
import os
import sys

from .render import render

def main():
    parser = argparse.ArgumentParser(prog="madore",
                                     description="python-enhanced markdown reports")

    parser.add_argument("file",
                        type=argparse.FileType("r"),
                        help="the file to render")

    parser.add_argument("-o", "--output",
                        default="-",
                        nargs="?",
                        help="file to render result into")

    parser.add_argument("--style",
                        type=argparse.FileType("r"),
                        help="css file to include")

    args = parser.parse_args()

    with args.file as f:
        text = f.read()

    options = {}
    if args.style:
        with args.style as f:
            options["style"] = f.read()

    # callers of the exeutable expect paths, including the module search path,
    # to be relative to the input file's directory
    wd = os.path.abspath(os.path.dirname(args.file.name))

    with change_dir_and_module_path(wd):
        result = render(text, **options)

    with open(args.output, "w") if args.output != "-" else sys.stdout as f:
        f.write(result)


@contextlib.contextmanager
def change_dir_and_module_path(d):
    old_path = sys.path[0]
    old_wd = os.getcwd()
    sys.path[0] = d
    os.chdir(d)
    yield
    sys.path[0] = old_path
    os.chdir(old_wd)
