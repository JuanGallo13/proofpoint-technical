# Data Quality Report

Total input records: 44
Total output records: 23
Number of discarded entries: 7
Number of corrected entries: 13
Number of duplicates detected: 14

## Deduplication Strategy
Episodes were considered duplicates using three possible keys:
- (SeriesName_normalized, SeasonNumber, EpisodeNumber)
- (SeriesName_normalized, 0, EpisodeNumber, EpisodeTitle_normalized)
- (SeriesName_normalized, SeasonNumber, 0, EpisodeTitle_normalized)

When duplicates were found, the best record was selected using the following priority:
- Valid Air Date over 'Unknown'
- Known Episode Title over 'Untitled Episode'
- Valid Season and Episode numbers
- If still tied, the first record encountered was kept.
