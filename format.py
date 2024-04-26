import bibtexparser
import sys


def format(input_file):
    library = bibtexparser.parse_file(input_file)


if __name__ == "__main__":
    input_file = sys.argv[1]
    format(input_file)
