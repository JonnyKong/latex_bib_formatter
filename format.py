import bibtexparser
from string import punctuation
import re
import sys
import pandas as pd

from bibtexparser.middlewares import BlockMiddleware


class FormatterMiddleware(BlockMiddleware):
    def __init__(self, rules_file):
        self.rules = pd.read_csv(rules_file).values.tolist()
        super().__init__()

    def transform_entry(self, entry, *args, **kwargs):
        if entry.entry_type == "inproceedings":
            if "booktitle" in entry:
                entry["booktitle"] = self.transform_booktitle(entry["booktitle"])
            elif "journal" in entry:
                entry["journal"] = self.transform_booktitle(entry["journal"])
            else:
                raise NotImplementedError()
            entry.key = self.synthesize_key(entry)

        return entry

    def transform_booktitle(self, n):
        for regex, formatted_name in self.rules:
            if re.search(regex, n, flags=re.IGNORECASE):
                return f"Proc. of {formatted_name}"
        return n

    def synthesize_key(self, entry):
        title_part = entry["title"].split(" ")[0].lower().strip(punctuation)

        if "booktitle" in entry:
            booktitle_part = entry["booktitle"].split(" ")[-1].capitalize()
        elif "journal" in entry:
            booktitle_part = entry["journal"].split(" ")[-1].capitalize()
        else:
            raise NotImplementedError()

        year_part = entry["year"] if "year" in entry else ""

        key = f"{title_part}{booktitle_part}{year_part}"
        return key


def format(input_file, output_file):
    layers = [
        FormatterMiddleware("rules.csv"),
    ]

    library = bibtexparser.parse_file(input_file, append_middleware=layers)
    bibtexparser.write_file(output_file, library)


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    format(input_file, output_file)
