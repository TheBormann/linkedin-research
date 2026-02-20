# Google Sheets Setup (One-Time)

Five steps. Takes ~10 minutes. Never repeat.

---

## Step 1 — Create a Google Cloud Project

1. Go to https://console.cloud.google.com
2. Click the project dropdown (top left) → **New Project**
3. Name it anything, e.g. `openclaw-outreach`
4. Click **Create**

---

## Step 2 — Enable the Sheets and Drive APIs

With your new project selected:

1. Go to https://console.cloud.google.com/apis/library
2. Search **Google Sheets API** → Enable
3. Search **Google Drive API** → Enable

---

## Step 3 — Create a Service Account

1. Go to https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click **Create Service Account**
3. Name: `openclaw` (anything works)
4. Click **Create and Continue** → skip role assignment → **Done**
5. Click the service account you just created
6. Go to **Keys** tab → **Add Key** → **Create new key** → **JSON**
7. A JSON file downloads automatically

---

## Step 4 — Save the credentials file

Move the downloaded JSON to:

```bash
mv ~/Downloads/your-project-*.json ~/.openclaw/google-credentials.json
```

That path is where the script looks by default.

---

## Step 5 — Share your Google Sheet with the service account

Open the credentials JSON and find the `client_email` field. It looks like:

```
openclaw@your-project.iam.gserviceaccount.com
```

Then:

1. Open your Google Sheet (or let the script create one — skip this step if you want the script to create a new sheet)
2. Click **Share** (top right)
3. Paste the `client_email` address
4. Set permission to **Editor**
5. Click **Send**

---

## Done. Test it:

```bash
python3 ~/.openclaw/skills/outreach-research/scripts/sync_to_sheets.py \
  --data '[{"name":"Test Contact","title":"QA Manager","company":"Pharma GmbH","profile_url":"https://linkedin.com/in/test","relevance_score":4}]'
```

The script will print the sheet URL. Open it and confirm the row appeared.

---

## Using a specific sheet by ID

If you already have a sheet you want to write to, grab its ID from the URL:

```
https://docs.google.com/spreadsheets/d/THIS_IS_THE_ID/edit
```

Then pass it to the script:

```bash
python3 sync_to_sheets.py --data '...' --sheet-id THIS_IS_THE_ID
```

Or set it in the skill invocation — the skill will remember it per problem space.

---

## Troubleshooting

**"Credentials file not found"**
→ Check that `~/.openclaw/google-credentials.json` exists.

**"Sheet not found or not shared with service account"**
→ You passed `--sheet-id` but didn't share the sheet with the `client_email`. See Step 5.

**"PERMISSION_DENIED" or 403 error**
→ The Sheets or Drive API is not enabled. Go back to Step 2.

**"insufficient authentication scopes"**
→ Delete the credentials file and re-download a fresh one from Step 3.
