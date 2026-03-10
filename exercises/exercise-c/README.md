# Word Frequency Analyzer

This program reads a text file and analyzes the frequency of words in the document.  
The script cleans and normalizes the text, counts how many times each word appears, and displays the **Top 10 most frequent words** in a small graphical interface.



## Text Processing

Before counting the words, the program performs several preprocessing steps:

- Converts all text to lowercase
- Removes accents and diacritics
- Removes punctuation and non-letter characters
- Splits the text into individual words

These steps ensure that words like `Data`, `data`, or `data,` are treated as the same token.



## Word Counting

Word frequencies are calculated using Python's `Counter` class from the `collections` module.  
The program then extracts the **10 most common words** from the dataset.



## Interface

Instead of printing the results to the terminal, the program opens a small **Tkinter GUI** that displays the results in a ranked list.

### Features of the interface

- Ranking of the **Top 10 words**
- Medals for the top 3 results (🥇🥈🥉)
- Word displayed on the left and its count on the right
- Simple dark theme layout for readability



## How to Run

Make sure Python is installed, then run:

```bash
python word_frequency.py sample.txt