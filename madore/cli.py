import argparse

from .render import render

def main():
    parser = argparse.ArgumentParser(prog="madore",
                                     description="python-enhanced markdown reports")

    parser.add_argument("file",
                        type=argparse.FileType("r"),
                        help="the file to render")

    parser.add_argument("-o", "--output",
                        type=argparse.FileType("w"),
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

    result = render(text, **options)

    with args.output as f:
        f.write(result)
