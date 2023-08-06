# Copyright (C) 2023 twyleg
import argparse
import os.path
import sys

from pathlib import Path
from ausbildungsnachweise_utils import processor

FILE_DIR = Path().absolute()
INPUT_DIR = "resources"


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)

    args = parser.parse_args()

    create_documents(args.input_file) if exist(args.input_file) else sys.exit("file does not exist")


def exist(input_file):
    path = os.path.join(FILE_DIR, INPUT_DIR)
    for f in os.listdir(path):
        if input_file in f:
            return True
    return False


def create_documents(input_file):
    processor.fill_template(FILE_DIR / INPUT_DIR / input_file, FILE_DIR / "output/example_output.docx")

    processor.convert_docx_to_pdf(FILE_DIR / "output/example_output.docx", FILE_DIR / "output/")

    processor.sign_pdf(FILE_DIR / "output/example_output.pdf", FILE_DIR / "output/example_output_signed.pdf")


if __name__ == "__main__":
    start()
