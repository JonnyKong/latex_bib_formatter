# bib_formatter

Formats the given latex bib file by:

* Rename the citation key to the following grammar:

    ```ebnf
    CITATION_KEY ::= PAPER_NAME ':' CONFERENCE_NAME [YEAR]

    PAPER_NAME ::= SYSTEM_NAME_IF_SYSTEMS_PAPER
                | FIRST_WORD_OF_TITLE

    CONFERENCE_NAME ::= 'ACM SIGCOMM'
                    | 'ACM MobiCom' 
                    | 'USENIX OSDI' 
                    ...
    ```

* Replace conference names with acronyms (see [`rules.csv`](rules.csv), append
  rows if needed)

### Getting Started

1. Import multiple `.bib` files into [JebRef](https://www.jabref.org) to remove
   duplicate entries, and export the de-duplicated `.bib` file

2. Install deps

```bash
pip install --pre bibtexparser
pip install nltk
```

3. Format the bib file:

```bash
python format.py <input_bib_file> <output_bib_file>
```