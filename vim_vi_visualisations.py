"""Visualise the size and expression distribution of the Penitentiary corpus.

This script is written in small, clearly separated parts so that the data and
methods can be inspected and adjusted without needing advanced Python knowledge.
"""

# PART 1: Imports and source-file locations
# ----------------------------------------
# pathlib helps us describe file locations in a readable, cross-platform way.
# csv is part of Python itself, so no extra package is needed to read this file.

from pathlib import Path
import csv



# The folder containing this Python script is the project folder.
PROJECT_FOLDER = Path(__file__).resolve().parent


# Corpus-size data are kept in a separate CSV file, so the figures can be
# updated without editing the Python code.
CORPUS_SIZE_FILE = PROJECT_FOLDER / "corpus_size.csv"


# This is the existing text file that contains the attested-expression counts.
# The path is the one supplied by the researcher; it points to their local PC.
EXPRESSION_COUNTS_FILE = Path(
    r"C:\Users\Hanna-Mari\Documents\Väitöskirja\auctoritate\Results\vim_vi_rhetoric\vim_vi_rhetoric_country_expression_table.txt"
)



# PART 2: Read the corpus-size data
# -----------------------------------
# Read the CSV file into a list of dictionaries. Each dictionary represents
# one region and contains its document and word counts.
def read_corpus_size(source_file):
    """Read document and word counts from the corpus-size CSV file."""
    with source_file.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        corpus_data = []

        for row in reader:
            corpus_data.append(
                {
                    "Region": row["Region"],
                    "Documents": int(row["Documents"]),
                    "Words": int(row["Words"]),
                }
            )

    return corpus_data



# Load the corpus-size data and print it as a simple check that the file was
# found and read correctly. Later parts of the script will use this data to draw.
corpus_size = read_corpus_size(CORPUS_SIZE_FILE)


print("Corpus size data loaded:")
for region in corpus_size:
    print(
        f"{region['Region']}: {region['Documents']:,} documents, "
        f"{region['Words']:,} words"
    )
