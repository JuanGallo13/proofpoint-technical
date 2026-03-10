import csv
from datetime import datetime

INPUT_FILE = "episodes.csv"
OUTPUT_FILE = "episodes_clean.csv"
REPORT_FILE = "report.md"


def normalize_text(text):
    if not text:
        return ""
    return " ".join(text.strip().lower().split())


def clean_series(series):
    if not series:
        return ""
    return " ".join(series.strip().split())


def clean_title(title):
    if not title or not title.strip():
        return "Untitled Episode"
    return " ".join(title.strip().split())


def clean_number(value):
    try:
        n = int(value)
        if n < 0:
            return 0
        return n
    except:
        return 0


def clean_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return date
    except:
        return "Unknown"


def is_missing_episode_data(ep):
    return (
        ep["episode"] == 0
        and ep["title"] == "Untitled Episode"
        and ep["date"] == "Unknown"
    )


def better_record(a, b):

    score_a = (
        a["date"] != "Unknown",
        a["title"] != "Untitled Episode",
        a["season"] != 0 and a["episode"] != 0
    )

    score_b = (
        b["date"] != "Unknown",
        b["title"] != "Untitled Episode",
        b["season"] != 0 and b["episode"] != 0
    )

    return a if score_a >= score_b else b


def read_and_clean():

    total_input = 0
    discarded = 0
    corrected = 0
    cleaned = []

    with open(INPUT_FILE, newline="", encoding="utf-8") as f:

        reader = csv.reader(f)

        for row in reader:

            total_input += 1

            if not row:
                discarded += 1
                continue

            raw_series = row[0] if len(row) > 0 else ""
            raw_season = row[1] if len(row) > 1 else ""
            raw_episode = row[2] if len(row) > 2 else ""
            raw_title = row[3] if len(row) > 3 else ""
            raw_date = row[4] if len(row) > 4 else ""

            series = clean_series(raw_series)

            if not series:
                discarded += 1
                continue

            season = clean_number(raw_season)
            episode = clean_number(raw_episode)
            title = clean_title(raw_title)
            date = clean_date(raw_date)

            if (
                raw_series.strip() != series
                or raw_season != str(season)
                or raw_episode != str(episode)
                or (raw_title or "").strip() != title
                or raw_date != date
            ):
                corrected += 1

            record = {
                "series": series,
                "season": season,
                "episode": episode,
                "title": title,
                "date": date
            }

            if is_missing_episode_data(record):
                discarded += 1
                continue

            cleaned.append(record)

    return cleaned, total_input, discarded, corrected


def deduplicate(records):

    duplicates = 0
    unique = {}

    for ep in records:

        series_norm = normalize_text(ep["series"])
        title_norm = normalize_text(ep["title"])

        keys = [
            ("A", series_norm, ep["season"], ep["episode"]),
            ("B", series_norm, 0, ep["episode"], title_norm),
            ("C", series_norm, ep["season"], 0, title_norm)
        ]

        found = None

        for k in keys:
            if k in unique:
                found = k
                break

        if found:
            duplicates += 1
            unique[found] = better_record(unique[found], ep)
        else:
            unique[keys[0]] = ep

    return list(unique.values()), duplicates


def write_csv(records):

    records.sort(key=lambda x: (
        normalize_text(x["series"]),
        x["season"],
        x["episode"]
    ))

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "SeriesName",
            "SeasonNumber",
            "EpisodeNumber",
            "EpisodeTitle",
            "AirDate"
        ])

        for ep in records:
            writer.writerow([
                ep["series"],
                ep["season"],
                ep["episode"],
                ep["title"],
                ep["date"]
            ])


def write_report(total_input, total_output, discarded, corrected, duplicates):

    with open(REPORT_FILE, "w") as f:

        f.write("# Data Quality Report\n\n")

        f.write(f"Total input records: {total_input}\n")
        f.write(f"Total output records: {total_output}\n")
        f.write(f"Number of discarded entries: {discarded}\n")
        f.write(f"Number of corrected entries: {corrected}\n")
        f.write(f"Number of duplicates detected: {duplicates}\n")

        f.write("\n## Deduplication Strategy\n")

        f.write(
            "Episodes were considered duplicates using three possible keys:\n"
        )

        f.write(
            "- (SeriesName_normalized, SeasonNumber, EpisodeNumber)\n"
        )

        f.write(
            "- (SeriesName_normalized, 0, EpisodeNumber, EpisodeTitle_normalized)\n"
        )

        f.write(
            "- (SeriesName_normalized, SeasonNumber, 0, EpisodeTitle_normalized)\n\n"
        )

        f.write(
            "When duplicates were found, the best record was selected using the following priority:\n"
        )

        f.write("- Valid Air Date over 'Unknown'\n")
        f.write("- Known Episode Title over 'Untitled Episode'\n")
        f.write("- Valid Season and Episode numbers\n")
        f.write("- If still tied, the first record encountered was kept.\n")


def main():

    cleaned, total_input, discarded, corrected = read_and_clean()

    unique, duplicates = deduplicate(cleaned)

    write_csv(unique)

    write_report(
        total_input,
        len(unique),
        discarded,
        corrected,
        duplicates
    )


if __name__ == "__main__":
    main()