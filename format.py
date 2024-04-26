import re
import sys
from string import punctuation

import bibtexparser
import nltk
import pandas as pd

nltk.download("stopwords")
from bibtexparser.library import Library
from bibtexparser.middlewares import BlockMiddleware, LibraryMiddleware
from bibtexparser.model import ParsingFailedBlock
from nltk.corpus import stopwords


class FormatterBlockMiddleware(BlockMiddleware):
    def __init__(self, rules_file):
        self.rules = pd.read_csv(rules_file).values.tolist()
        self.stopwords = set(stopwords.words("english"))
        super().__init__()

    def transform_entry(self, entry, *args, **kwargs):
        if entry.entry_type in ["inproceedings", "article", "conference"]:
            if "booktitle" in entry:
                entry["booktitle"] = self.transform_booktitle(entry["booktitle"])
            elif "journal" in entry:
                entry["journal"] = self.transform_booktitle(entry["journal"])
            entry.key = self.synthesize_key(entry)

        return entry

    def transform_booktitle(self, n):
        for regex, formatted_name in self.rules:
            if re.search(regex, n, flags=re.IGNORECASE):
                return f"Proc. of {formatted_name}"
        return n

    def synthesize_key(self, entry):
        # title
        title = [w.lower().strip("{}") for w in entry["title"].split(" ")]
        title = [w for w in title if w not in self.stopwords]
        title_part = title[0].lower().strip(punctuation)
        title_part = re.sub(r"[^\w\s]", "", title_part)

        # booktitle
        if self.is_arxiv(entry):
            booktitle_part = "Arxiv"
        else:
            # Assumes last word is the conference acronym
            if "booktitle" in entry:
                booktitle_part = entry["booktitle"].split(" ")[-1].capitalize()
            elif "journal" in entry:
                booktitle_part = entry["journal"].split(" ")[-1].capitalize()
            else:
                booktitle_part = ""

        # year
        year_part = entry["year"] if "year" in entry else ""

        key = f"{title_part}{booktitle_part}{year_part}"
        return key

    def is_arxiv(self, entry):
        fields_to_search = ["booktitle", "journal", "publisher"]
        for f in fields_to_search:
            if f in entry and "arxiv" in entry[f].lower():
                return True
        return False


class RemoveFailedBlocksLibraryMiddleware(LibraryMiddleware):
    def transform(self, library):
        library = Library(
            blocks=[b for b in library._blocks if not isinstance(b, ParsingFailedBlock)]
        )
        return library


def format(input_file, output_file):
    library = bibtexparser.parse_file(
        input_file,
        append_middleware=[FormatterBlockMiddleware("rules.csv")],
    )
    bibtexparser.write_file(
        output_file,
        library,
        append_middleware=[RemoveFailedBlocksLibraryMiddleware()],
    )


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    format(input_file, output_file)
