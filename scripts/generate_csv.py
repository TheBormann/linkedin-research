#!/usr/bin/env python3
"""Generate a CSV file from LinkedIn research data.

Usage:
    python3 generate_csv.py --output /path/to/output.csv --data '<JSON array>'
    python3 generate_csv.py --output /path/to/output.csv --file /path/to/data.json

Fields per contact:
    name, title, company, company_url, company_size, company_rating, company_notes,
    location, profile_url, relevance_score, relevance_notes, experience_summary,
    outreach_draft_A, outreach_draft_B (and legacy outreach_draft)
"""

import argparse
import csv
import json
import sys
from pathlib import Path

FIELDS = [
    "name",
    "title",
    "company",
    "company_url",
    "company_size",
    "company_rating",
    "company_notes",
    "location",
    "profile_url",
    "relevance_score",
    "relevance_notes",
    "experience_summary",
    "outreach_draft_A",
    "outreach_draft_B",
    "outreach_draft",
]


def main():
    parser = argparse.ArgumentParser(description="Generate LinkedIn research CSV")
    parser.add_argument("--output", "-o", required=True, help="Output CSV file path")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--data", "-d", help="JSON string of contact array")
    group.add_argument("--file", "-f", help="Path to JSON file with contact array")
    parser.add_argument(
        "--append", "-a", action="store_true", help="Append to existing CSV"
    )
    parser.add_argument(
        "--min-score", type=int, default=0,
        help="Exclude contacts below this relevance score (default: 0)"
    )
    args = parser.parse_args()

    # Parse input
    if args.data:
        try:
            contacts = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON data: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            with open(args.file, "r") as f:
                contacts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    if not isinstance(contacts, list):
        print("Error: JSON data must be an array of contact objects", file=sys.stderr)
        sys.exit(1)

    # Filter by minimum score
    if args.min_score > 0:
        before = len(contacts)
        contacts = [c for c in contacts if c.get("relevance_score", 0) >= args.min_score]
        filtered = before - len(contacts)
        if filtered:
            print(f"Filtered out {filtered} contacts below score {args.min_score}")

    # Sort: company_rating A first, then by relevance score descending
    rating_order = {"A": 0, "B": 1, "C": 2}
    contacts.sort(
        key=lambda c: (
            rating_order.get(c.get("company_rating", "C"), 2),
            -c.get("relevance_score", 0),
        )
    )

    # Write CSV
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    mode = "a" if args.append else "w"
    write_header = not args.append or not output_path.exists()

    with open(output_path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        for contact in contacts:
            writer.writerow(contact)

    # Summary
    print(f"Wrote {len(contacts)} contacts to {output_path}")
    by_rating = {}
    for c in contacts:
        r = c.get("company_rating", "?")
        by_rating[r] = by_rating.get(r, 0) + 1
    print(f"  By company rating: {', '.join(f'{k}={v}' for k, v in sorted(by_rating.items()))}")
    print(f"  Score range: {min(c.get('relevance_score', 0) for c in contacts)}-{max(c.get('relevance_score', 0) for c in contacts)}" if contacts else "  (empty)")


if __name__ == "__main__":
    main()
