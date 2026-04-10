import csv
from pathlib import Path
import argparse
BASE_DIR = Path("./")
OUTPUT_DIR = Path("build")
LANG = "ja-JP"

def load_csv_files(directory: Path):
    entries = []
    for file in directory.glob("*.csv"):
        with open(file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                reading = row.get("reading", "").strip()
                word = row.get("word", "").strip()
                pos = row.get("pos", "").strip()

                if reading and word:
                    entries.append((reading, word, pos))
    return entries

def write_gboard(entries, output_path):
    with open(output_path, "w", encoding="utf-8") as out:
        out.write("# Gboard Dictionary version:2\n")
        out.write("# Gboard Dictionary format:shortcut\tword\tlanguage_tag\tpos_tag\n")

        for reading, word, pos in entries:
            out.write(f"{reading}\t{word}\t{LANG}\t{pos}\n")

def deduplicate(entries):
    seen = set()
    result = []
    for entry in entries:
        if entry not in seen:
            seen.add(entry)
            result.append(entry)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-private", action="store_true")
    args = parser.parse_args()

    public_entries = load_csv_files(BASE_DIR / "public")

    if args.no_private:
        private_entries = []
    else:
        private_entries = load_csv_files(BASE_DIR / "private")

    public_entries = deduplicate(public_entries)
    private_entries = deduplicate(private_entries)
    all_entries = deduplicate(public_entries + private_entries)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    write_gboard(public_entries, OUTPUT_DIR / "gboard_public.txt")

    if not args.no_private:
        write_gboard(private_entries, OUTPUT_DIR / "gboard_private.txt")

    write_gboard(all_entries, OUTPUT_DIR / "gboard_all.txt")
if __name__ == "__main__":
    main()