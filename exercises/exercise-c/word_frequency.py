import re
from collections import Counter
import sys
import unicodedata
import tkinter as tk


def clean_text(text):

    text = text.lower()

    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")

    text = re.sub(r"[^a-z\s]", "", text)

    return text.split()


def count_words(filename):

    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    words = clean_text(text)

    return Counter(words)


def show_results(counter, n=10):

    root = tk.Tk()
    root.title("Word Frequency Analyzer - Proofpoint")
    root.geometry("550x550")
    root.configure(bg="#1a1a1a")

    title = tk.Label(
        root,
        text="Top 10 Most Frequent Words",
        font=("Segoe UI", 16, "bold"),
        fg="white",
        bg="#1a1a1a"
    )
    title.pack(pady=15)

    container = tk.Frame(root, bg="#1a1a1a")
    container.pack()

    medals = ["🥇", "🥈", "🥉"]
    colors = ["#FFD700", "#C0C0C0", "#CD7F32"]

    results = counter.most_common(n)

    for i, (word, count) in enumerate(results):

        card = tk.Frame(
            container,
            bg="#262626",
            padx=12,
            pady=6
        )
        card.pack(fill="x", padx=40, pady=3)

        medal = medals[i] if i < 3 else ""
        color = colors[i] if i < 3 else "white"

        # Ranking + Word
        word_label = tk.Label(
            card,
            text=f"{i+1}. {medal} {word}",
            font=("Segoe UI", 11, "bold"),
            fg=color,
            bg="#262626",
            anchor="w"
        )
        word_label.pack(side="left")

        # Count column
        count_label = tk.Label(
            card,
            text=f"Count: {count}",
            font=("Segoe UI", 11),
            fg="white",
            bg="#262626"
        )
        count_label.pack(side="right")

    root.mainloop()


def main():

    if len(sys.argv) < 2:
        print("Usage: python word_frequency.py <text_file>")
        return

    filename = sys.argv[1]

    counter = count_words(filename)

    show_results(counter)


if __name__ == "__main__":
    main()