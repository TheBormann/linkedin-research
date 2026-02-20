#!/usr/bin/env python3
"""Sync LinkedIn research contacts to a Google Sheet.

Usage:
    python3 sync_to_sheets.py --data '<JSON array>'
    python3 sync_to_sheets.py --file /path/to/data.json
    python3 sync_to_sheets.py --data '<JSON array>' --sheet-id 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms

Credentials:
    Place your Google service account JSON at:
    ~/.openclaw/google-credentials.json

    Or set GOOGLE_CREDENTIALS_PATH env var to a custom path.

Sheet structure (auto-created if missing):
    Tab "Contacts" with columns:
    Name | Title | Company | Company URL | Size | Rating | Company Notes |
    Location | LinkedIn | Score | Notes | Experience | Status | Contacted On |
    Draft A | Draft B | Source A | Source B

Deduplication:
    Rows are matched by LinkedIn profile URL. If a URL already exists in the
    sheet the row is UPDATED (drafts, score, notes refreshed). New contacts
    are appended at the bottom. This means running the skill multiple times
    never creates duplicates.
"""

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

try:
    import gspread
    from gspread.utils import ValueInputOption
    from google.oauth2.service_account import Credentials
except ImportError:
    print(
        "Error: Missing dependencies. Run:\n"
        "  pip3 install gspread google-auth",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

DEFAULT_CREDENTIALS_PATH = Path.home() / ".openclaw" / "google-credentials.json"
DEFAULT_SHEET_NAME = "Outreach Research"
TAB_NAME = "Contacts"

# Column order in the sheet (1-indexed positions used internally)
COLUMNS = [
    "name",
    "title",
    "company",
    "company_url",
    "company_size",
    "company_rating",
    "company_notes",
    "location",
    "profile_url",       # dedup key
    "relevance_score",
    "relevance_notes",
    "experience_summary",
    "status",            # managed manually in the sheet
    "contacted_on",      # managed manually in the sheet
    "outreach_draft_A",
    "outreach_draft_B",
    "source_A",
    "source_B",
]

HEADERS = [
    "Name",
    "Title",
    "Company",
    "Company URL",
    "Size",
    "Rating",
    "Company Notes",
    "Location",
    "LinkedIn",
    "Score",
    "Notes",
    "Experience",
    "Status",
    "Contacted On",
    "Draft A",
    "Draft B",
    "Source A",
    "Source B",
]

# Columns that the script manages (others are left alone when updating)
MANAGED_COLUMNS = {
    "name", "title", "company", "company_url", "company_size",
    "company_rating", "company_notes", "location", "relevance_score",
    "relevance_notes", "experience_summary", "outreach_draft_A",
    "outreach_draft_B", "source_A", "source_B",
}

# Column index of the dedup key (0-indexed in COLUMNS list)
PROFILE_URL_COL = COLUMNS.index("profile_url")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_credentials(path: Path) -> Credentials:
    if not path.exists():
        print(
            f"Error: Credentials file not found at {path}\n\n"
            "Run the setup:\n"
            "  See ~/.openclaw/skills/outreach-research/SHEETS_SETUP.md",
            file=sys.stderr,
        )
        sys.exit(1)
    return Credentials.from_service_account_file(str(path), scopes=SCOPES)


def get_or_create_sheet(gc: gspread.Client, sheet_id: str | None, sheet_name: str):
    if sheet_id:
        try:
            return gc.open_by_key(sheet_id)
        except gspread.SpreadsheetNotFound:
            print(f"Error: Sheet with ID '{sheet_id}' not found or not shared with service account.", file=sys.stderr)
            sys.exit(1)
    # Try by name, create if missing
    try:
        return gc.open(sheet_name)
    except gspread.SpreadsheetNotFound:
        print(f"Sheet '{sheet_name}' not found — creating it...")
        sh = gc.create(sheet_name)
        print(f"Created sheet. Share this URL with yourself: {sh.url}")
        return sh


def get_or_create_tab(sh: gspread.Spreadsheet) -> gspread.Worksheet:
    try:
        ws = sh.worksheet(TAB_NAME)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=TAB_NAME, rows=1000, cols=len(COLUMNS))
        ws.append_row(HEADERS, value_input_option=ValueInputOption.raw)
        # Freeze header row
        ws.freeze(rows=1)
        # Bold header row
        ws.format("1:1", {"textFormat": {"bold": True}})
        print(f"Created tab '{TAB_NAME}' with headers.")
    return ws


def format_sheet(ws: gspread.Worksheet):
    """Apply basic formatting: freeze, column widths, color coding for Rating."""
    try:
        # Set useful column widths
        requests = [
            # Name
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1}, "properties": {"pixelSize": 160}, "fields": "pixelSize"}},
            # Title
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 1, "endIndex": 2}, "properties": {"pixelSize": 180}, "fields": "pixelSize"}},
            # Company
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 2, "endIndex": 3}, "properties": {"pixelSize": 150}, "fields": "pixelSize"}},
            # Draft A + B wider
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 14, "endIndex": 16}, "properties": {"pixelSize": 400}, "fields": "pixelSize"}},
        ]
        ws.spreadsheet.batch_update({"requests": requests})
    except Exception:
        pass  # Formatting is best-effort, never fail the sync


# ---------------------------------------------------------------------------
# Core sync logic
# ---------------------------------------------------------------------------

def sync_contacts(ws: gspread.Worksheet, contacts: list[dict], min_score: int) -> dict:
    stats = {"added": 0, "updated": 0, "skipped": 0}

    # Filter by score
    if min_score > 0:
        before = len(contacts)
        contacts = [c for c in contacts if int(c.get("relevance_score", 0)) >= min_score]
        if len(contacts) < before:
            print(f"Filtered {before - len(contacts)} contacts below score {min_score}.")

    if not contacts:
        print("No contacts to sync.")
        return stats

    # Load existing sheet data
    all_rows = ws.get_all_values()  # includes header
    header_row = all_rows[0] if all_rows else []
    data_rows = all_rows[1:] if len(all_rows) > 1 else []

    # Build dedup index: profile_url -> (row_index_in_sheet, 1-indexed)
    # Sheet row 1 = header, row 2 = first data row
    existing_urls: dict[str, int] = {}
    for i, row in enumerate(data_rows):
        url = row[PROFILE_URL_COL].strip() if len(row) > PROFILE_URL_COL else ""
        if url:
            existing_urls[url] = i + 2  # 1-indexed, +1 for header, +1 for 1-indexing

    # Batch updates
    rows_to_append = []
    cell_updates = []

    for contact in contacts:
        profile_url = contact.get("profile_url", "").strip()
        row_values = [contact.get(col, "") for col in COLUMNS]

        if profile_url and profile_url in existing_urls:
            # UPDATE: only overwrite managed columns, preserve Status and Contacted On
            sheet_row = existing_urls[profile_url]
            for col_idx, col_name in enumerate(COLUMNS):
                if col_name in MANAGED_COLUMNS:
                    cell_updates.append({
                        "range": gspread.utils.rowcol_to_a1(sheet_row, col_idx + 1),
                        "values": [[str(contact.get(col_name, ""))]],
                    })
            stats["updated"] += 1
        else:
            rows_to_append.append([str(v) for v in row_values])
            stats["added"] += 1

    # Apply batch cell updates
    if cell_updates:
        ws.batch_update(cell_updates, value_input_option=ValueInputOption.raw)

    # Append new rows
    if rows_to_append:
        ws.append_rows(rows_to_append, value_input_option=ValueInputOption.raw)

    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Sync LinkedIn research contacts to Google Sheets")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--data", "-d", help="JSON string of contact array")
    group.add_argument("--file", "-f", help="Path to JSON file with contact array")
    parser.add_argument("--sheet-id", help="Google Sheet ID (from URL). If omitted, opens/creates sheet by name.")
    parser.add_argument("--sheet-name", default=DEFAULT_SHEET_NAME, help=f"Sheet name to open or create (default: '{DEFAULT_SHEET_NAME}')")
    parser.add_argument("--credentials", default=str(DEFAULT_CREDENTIALS_PATH), help="Path to service account JSON credentials")
    parser.add_argument("--min-score", type=int, default=3, help="Exclude contacts below this score (default: 3)")
    args = parser.parse_args()

    # Parse contacts
    if args.data:
        try:
            contacts = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            with open(args.file) as f:
                contacts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    if not isinstance(contacts, list):
        print("Error: JSON must be an array of contact objects.", file=sys.stderr)
        sys.exit(1)

    # Auth
    creds = load_credentials(Path(args.credentials))
    gc = gspread.authorize(creds)

    # Open/create sheet and tab
    sh = get_or_create_sheet(gc, args.sheet_id, args.sheet_name)
    ws = get_or_create_tab(sh)
    format_sheet(ws)

    # Sync
    stats = sync_contacts(ws, contacts, args.min_score)

    print(f"\nSync complete:")
    print(f"  Added:   {stats['added']} new contacts")
    print(f"  Updated: {stats['updated']} existing contacts")
    print(f"\nOpen your sheet: {sh.url}")


if __name__ == "__main__":
    main()
