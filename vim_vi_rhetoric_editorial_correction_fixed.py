# November 6 - 2026

# TIAS seminar on rhetoric 

# we need to find the use cases of vim ... vi ... and ... specifically vim vi repellendo even with spelling mistakes, that means some of the letter might be doubled etc.
# we need to reject cases where there only occurs vim and some other verb

# suggestion as regex but the "repellendo" might be missing completely
# vimvi = r"[.][^.]*vim\svi\srepp?ellendo.*?\."

# the findings have to be assigned the correct new file with xml structure or just plain text?
# the object is to have a clear listing and also statistics

# the listings include a target output that has

# name of collection where the expression was found i.e. country of origin
# the number of the document where it was found
# the sentence where it was found in its entireness
# 

# actual attested findings should actually be made into a .md file for easy sharing with conference participants
# all the attested findings should be printed with bold

# statistics could be printed into a simple text file

# descriptive statistics should contain

# counts of the entire expression found as "vim vi repellendo" per document, in columns info about country of origin

# e.g. just to showcase:

# expression in full    England     Sweden 
# vim vi repellendo     13          55

# vim vi                    document 33, england
# vim vi reppelendo         document 2, sweden
# vim vi puerum repelendo 

# counts of deviations of the expression as well as partial use, document in columns

# a listing of the partial uses with document number after it

# take the correct xml files with the following paths:

# Norway
# "C:\Users\Hanna-Mari\Documents\Väitöskirja\Norway\Data\Norway_data.xml"

# Sweden
# "C:\Users\Hanna-Mari\Documents\Väitöskirja\auctoritate\Data\auctoritate_teksti.xml"


# England and Wales
# "C:\Users\Hanna-Mari\Documents\Väitöskirja\EnglandWales\Data\England_Wales_1_data.xml"

# "C:\Users\Hanna-Mari\Documents\Väitöskirja\EnglandWales\Data\England_Wales_2_data.xml"

# "C:\Users\Hanna-Mari\Documents\Väitöskirja\EnglandWales\Data\England_Wales_3_data.xml"

# the output files, ie. markdown and text and xml? should be printed in C:\Users\Hanna-Mari\Documents\Väitöskirja\auctoritate\Results with new folder name "vim_vi_rhetoric" and add this to all the results files as well as an identifier

# =============================================================================
# vim_vi_rhetoric — executable corpus search and reporting code
# Project identifier: vim_vi_rhetoric
#
# IMPORTANT:
# * This script reads the five source XML files but never edits them.
# * Search is case-insensitive.
# * Editorial ">" marks are tolerated inside the expression.
# * Sentence-initial "Vim ..." is allowed.
# * Full, variant, extended, and partial uses are reported separately.
# * XML schemas differ; document/sentence extraction below is deliberately
#   generic. Review the extraction settings after the first test run.
# =============================================================================


# Postpone the evaluation of type annotations.
# This can make it easier to refer to classes or types that are
# defined later in the code, and can be useful for type hints.
from __future__ import annotations

# Regular expressions: tools for searching, matching, and manipulating text
# according to patterns. Useful for linguistic data and text cleaning.
import re

# System-related functionality, such as command-line arguments,
# program exit, and interaction with the Python runtime.
import sys

# Tools for reading and writing CSV files.
# CSV is a common format for tables that can be opened in Excel,
# LibreOffice, and other spreadsheet programs.
import csv
import copy

# Tools for escaping and unescaping HTML characters.
# Useful when text contains characters such as <, >, or &.
import html

# Provides information about errors and their tracebacks.
# Useful for diagnosing problems when something goes wrong.
import traceback

# Counter: counts how often items occur.
# defaultdict: a dictionary that can automatically create a default
# value for a missing key.
from collections import Counter, defaultdict

# dataclass: a convenient way to create classes primarily used
# for storing structured data, without writing as much boilerplate.
from dataclasses import dataclass

# Path: a convenient, cross-platform way of working with file
# and folder paths.
from pathlib import Path

# Optional: indicates that a value may either contain an object
# of a specified type or be None (no value).
from typing import Optional

# ElementTree: tools for reading, navigating, and processing XML.
# XML is a structured format often used for dictionaries,
# corpora, archives, and historical or linguistic datasets.
import xml.etree.ElementTree as ET




# A short identifier for this analysis/project.
# Used to distinguish its output from the results of other projects.
PROJECT_ID = "vim_vi_rhetoric"

# Main folder containing the research data and project folders.
# Change this path if the project is stored somewhere else
# (for example, on another computer).
BASE_DIR = Path(r"C:\Users\Hanna-Mari\Documents\Väitöskirja")

# Folder where the results of this project will be stored.
# The path is built from BASE_DIR and the subfolder names.
# This line defines the path; it does not create the folder.
RESULT_DIR = BASE_DIR / "auctoritate" / "Results" / PROJECT_ID

# List of XML files to be processed.
# Each entry contains three values:
#   1. A broader source group (e.g. country or region)
#   2. A source identifier (used to distinguish individual datasets)
#   3. The path to the XML file
#
# The first two values are labels. Their exact function depends
# on how they are used later in the program.
SOURCES = [
    # Norway: one source file
    ("Norway", "Norway",
     BASE_DIR / "Norway" / "Data" / "Norway_data.xml"),

    # Sweden: one source file
    ("Sweden", "auctoritate",
     BASE_DIR / "auctoritate" / "Data" / "auctoritate_teksti.xml"),

    # England and Wales: the data is divided into three files.
    # Each file has its own identifier but belongs to the same
    # broader source group.
    ("England and Wales", "England_Wales_1",
     BASE_DIR / "EnglandWales" / "Data" / "England_Wales_1_data.xml"),

    ("England and Wales", "England_Wales_2",
     BASE_DIR / "EnglandWales" / "Data" / "England_Wales_2_data.xml"),

    ("England and Wales", "England_Wales_3",
     BASE_DIR / "EnglandWales" / "Data" / "England_Wales_3_data.xml"),
]


# Tune these only if inspection of your XML shows different document tags.
DOCUMENT_TAGS = {
    "doc", "document", "text", "work", "item", "record"
}

# Common sentence/paragraph tags. If none are present, text is split by punctuation.
SENTENCE_TAGS = {"s", "sentence"}
PARAGRAPH_TAGS = {"p", "para", "paragraph"}

## editorial comments should not be a part of the analysis
def exclude_editorial_corrections(text: str) -> str:
    """
    Exclude editorial corrections marked by [recte ...]
    from the text used for searching.

    Spaces replace the editorial material so that character
    positions remain unchanged.
    """
    return re.sub(
        r"\[\s*recte\b[^\]]*\]",
        lambda match: " " * len(match.group()),
        text,
        flags=re.IGNORECASE
    )

# Characters that may appear between the core words of the expression.
# These include whitespace, certain brackets, editorial symbols,
# and punctuation. The * means that zero or more such characters
# are allowed.
#
# This does NOT allow arbitrary words or full XML tags between
# the search terms.
EDITORIAL_GAP = r"(?:\s|>|\[|\]|\(|\)|\{|\}|[.,;:!?—–-])*"

# A pattern for matching sequences of letters (without digits or underscores).
# Currently, check whether this is used elsewhere in the program.
WORD = r"[^\W\d_]+"

# Finds "vim" followed by "vi", allowing the characters defined
# in EDITORIAL_GAP between them.
# Capitalization is ignored.
VIM_VI_RE = re.compile(
    rf"\bvim\b{EDITORIAL_GAP}\bvi\b",
    flags=re.IGNORECASE
)

# Finds candidate participle-like forms.
# Allows:
#   - r followed by one or more e's
#   - one or two p's
#   - an optional e
#   - one or two l's
#   - optional e or a after the l-sequence, then optional n, d, and o
#
# This is intentionally broad. A match is a candidate for human
# review, not proof of a correct linguistic form.
PARTICIPLE_RE = re.compile(
    r"\bre+p{1,2}e?l{1,2}[ea]?n?d?o?\b",
    flags=re.IGNORECASE
)

# Finds the combined expression: "vim" + "vi" + a participle-like form.
# The elements must occur in this order, with only the allowed
# whitespace/punctuation/editorial characters between them.
# Unlike PARTICIPLE_RE, the final "o" is required here.
FULL_RE = re.compile(
    rf"\bvim\b{EDITORIAL_GAP}\bvi\b{EDITORIAL_GAP}"
    rf"\bre+p{{1,2}}e?l{{1,2}}[ea]?n?d?o\b",
    flags=re.IGNORECASE
)



# A template for storing one search finding.
# Each finding will contain the text that was found and information
# about where it came from, so that the results can be checked later.
@dataclass
class Finding:

    # A unique identifier for this finding (e.g. "F0001").
    finding_id: str

    # The country or geographical group the source belongs to.
    country: str

    # The name of the corpus, collection, or dataset.
    collection: str

    # The name or path of the original source file.
    source_file: str

    # The identifier or name of the document in which the finding occurs.
    document: str

    # The sentence or passage containing the finding.
    sentence: str

    # The exact text that matched the search pattern.
    matched_text: str

    # Classification of the finding.
    # Possible labels used by the program:
    # full_exact, full_variant, extended, partial
    category: str

    # Classification of the spelling.
    # Possible labels: exact, variant, not_applicable
    spelling: str

    # An optional note about the finding.
    # If no note is provided, this field is left empty.
    note: str = ""


def normalize_expression(text: str) -> str:
    """
    Clean a text expression to make comparisons and variant counting
    more consistent.

    This function:
    1. Converts all letters to lowercase.
    2. Removes certain editorial symbols and brackets.
    3. Replaces repeated spaces or line breaks with one space.
    4. Removes whitespace from the beginning and end.

    The cleaned text is returned. The original text should be
    preserved separately for research and verification.
    """

    # Make capitalization consistent (e.g. "VIM" becomes "vim").
    text = text.lower()

    # Remove selected editorial and bracket characters.
    # The characters inside brackets are deleted, not replaced by spaces.
    text = re.sub(r"[>\[\]{}()]", "", text)

    # Replace multiple spaces, tabs, or line breaks with a single space.
    text = re.sub(r"\s+", " ", text)

    # Remove spaces from the beginning and end, then return the cleaned text.
    return text.strip()



def expression_profile(findings: list[Finding]) -> Counter:
    """
    Count how many times each normalized expression occurs
    in the collected findings.

    Differences in capitalization, spacing, and selected editorial
    marks are removed before counting, using normalize_expression().

    Returns a counter containing each expression and its frequency.
    """

    # Start with an empty counter for the expression frequencies.
    counts = Counter()

    # Examine each finding in the collected results, one at a time.
    for finding in findings:

        # Clean the matched expression so that superficial differences
        # (such as capitalization or spacing) do not create separate
        # counts. Then increase its frequency by one.
        counts[normalize_expression(finding.matched_text)] += 1

    # Return the completed frequency counts to the calling code.
    return counts

def write_variant_report(findings: list[Finding]) -> None:

    counts = expression_profile(findings)

    lines = [
        f"{PROJECT_ID} — VARIANT REPORT",
        "=" * 60,
        ""
    ]

    for expr, n in counts.most_common():

        lines.append(f"{n:5d}  {expr}")

    (RESULT_DIR / f"{PROJECT_ID}_variants.txt").write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

def write_country_table(findings: list[Finding]) -> None:
    # Create an empty counting table.
    # It will store each expression and how many times it occurs
    # in each country.
    table = defaultdict(Counter)

    # Go through every finding identified during the analysis.
    # Each finding represents one identified occurrence.
    for f in findings:

        # Standardise the expression so that equivalent expressions
        # are grouped together rather than treated as different entries.
        key = normalize_expression(f.matched_text)

        # Add one occurrence to the count for this expression
        # in the country where the finding was identified.
        table[key][f.country] += 1

    # Define the countries that will appear as columns in the output table.
    # This also determines their display order.
    countries = ["Norway", "Sweden", "England and Wales"]

    # Prepare an empty list to collect the lines of the output file.
    lines = []

    # Create the column headings:
    # "Expression" for the expressions being counted,
    # followed by one column for each country.
    # The spacing keeps the columns visually aligned.
    header = (
        f"{'Expression':<45}"
        + "".join(f"{c:<20}" for c in countries)
    )

    # Add the column headings as the first line of the output.
    lines.append(header)

    # Add a separator line underneath the headings for readability.
    lines.append("-" * len(header))

    # Go through the expressions in alphabetical order
    # so that the final table is easier to read and compare.
    for expr in sorted(table):

        # Start a new row with the expression in the first column.
        row = f"{expr:<45}"

        # Fill in the count for each country.
        # If an expression has no occurrences in a country,
        # its count will be 0.
        for country in countries:
            row += f"{table[expr][country]:<20}"

        # Add the completed row to the list of output lines.
        lines.append(row)

    # Write all the collected lines into a text file.
    # Each item in "lines" becomes a separate line in the file.
    # The file is saved in the results folder, using the project ID
    # as part of its filename.
    (RESULT_DIR / f"{PROJECT_ID}_country_expression_table.txt").write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

def local_name(tag: str) -> str:
    # Extract the readable name of an XML tag, removing any namespace
    # information if one is present.
    # Convert the name to lowercase so that it is treated consistently.
    """Return an XML tag name without namespace."""
    return tag.rsplit("}", 1)[-1].lower() if "}" in tag else tag.lower()

# the logic could also be written as a conventional if else statement
#if "}" in tag:
#    return tag.rsplit("}", 1)[-1].lower()
#else:
#    return tag.lower()

def element_text(element: ET.Element) -> str:
    # Collect the text contained within an XML element and its descendants.
    # Combine the text fragments with spaces to make the result readable.
    """Collect descendant text, retaining readable spaces between XML nodes."""

    # Create an empty list to store the text fragments as they are found.
    pieces = []

    # Go through the given XML element and all elements nested inside it.
    for item in element.iter():

        # If the current element contains text before its child elements,
        # add that text to the collection.
        if item.text:
            pieces.append(item.text)

        # If text appears after the current element or after a child element
        # within the XML structure, add that text as well.
        if item.tail:
            pieces.append(item.tail)

    # Combine all collected text fragments into one string,
    # inserting a space between fragments to improve readability.
    return " ".join(pieces)


def get_attr(element: ET.Element, names: tuple[str, ...]) -> Optional[str]:
    # Look for a specific attribute in an XML element.
    # Return the attribute's value if a matching, non-empty value is found.
    # Otherwise, return None.
    """Get the first matching attribute, including xml:id."""

    # Go through all attributes belonging to this XML element,
    # examining each attribute name and its value.
    for key, value in element.attrib.items():

        # Remove any namespace information from the attribute name
        # and convert the remaining name to lowercase.
        # This allows names such as "xml:id" to be checked
        # by their local name, "id".
        bare = key.rsplit("}", 1)[-1].lower()

        # Check whether the attribute name matches one of the requested names
        # and whether its value contains something other than whitespace.
        if bare in names and value.strip():

            # Return the attribute value after removing leading
            # and trailing whitespace.
            return value.strip()

    # If no matching attribute with a usable value was found,
    # return None to indicate that no value is available.
    return None

def split_sentences(text: str) -> list[str]:
    # Split text into sentences using punctuation and spacing as clues.
    # This is a cautious approach rather than a full linguistic analysis.
    # Sentence-ending punctuation is kept attached to each sentence.
    # If XML already identifies sentence boundaries, those are preferred.
    """
    Conservative punctuation-based sentence split.
    Keeps the punctuation attached to each sentence. Latin abbreviations may
    occasionally cause a split; the XML sentence tags are preferred whenever
    available.
    """

    # Replace sequences of whitespace (such as multiple spaces, tabs or line breaks)
    # with a single space, and remove whitespace from the beginning and end.
    text = re.sub(r"\s+", " ", text).strip()

    # If the text is empty after cleaning, return an empty list.
    # There is no text to split into sentences.
    if not text:
        return []

    # Split the text at likely sentence boundaries.
    # A split is made when punctuation is followed by whitespace
    # and the next sentence appears to begin with an uppercase letter.
    # The punctuation remains attached to the preceding sentence.
    chunks = re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-ÖØ-Þ])", text)

    # Remove surrounding whitespace from each sentence fragment.
    # Keep only fragments that contain text, then return them as a list.
    return [chunk.strip() for chunk in chunks if chunk.strip()]

def xml_documents(root: ET.Element, country: str, source_file: str):
    """Yield (true document number, element) using dataset-aware boundaries.



    England/Wales records use <document num="...">.
    Sweden records begin at <h2 num="..."> headings; each heading's
    content extends to the next such heading among the same siblings.
    Norway may use sibling <num>75</num> metadata markers without wrapper
    elements; where these markers repeat among siblings, split at them.
    Generic wrapper detection remains a fallback for other XML formats.
    """
    def synthetic_from_siblings(siblings, start, end):
        wrapper = ET.Element("synthetic_document")
        for node in siblings[start:end]:
            wrapper.append(copy.deepcopy(node))
        return wrapper


    # Sweden: h2 headers carry the authoritative num attribute.
    if country == "Sweden":
        parent_map = {child: parent for parent in root.iter() for child in parent}
        headers = [el for el in root.iter()
                   if local_name(el.tag) == "h2" and get_attr(el, ("num",))]
        if headers:
            grouped = defaultdict(list)
            for h in headers:
                grouped[parent_map.get(h)].append(h)
            yielded = False
            for parent, parent_headers in grouped.items():
                if parent is None:
                    continue
                siblings = list(parent)
                positions = [siblings.index(h) for h in parent_headers]
                for j, h in enumerate(parent_headers):
                    start = positions[j]
                    end = positions[j + 1] if j + 1 < len(positions) else len(siblings)
                    yield (get_attr(h, ("num",)), synthetic_from_siblings(siblings, start, end))
                    yielded = True
            if yielded:
                return

    # Norway: records may either be individual siblings containing their own
    # <num> child, or a flat sequence where each <num> starts a record.
    if country == "Norway":
        for parent in root.iter():
            siblings = list(parent)
            record_children = []
            for child in siblings:
                num_child = next((sub for sub in child
                                if local_name(sub.tag) == "num" and (sub.text or "").strip()), None)
                if num_child is not None:
                    record_children.append((child, (num_child.text or "").strip()))
            if len(record_children) >= 2:
                for child, number in record_children:
                    yield (number, copy.deepcopy(child))
                return

        # Flat metadata format: <num>75</num><date>... followed by content,
        # with another <num> marking the next record.
        for parent in root.iter():
            siblings = list(parent)
            markers = [i for i, child in enumerate(siblings)
                      if local_name(child.tag) == "num" and (child.text or "").strip()]
            if len(markers) >= 2:
                for j, start in enumerate(markers):
                    end = markers[j + 1] if j + 1 < len(markers) else len(siblings)
                    number = (siblings[start].text or "").strip()
                    yield (number, synthetic_from_siblings(siblings, start, end))
                return

    # General XML wrapper formats, including England/Wales <document num="...">.
    candidates = [el for el in root.iter() if local_name(el.tag) in DOCUMENT_TAGS]
    top_candidates = []
    for el in candidates:
        if not any(el is not other and el in list(other.iter()) for other in candidates):
            top_candidates.append(el)

    if not top_candidates:
        yield ("1", root)
        return


    for index, doc in enumerate(top_candidates, start=1):
        explicit = get_attr(doc, ("num", "n", "number", "docno", "document", "id"))
        yield (explicit or str(index), doc)


def sentences_in_document(doc: ET.Element) -> list[str]:
    tagged = [
        el for el in doc.iter()
        if local_name(el.tag) in SENTENCE_TAGS
    ]
    if tagged:
        return [re.sub(r"\s+", " ", element_text(el)).strip()
                for el in tagged if element_text(el).strip()]

    paragraphs = [
        el for el in doc.iter()
        if local_name(el.tag) in PARAGRAPH_TAGS
    ]
    if paragraphs:
        result = []
        for p in paragraphs:
            result.extend(split_sentences(element_text(p)))
        return result

    return split_sentences(element_text(doc))

## Editorial corrections should not be treated as part of the attested wording.
def classify_sentence(sentence: str) -> list[tuple[str, str, str, str]]:
    """
    Identify attested vim-vi expressions.

    Editorial corrections marked [recte ...] are blanked out for searching.
    The original sentence is retained for the findings report. Because the
    correction is replaced with spaces of equal length, character positions
    in the original and search versions remain aligned.

    Returns tuples: (category, spelling, matched text, explanatory note).
    One sentence can contain multiple distinct vim-vi occurrences.
    """
    search_sentence = exclude_editorial_corrections(sentence)

    output = []
    pair_matches = list(VIM_VI_RE.finditer(search_sentence))
    if not pair_matches:
        return output

    for pair in pair_matches:
        start = pair.start()

        # Inspect a bounded window after "vi" for an attested participle.
        window_end = min(len(search_sentence), pair.end() + 100)
        window = search_sentence[pair.end():window_end]
        part = PARTICIPLE_RE.search(window)

        if part:
            between = window[:part.start()]

            # A lexical word between vi and the participle marks an extended use.
            lexical = re.findall(r"\\b[^\\W\\d_]+\\b", between, flags=re.UNICODE)
            if lexical:
                category = "extended"
                note = "Lexical material intervenes between vi and the participle."
            else:
                category = "full_variant"
                note = ""

            matched_end = pair.end() + part.end()

            # Keep the original source wording in the output, but determine
            # exactness from the correction-excluded search text.
            matched = sentence[start:matched_end]
            normalized = re.sub(
                r"[\\s>]+", " ",
                search_sentence[start:matched_end]
            ).strip().lower()
            exact = normalized == "vim vi repellendo"
            spelling = "exact" if exact and category == "full_variant" else "variant"
            if category == "full_variant" and spelling == "exact":
                category = "full_exact"

            output.append((category, spelling, matched, note))
        else:
            output.append((
                "partial", "not_applicable",
                sentence[start:pair.end()],
                "vim vi occurs without a detected attested repellendo participle."
            ))

    return output


def run_search() -> list[Finding]:
    findings: list[Finding] = []
    errors = []
    counter = 0

    for country, collection, xml_path in SOURCES:
        if not xml_path.exists():
            errors.append(f"MISSING FILE: {xml_path}")
            continue
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            for document_number, doc in xml_documents(root, country, xml_path.name):
                for sentence in sentences_in_document(doc):
                    for category, spelling, matched, note in classify_sentence(sentence):
                        counter += 1
                        findings.append(Finding(
                            finding_id=f"{PROJECT_ID}_{counter:06d}",
                            country=country,
                            collection=collection,
                            source_file=xml_path.name,
                            document=str(document_number),
                            sentence=sentence,
                            matched_text=matched,
                            category=category,
                            spelling=spelling,
                            note=note,
                        ))
        except Exception as exc:
            errors.append(f"ERROR parsing {xml_path}: {exc}")
            errors.append(traceback.format_exc())

    if errors:
        RESULT_DIR.mkdir(parents=True, exist_ok=True)
        (RESULT_DIR / f"{PROJECT_ID}_search_log.txt").write_text(
            "\n".join(errors), encoding="utf-8"
        )
    return findings



def write_markdown(findings: list[Finding]) -> None:
    # Prepare the opening text for the Markdown report.
    # The report includes the project identifier and a brief explanation
    # of what the file contains.
    out = [
        f"# {PROJECT_ID} — Attested findings",
        "",
        "Search output for manual verification. Source spelling and sentence text are retained.",
        ""
    ]

    # Define the order in which the countries will appear in the report.
    country_order = ["Norway", "Sweden", "England and Wales"]

    # Process the findings country by country, using the order defined above.
    for country in country_order:

        # Select only those findings that belong to the current country.
        selected = [f for f in findings if f.country == country]

        # If there are no findings for this country, skip it
        # and move on to the next country.
        if not selected:
            continue

        # Add a country heading to the Markdown report.
        out += [f"## {country}", ""]

        # Create a structure for grouping findings by source file
        # and document. Each new group starts with an empty list.
        groups = defaultdict(list)

        # Go through the selected findings for this country.
        for f in selected:

            # Group each finding according to its source file
            # and document identifier.
            groups[(f.source_file, f.document)].append(f)

        # Sort the groups to produce a consistent order in the report.
        # This makes the output easier to review and compare
        # between runs of the program.
        for (source_file, document), items in sorted(groups.items()):

            # Add a heading identifying the document and source file.
            out += [f"### Document {document} — {source_file}", ""]

            # Go through the individual findings belonging to this group.
            for f in items:

                # Create a display version of the sentence by adding
                # Markdown bold formatting around the core expression.
                # The original sentence is not changed.
                # The number 1 means only the first occurrence is replaced.
                highlighted = f.sentence.replace(
                    "vim vi",
                    "**vim vi**",
                    1
                )

                # Add the sentence and its finding information to the report.
                out += [
                    f"- {highlighted}",
                    f"  - Finding ID: `{f.finding_id}`",
                    f"  - Match: `{f.matched_text}`",
                    f"  - Classification: `{f.category}` ({f.spelling})",
                    ""
                ]

    # Save the completed Markdown report in the results folder.
    # The newline character separates each item in the output list.
    # UTF-8 encoding preserves special characters and historical spellings.
    (RESULT_DIR / f"{PROJECT_ID}_findings.md").write_text(
        "\n".join(out), encoding="utf-8"
    )




    # Save the completed report in the results folder.
    # Join all collected lines with line breaks and use UTF-8 encoding
    # to support characters from different languages.
    (RESULT_DIR / f"{PROJECT_ID}_findings.md").write_text(
        "\n".join(out), encoding="utf-8"
    )


def write_concordance(findings: list[Finding]) -> None:
    """
    Create a tab-separated concordance file from a list of findings.

    Each output line contains:
    country, document, normalized match, and sentence context.

    The resulting file is written to the project results directory.
    """

    # Collect the concordance lines before writing them to disk.
    lines = []

    # Process each Finding object in turn.
    for f in findings:

        # Construct one tab-separated concordance line:
        # country -> document -> normalized match -> sentence context
        lines.append(
            f"{f.country}\t"
            f"{f.document}\t"
            f"{normalize_expression(f.matched_text)}\t"
            f"{f.sentence}"
        )

    # Join all lines with newline characters and write the result
    # as a UTF-8 encoded TSV (tab-separated values) file.
    (RESULT_DIR / f"{PROJECT_ID}_concordance.tsv").write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

def write_statistics(findings: list[Finding]) -> None:
    """
    Generate a descriptive statistics report for the findings.

    The report contains:
    - counts by category and country,
    - counts by individual document,
    - a detailed list of all partial matches.

    The finished report is written as a plain-text file.
    """

    # Countries and match categories included in the summary tables.
    countries = ["Norway", "Sweden", "England and Wales"]
    categories = ["full_exact", "full_variant", "extended", "partial"]

    # Count findings by (category, country).
    # Example key:
    # ('full_exact', 'Norway') -> 42
    by_country = Counter((f.category, f.country) for f in findings)

    # Count findings by category and individual document.
    # Example key:
    # ('full_exact', 'Norway', 'DN.xml', '14') -> 7
    by_doc = Counter((f.category, f.country, f.source_file, f.document)
                     for f in findings)

    # Start assembling the report text.
    lines = [
        f"{PROJECT_ID} — DESCRIPTIVE STATISTICS",
        "=" * 60,
        "",
        "COUNTS BY CATEGORY AND COUNTRY",
        "(Counts are finding occurrences, not unique documents.)",
        ""
    ]

    # Create table header with aligned columns.
    header = f"{'Category':<18}" + "".join(
        f"{c:<22}" for c in countries
    ) + "Total"

    lines.append(header)
    lines.append("-" * len(header))

    # Add one summary row per category.
    for category in categories:
        vals = [by_country[(category, c)] for c in countries]
        lines.append(
            f"{category:<18}" +
            "".join(f"{v:<22}" for v in vals) +
            str(sum(vals))
        )

    # Document-level breakdown of findings.
    lines += ["", "DOCUMENT-LEVEL COUNTS", ""]

    for category in categories:
        lines += [f"[{category}]"]

        rows = [(c, sf, d, n)
                for (cat, c, sf, d), n in by_doc.items()
                if cat == category]

        for country, source_file, document, count in sorted(rows):
            lines.append(
                f"{country} | {source_file} | Document {document}: {count}"
            )

        lines.append("")

    # Detailed list of all partial matches for manual inspection.
    lines += ["PARTIAL USES — DOCUMENT LIST", ""]

    for f in findings:
        if f.category == "partial":
            lines.append(
                f"{f.country} | {f.source_file} | "
                f"Document {f.document} | {f.matched_text}"
            )

    # Write the completed report to disk.
    (RESULT_DIR / f"{PROJECT_ID}_statistics.txt").write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

# Write the results also as an XML file
# Handy for those who are fluent with XML structures and manipulations
# Suitable for the large scale analysis

def write_xml(findings: list[Finding]) -> None:
    root = ET.Element("vim_vi_rhetoric_results", {
        "project": PROJECT_ID,
        "run_date": "2026-11-06",
        "finding_count": str(len(findings))
    })
    for f in findings:
        item = ET.SubElement(root, "finding", {
            "id": f.finding_id,
            "country": f.country,
            "collection": f.collection,
            "source_file": f.source_file,
            "document": f.document,
            "classification": f.category,
            "spelling": f.spelling,
        })
        ET.SubElement(item, "matched_expression").text = f.matched_text
        ET.SubElement(item, "sentence").text = f.sentence
        if f.note:
            ET.SubElement(item, "note").text = f.note

    tree = ET.ElementTree(root)
    try:
        ET.indent(tree, space="  ")
    except AttributeError:
        pass  # Python older than 3.9
    tree.write(
        RESULT_DIR / f"{PROJECT_ID}_findings.xml",
        encoding="utf-8",
        xml_declaration=True
    )


def write_csv(findings: list[Finding]) -> None:
    csv_path = RESULT_DIR / f"{PROJECT_ID}_analysis.csv"
    fields = [
        "project", "finding_id", "country", "collection", "source_file",
        "document", "category", "spelling", "matched_text", "sentence", "note"
    ]
    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for f in findings:
            writer.writerow({
                "project": PROJECT_ID,
                "finding_id": f.finding_id,
                "country": f.country,
                "collection": f.collection,
                "source_file": f.source_file,
                "document": f.document,
                "category": f.category,
                "spelling": f.spelling,
                "matched_text": f.matched_text,
                "sentence": f.sentence,
                "note": f.note,
            })


def main() -> None:
    print(f"Starting {PROJECT_ID}")
    print(f"Output folder: {RESULT_DIR}")
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    findings = run_search()

    # Write the main reports
    write_markdown(findings)
    write_statistics(findings)
    write_xml(findings)
    write_csv(findings)

    # Write additional analysis reports
    write_variant_report(findings)
    write_country_table(findings)
    write_concordance(findings)

    print(f"Search complete: {len(findings)} candidate findings.")
    print("Files written:")

    for name in (
        f"{PROJECT_ID}_findings.md",
        f"{PROJECT_ID}_statistics.txt",
        f"{PROJECT_ID}_findings.xml",
        f"{PROJECT_ID}_analysis.csv",
        f"{PROJECT_ID}_variants.txt",
        f"{PROJECT_ID}_country_expression_table.txt",
        f"{PROJECT_ID}_concordance.tsv",
        f"{PROJECT_ID}_search_log.txt",
    ):
        target = RESULT_DIR / name
        if target.exists():
            print(f"  - {target}")

    print()
    print("Please inspect the Markdown findings manually: regex results are candidates,")
    print("and XML sentence/document extraction may need adjustment to your TEI schema.")


if __name__ == "__main__":
    main()

