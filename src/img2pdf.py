# Copyright (c) 2025 haogu2025@gmail.com
# pdfunite $(ls page_*.pdf | sort -V) merged.pdf
from argparse import ArgumentParser
import glob
from pathlib import Path

from PIL import Image


def img2pdf(folder):
    for image in glob.glob(f"{folder}/*.jpg"):
        im = Image.open(image).convert('RGB')
        im.thumbnail((2732, 2048), Image.LANCZOS)
        im.save(Path(image).with_suffix(".pdf"))


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("folder", nargs="?", default=".")
    args = parser.parse_args()
    img2pdf(args.folder)


if __name__ == "__main__":
    main()
