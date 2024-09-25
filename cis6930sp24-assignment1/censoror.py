from assignment1.hidestring import MaskString
import argparse
import os, sys
import glob
import spacy


def create_censored_file(output_string, file_path, out_folder_path):
    file_name = os.path.basename(file_path)
    output_file_path = os.path.join(out_folder_path, f"{file_name}.censored")

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(output_string)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Censor sensitive information from text files.')
    parser.add_argument('--input', type=str, action='append', help='Glob pattern for input text files', required=True)
    parser.add_argument('--output', type=str, help='Output directory for censored files', required=True)
    parser.add_argument('--names', action='store_true', help='Censor names', required=True)
    parser.add_argument('--dates', action='store_true', help='Censor dates', required=True)
    parser.add_argument('--phones', action='store_true', help='Censor phone numbers', required=True)
    parser.add_argument('--address', action='store_true', help='Censor addresses', required=True)
    parser.add_argument('--stats', type=str, help='File or location to write statistics (stderr, stdout, or filename)', required=True)
    return parser.parse_args()


def write_stats(stats, destination):
    if destination in ['stderr', 'stdout']:
        output = getattr(sys, destination)
        output.write(str(stats))
    else:
        if os.path.isdir(destination):
            destination = os.path.join(destination, "stats")
        with open(destination, 'w', encoding='utf-8') as file:
            file.write(str(stats))


def main():
    stats = ""
    args = parse_arguments()
    model_name = "en_core_web_md"
    spacy.cli.download(model_name)

    if not os.path.exists(args.output):
        os.makedirs(args.output)
    hide_processor = MaskString()
    for input_pattern in args.input:
        # Iterates over each glob pattern provided
        for file_path in glob.glob(input_pattern, recursive=True):
            try:
                if not os.path.isfile(file_path):
                    continue
                with open(file_path, 'r', encoding='utf-8') as file:
                    # print(file_path)
                    contents = file.read()
                    hide_processor.set_input_string(contents)
                    hidden_address = hide_processor.hide_address()
                    hidden_name = hide_processor.hide_names()
                    hidden_dates = hide_processor.hide_date()
                    hidden_phone_numbers = hide_processor.hide_phone_numbers()
                    create_censored_file(hide_processor.partially_hidden_string, file_path, args.output)
                    stats += f"""{'*'*25} Stats for file : {os.path.basename(file_path)} {"*"*25}\n""" +\
                             f"""Censored Name count: {hidden_name}\n"""\
                             f"""Censored Address count : {hidden_address}\n"""\
                             f"""Censored Date count: {hidden_dates}\n"""\
                             f"""Censored Phone numbers: {hidden_phone_numbers}\n"""

            except Exception as e:
                stats += f""""{'*'*25} Stats for file : {os.path.basename(file_path)} {"*"*25}\n"""\
                         f"""Process file failed with  error :{e}\n"""
    write_stats(stats, args.stats)


if __name__ == '__main__':
    main()
