import bibtexparser
import re
import sys

from bibtexparser.middlewares import BlockMiddleware


class FormatterMiddleware(BlockMiddleware):
    booktitle_regex_to_formatted_name = [
        [r"symposium on cloud computing", "Proc. of ACM SoCC"],
        [r"annual technical conference", "Proc. of USENIX ATC"],
    ]

    def transform_entry(self, entry, *args, **kwargs):
        if "booktitle" in entry:
            entry["booktitle"] = self.transform_booktitle(entry["booktitle"])
        return entry

    def transform_booktitle(self, n):
        for regex, formatted_name in self.booktitle_regex_to_formatted_name:
            if re.search(regex, n, flags=re.IGNORECASE):
                return formatted_name
        return n


def format(input_file, output_file):
    layers = [
        FormatterMiddleware(),
    ]

    library = bibtexparser.parse_file(input_file, append_middleware=layers)
    bibtexparser.write_file(output_file, library)


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    format(input_file, output_file)
