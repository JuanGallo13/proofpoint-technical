# Proofpoint Intern Challenge

This project contains a solution for the catalog cleaning exercise.

The program reads a CSV file containing TV series episode records and produces a cleaned version of the dataset, handling common data quality issues such as missing values, invalid formats, and duplicate entries.

## What the program does

The script processes the input file and applies the following steps:

- Parses all records from the CSV file
- Normalizes and validates episode data
- Replaces invalid or missing values using safe defaults
- Detects and removes duplicate episodes
- Produces a cleaned catalog
- Generates a small data quality report summarizing the results

## Running the program

Place the input file `episodes.csv` in the same directory as the script and run:


python clean_catalog.py


## Output files

The program generates two files:

**episodes_clean.csv**

A cleaned catalog containing the following fields:


SeriesName,SeasonNumber,EpisodeNumber,EpisodeTitle,AirDate


All corrections and deduplication rules are applied.

**report.md**

A short report summarizing:

- number of input records
- number of output records
- discarded entries
- corrected entries
- duplicates detected
- explanation of the deduplication logic