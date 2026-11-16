# Assessment card session — November 16, 2026

## GitHub synchronization

- Checked local `main` against GitHub: both initially pointed to `f5c3b79`.
- Found two modified tracked files and 91 untracked files.
- At the user's request, committed and pushed all 93 files as `eca6301` (`Add assessment cards and dissertation output artifacts`). The working tree was clean immediately after that push.
- The notebook, CSV, and card revisions below were made after that push; they have not been committed or pushed during this session.

## Dataset and examples

The full assessment dataset is `results/chpt6-results.csv`:

- 271 publications total.
- 191 at risk (70.5%).
- 80 not at risk (29.5%).

The current five examples are:

| Citation label | DOI | Verdict |
| --- | --- | --- |
| Liu et al. (2020) | 10.1002/chir.23189 | not at risk |
| Jonas et al. (2022) | 10.1002/mrc.5234 | not at risk |
| Lomas (2014) | 10.1002/mrc.4130 | not at risk |
| Matsuo et al. (2017) | 10.1002/anie.201706532 | at risk |
| Kim et al. (2020) | 10.1007/s12272-020-01277-4 | not at risk |

Earlier runs had left additional card images in the output folder; the five-row manifest identifies the current example selection.

## User feedback and agreed decisions

1. The Lomas card displayed the raw internal tag `lomas_2014_<sup>1</sup>`. Readable publication labels should resemble APA narrative citations instead.
2. Use the metadata's existing `Publication Year` column rather than extracting a year by splitting `Date`. Dates have mixed formats, including `11/13/17`.
3. Add a separate `citation_label` column. DOI remains the stable publication identifier; the existing internal `tag` remains separate.
4. Citation labels use one surname for a single author, both surnames joined with “and” for two authors, and first surname plus “et al.” for three or more authors.
5. Do not expand ambiguous author groups or add year suffixes such as `2020a`: the user explained that cards will be read individually.
6. Every justification must retain the DOI because the message may also be read independently. Example opening: “Lomas (2014) (DOI: 10.1002/mrc.4130) is judged…” The DOI also remains in the header.
7. Change “Final verdict” to “Verdict”.
8. Add a blank line between separate justifications to improve readability.
9. Capitalize the heading as “Reasoning Visualization”.

## Changes completed

### Notebook and CSV

Updated `scripts/prototype-chpt6.ipynb` to:

- Merge `Publication Year` alongside DOI, Author, Title, and Date.
- Use `Publication Year` for the year in tags and citation labels.
- Generate `citation_label` independently of the internal tag.
- Use `{citation_label} (DOI: {DOI})` at the start of all four justification templates, removing the leading “Publication”.

Executed the notebook's code cells with the project's `.venv/bin/python` and regenerated `results/chpt6-results.csv`. The system Python did not have pandas, but the project environment did.

Verified that all 271 DOIs remain unique, all citation labels are present, every message starts with its citation label and DOI, and all assessment flags and verdicts match the previous CSV. Counts remain 191 at risk and 80 not at risk.

### Card generator and outputs

Updated `scripts/generate_assessment_cards.py` with the readable-label fallback, the “Verdict” heading, explicit blank-line spacing between messages, and “Reasoning Visualization” capitalization.

Regenerated the five cards after each requested change. Visually checked the Lomas card and the Kim card, including the separation between Kim's two justifications.

The user deleted the cards because they were difficult to locate. Regenerated them and created clearly named PNG copies in `output/five-assessment-examples`:

- `01-Liu-et-al-2020.png`
- `02-Jonas-et-al-2022.png`
- `03-Lomas-2014.png`
- `04-Matsuo-et-al-2017.png`
- `05-Kim-et-al-2020.png`

The DOI-named PNGs, LaTeX source files, and five-row manifest are in `output/assessment-cards`.

## Regeneration

From the repository root, run:

```sh
python3 scripts/generate_assessment_cards.py
```

This regenerates the default five examples in `output/assessment-cards`; it does not automatically refresh the separately named copies in `output/five-assessment-examples`. Those copies were refreshed manually during this session.

The generator requires `pdflatex` and `pdftoppm`. Regenerating the CSV requires running the notebook with the project Python environment, with notebook-relative paths resolved from `scripts`.
