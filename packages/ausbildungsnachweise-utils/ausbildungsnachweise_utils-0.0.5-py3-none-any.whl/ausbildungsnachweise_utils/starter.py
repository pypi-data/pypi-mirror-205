# Copyright (C) 2023 twyleg

import glob
import os.path

from pathlib import Path
from ausbildungsnachweise_utils import processor

FILE_DIR = Path().absolute()
INPUT_DIR = "resources"
OUTPUT_DIR = "output"


def start():
    input_files = [f.split("/")[-1] for f in glob.glob(os.path.join(FILE_DIR, INPUT_DIR) + '/*.xml')]
    output_files = [f.split("/")[-1] for f in glob.glob(os.path.join(FILE_DIR, OUTPUT_DIR) + '/*.pdf')]

    for i in input_files:
        exist = False
        for o in output_files:
            if i.split(".")[0] == o.split(".")[0]:
                compare_m_time(i, o)
                exist = True
                break

        if not exist:
            create_documents(i, set_file_extensions(i))


def compare_m_time(input_file, output_file):
    input_file_path = os.path.join(FILE_DIR, INPUT_DIR, input_file)
    output_file_path = os.path.join(FILE_DIR, OUTPUT_DIR, output_file)

    if os.path.getmtime(input_file_path) > os.path.getmtime(output_file_path):
        create_documents(input_file, set_file_extensions(input_file))


def set_file_extensions(input_file):
    output_file = input_file.split(".")[0]
    file_names = (output_file + '.docx', output_file + '.pdf', output_file + '_signed.pdf')
    return file_names


def create_documents(input_file, output_files):
    processor.fill_template(FILE_DIR / INPUT_DIR / input_file, FILE_DIR / OUTPUT_DIR / output_files[0])

    processor.convert_docx_to_pdf(FILE_DIR / OUTPUT_DIR / output_files[0], FILE_DIR / str(OUTPUT_DIR + '/'))

    processor.sign_pdf(FILE_DIR / OUTPUT_DIR / output_files[1], FILE_DIR / OUTPUT_DIR / output_files[2])


if __name__ == "__main__":
    start()
