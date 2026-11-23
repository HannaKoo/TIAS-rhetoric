# *Vim vi repellendo* as a rhetorical device — Corpus Search and Analysis

This repository/folder contains the Python code used to search the Apostolic Penitentiary corpora for occurrences and variants of the expression *vim vi repellendo* in material from Norway, Sweden, and England and Wales.

The script searches the XML text samples, records candidate occurrences with their source and document information, and produces reports for inspection and further analysis. Search results are candidates; the script should not replace the manual checking the original editions or XML passages.

## Important note about citing the corpus

The text samples analysed in this project are drawn from the published editions listed below. When citing the historical documents, please refer to the respective editions and credit the editors according to the bibliographic references provided for each region.

### Norway

Jørgensen, Torstein, and Gastone Saletnich. 2004. *Synder og pavemakt: botsbrev fra Den Norske Kirkeprovins og Suderøyene til Pavestolen, 1438–1531*. Diplomatarium Poenitentiariae Norvegicum. Misjonshøgskolens forlag. ISBN 9788277210841.

### England and Wales

Clarke, Peter D., and Patrick N. R. Zutshi. 2013. *Supplications from England and Wales in the registers of the Apostolic Penitentiary, 1410–1503*. Volume I, 1410–1464. Canterbury and York Society, Vol. CIII. Woodbridge, Suffolk: Canterbury / York Society. ISBN 978-0-907239-75-8.

Clarke, Peter D., and Patrick N. R. Zutshi. 2014. *Supplications from England and Wales in the registers of the Apostolic Penitentiary, 1410–1503*. Volume II, 1464–1492. Canterbury and York Society, Vol. CIV. Woodbridge, Suffolk: Canterbury / York Society. ISBN 978-0-907239-77-2.

Clarke, Peter D., Patrick N. R. Zutshi, and Kelcey Wilson-Lee. 2015. *Supplications from England and Wales in the registers of the Apostolic Penitentiary, 1410–1503*. Volume III, 1492–1503. Canterbury and York Society, Vol. CV. Woodbridge, Suffolk: Canterbury / York Society. ISBN 978-0-907239-78-9.

### Sweden

Risberg, Sara, and Kirsi Salonen. 2008. *Appendix: Acta Pontificum Suecica. 2, Acta Poenitentiare: Auctoritate papae: the church province of Uppsala and the apostolic penitentiary 1410–1526*. Diplomatarium Suecanum. Stockholm: Riksarkivet. ISBN 978-91-88366-82-5.


## Research scope

The search focuses on the sequence *vim* + *vi* followed by a form related to *repellendo*. It also records instances where the phrase *vim vi* occurs without a detected participle-like form, as well as longer/extended constructions where lexical material intervenes between *vi* and the detected participle.

The project includes these source groups:

- **Norway** — one XML file
- **Sweden** — one XML file
- **England and Wales** — three XML files

## Search approach

The script uses Python regular expressions to locate candidate expressions. Matching is case-insensitive and tolerates certain whitespace, punctuation, brackets, and editorial marks between the core words. It searches for the sequence in the order `vim` → `vi` → a participle-like form.

The participle pattern is deliberately broad, allowing some spelling variation (including doubled letters and certain vowel variations). This is intended to capture possible variants for review, not to establish that every match is linguistically valid.

### Categories used in the reports

- **`full_exact`** — the normalized match is *vim vi repellendo*.
- **`full_variant`** — a detected participle-like form follows *vim vi* without intervening lexical material, but the normalized expression is not the exact form *vim vi repellendo*.
- **`extended`** — lexical material occurs between *vim vi* and the detected participle-like form within the search window.
- **`partial`** — *vim vi* occurs but no participle-like form is detected in the search window.

These labels are automated classifications based on the script's current pattern and rules. They should be checked against the text in context before being used as linguistic or legal conclusions.

## The files

- The files will be available in an another GitHub soon, a link will be added later

## Running the analysis

Use the main code: python vim_vi_rhetoric_fixed_document_ids.py


## Output files

The script produces the following files. Each filename begins with the project identifier `vim_vi_rhetoric`.

| File | Contents |
|---|---|
| `vim_vi_rhetoric_findings.md` | Readable Markdown report of findings, grouped by country, source file, and document; includes the sentence/passsage, match, finding ID, and classification. The detected phrase is highlighted for review. |
| `vim_vi_rhetoric_statistics.txt` | Counts by category and country, document-level counts, and a list of partial occurrences. Counts are occurrence counts, not counts of unique documents. |
| `vim_vi_rhetoric_findings.xml` | Structured XML export of each finding and its associated source/document metadata, sentence, classification, spelling label, and optional note. |
| `vim_vi_rhetoric_analysis.csv` | Tabular export of the findings, suitable for spreadsheet review; includes source metadata, document number, category, match, sentence, and note. |
| `vim_vi_rhetoric_variants.txt` | Frequency list of normalized expressions/variants. |
| `vim_vi_rhetoric_country_expression_table.txt` | Expression frequency table broken down by Norway, Sweden, and England and Wales. |
| `vim_vi_rhetoric_concordance.tsv` | Tab-separated concordance with country, document number, normalized expression, and sentence. |
| `vim_vi_rhetoric_search_log.txt` | Log of missing input files or parsing errors, if encountered. |


## Reviewing and validating findings

The output is intended to support manual verification. In particular:


- Check each highlighted occurrence against the source XML and, where appropriate, the published edition.
- Verify that document boundaries and document numbers are being extracted correctly for each corpus, since the XML structures differ between collections.
- Review the automated category assignment, especially `extended` and `partial` cases, and confirm that the match is relevant to the expression under study.
- Treat the spelling/variant frequency tables as normalized search summaries. The source spelling and sentence are retained in the findings for checking.
- If the XML contains multiple occurrences in a single sentence, inspect the sentence and match fields carefully; one sentence may yield more than one candidate finding.

The script does not modify the source XML files. It reads them and writes reports to the project results directory.





