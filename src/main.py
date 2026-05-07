import sys
import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    if os.path.exists("public"):
        shutil.rmtree("public")

    copy_files_recursive("static", "public")
    generate_pages_recursive("content", "template.html", "public", basepath)


if __name__ == "__main__":
    main()
