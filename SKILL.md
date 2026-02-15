---
name: linkedin-research
description: Research LinkedIn contacts for problem discovery and customer development. Finds decision makers (not ICs), qualifies their companies by checking websites, and targets the sweet spot between too-small and enterprise. Use when the user wants to find interview targets, map decision makers, or research contacts for outbound. Triggers on "find people to interview about X", "research LinkedIn contacts", "who should I talk to about Z problem", "find decision makers at company W".
---

# LinkedIn Research

Find and qualify decision-maker contacts for problem discovery interviews. Three-phase process: find people, qualify their companies, score and rank.

## Prerequisites

- User must be logged into LinkedIn in the `openclaw` browser profile
- If not logged in: `openclaw browser start && openclaw browser open https://linkedin.com` — ask user to log in manually
- Never attempt automated login (triggers anti-bot lockout)

## Phase 1: Research Brief

Collect from the user:

- **Problem space**: What problem are they exploring?
- **Target persona**: Seniority + function (e.g. "heads of product at B2B SaaS")
- **Company sweet spot**: Industry, stage, size range (default: 20-500 employees)
- **Geography** (optional): Location constraints
- **Interview goal**: What specific insight do they need?

If the user doesn't specify company size, default to the **mid-market sweet spot**: companies with roughly 20-500 employees, Series A through C, or bootstrapped with visible traction. These are ideal because:
- Decision makers are accessible (not behind layers of gatekeepers)
- They're big enough to have real problems worth solving
- People actually make purchasing/process decisions (not just "I'll pass it up the chain")

## Phase 2: Find Decision Makers on LinkedIn

### Search Strategy

Build searches that target **decision-making titles**, not generic keywords. Always combine a seniority keyword with the domain:

```
"VP Engineering" AND (SaaS OR "developer tools")
"Head of Product" AND "B2B"
founder AND (logistics OR "supply chain")
"Chief Technology Officer" OR CTO AND fintech
```

**Title priority order** (highest decision power first):

| Tier | Titles | Why |
|------|--------|-----|
| 1 | Founder, CEO, CTO, COO | Own the problem and the budget |
| 2 | VP, SVP, Head of [Function] | Direct authority over team/budget |
| 3 | Director | Influence + context, often closer to the problem |
| 4 | Senior Manager | Only if at a smaller company (<100 people) where this is effectively a director role |

**Skip:** Individual contributors, analysts, associates, coordinators, interns. They rarely have decision power or budget visibility.

### Execute Search

```bash
openclaw browser open "https://www.linkedin.com/search/results/people/?keywords=<URL-encoded query>" --browser-profile openclaw
```

Wait for load, then snapshot:

```bash
openclaw browser snapshot --browser-profile openclaw
```

**Apply filters via UI:**
1. Snapshot to find filter button refs
2. Click relevant filters (Locations, Current company, Industry)
3. Re-snapshot after each filter

**Pagination:** Click "Next" button ref for more results. Aim for 2-3 pages max per search query.

### Extract from Search Results

For each result, capture: **Name, Headline, Company, Location, Profile URL**.

Immediately **skip** anyone whose title is IC-level (engineer, designer, analyst, associate, etc.) unless the company is very small (<20 people).

### Deep-Dive Profiles (selective)

Only open individual profiles for Tier 1-2 candidates. Extract:

- Current role + duration (longer tenure = more context about the problem)
- Previous experience (pattern of relevant domain experience?)
- About section (do they mention the problem space?)
- Recent posts/activity (are they thinking about this topic publicly?)
- Company name + size indicator from profile

```bash
openclaw browser open "<profile-url>" --browser-profile openclaw
openclaw browser snapshot --browser-profile openclaw
```

## Phase 3: Qualify the Company

**This is critical.** A perfect-title contact at the wrong company is a wasted interview. For each candidate's company, check the website.

### Company Website Check

```bash
openclaw browser open "<company-website>" --browser-profile openclaw
openclaw browser snapshot --browser-profile openclaw
```

Evaluate these signals:

**Green flags (keep):**
- Professional, modern website (not a template with stock photos)
- Clear product/service description — they know what they do
- Customer logos, case studies, or testimonials
- Active blog or content (recent posts within 3 months)
- Hiring page with open roles (sign of growth)
- Pricing page (means real customers paying money)

**Red flags (disqualify):**
- Website is down, broken, or parked domain
- Last blog post is 2+ years old
- No clear product — just buzzwords
- "Coming soon" or "stealth mode" with nothing to show
- Only 1-2 LinkedIn employees and a Wix site

**Size disqualifiers:**
- **Too small** (<10 employees, no real website): Skip — they likely don't have the problem at scale yet, or can't pay for a solution
- **Too big** (>2000 employees, Fortune 500): Skip unless user specifically wants enterprise. Reasons:
  - Getting a meeting is 10x harder
  - They can't speak freely (NDA culture, PR review)
  - Decisions involve 12 stakeholders — bad signal for problem discovery
  - Their problems are often unique to scale, not representative

### Company Size Estimation

Use multiple signals since LinkedIn employee count isn't always accurate:

1. **LinkedIn company page**: Check employee count range
2. **Website careers page**: Number of open roles indicates size
3. **Crunchbase/funding** (if easily found): Funding stage maps to company size
4. **Team page on website**: Sometimes lists the team directly

### Company Rating

| Rating | Profile | Action |
|--------|---------|--------|
| A | 20-500 employees, funded or profitable, active product, modern site | Top priority — interview these first |
| B | 10-20 or 500-2000 employees, decent product, some traction signals | Good backup — interview if A-tier runs thin |
| C | <10 or >2000 employees, unclear product, or stale web presence | Skip unless the contact is exceptionally relevant |

## Phase 4: Score and Rank

Combined score (1-5) based on **both** person fit AND company fit:

| Score | Person | Company | Verdict |
|-------|--------|---------|---------|
| 5 | Tier 1-2 title, relevant domain, active on topic | A-rated, perfect industry fit | Interview immediately |
| 4 | Tier 1-2 title, relevant domain | A or B-rated | Strong candidate |
| 3 | Tier 2-3 title, somewhat relevant | A or B-rated | Worth reaching out |
| 2 | Right title but wrong domain, OR right domain but IC-level | B or C-rated | Only if pipeline is thin |
| 1 | IC at a C-rated company | C-rated | Do not contact |

**Disqualify entirely (score 0, omit from CSV):**
- IC with no decision authority at a large company
- Company website is dead/parked
- Contact has been in role <3 months (no context yet)

## Phase 5: Draft Outreach

For contacts scored 3+, draft a personalized outreach message using the templates in [references/outreach-templates.md](references/outreach-templates.md). Read that file before drafting any messages.

**Template selection (quick reference):**

| Contact type | Template |
|-------------|----------|
| Founder/CEO testing a hypothesis | 1 — Hypothesis |
| Founder/CEO, peer comparison angle | 2 — Pattern |
| VP/Head of, understanding their workflow | 3 — Workflow |
| Warm connection or early-stage founder | 4 — Short |

**Language:** Default to German for DACH-region contacts, English otherwise. Ask user if unclear.

**Key rules:**
- Fill all placeholders with specifics from the research (never leave generic text)
- Leave `[CALENDLY-LINK]` as-is — user fills this in
- Never pitch a solution — frame everything as research/exploration
- Reference something concrete from their profile or company

## Phase 6: Generate CSV

```bash
python3 ~/.openclaw/skills/linkedin-research/scripts/generate_csv.py \
  --output ~/.openclaw/workspace/linkedin_research_$(date +%Y-%m-%d).csv \
  --data '<JSON array>'
```

JSON format per contact:

```json
{
  "name": "Jane Smith",
  "title": "VP Product",
  "company": "Acme Corp",
  "company_url": "https://acme.com",
  "company_size": "~120 employees",
  "company_rating": "A",
  "company_notes": "Series B, active SaaS product, hiring 8 roles",
  "location": "San Francisco, CA",
  "profile_url": "https://linkedin.com/in/janesmith",
  "relevance_score": 4,
  "relevance_notes": "Led product at 3 B2B SaaS cos, posts about user research methods",
  "experience_summary": "10yr product leadership, prev. Stripe and Notion",
  "outreach_draft": "Hi Jane, I'm researching how product teams prioritize user feedback..."
}
```

## Rate Limiting

- Wait 2-3 seconds between page loads
- Max 20-30 profiles per session (LinkedIn + company sites combined)
- If CAPTCHA appears, stop and ask the user to solve it

## Tips

- **Sales Navigator** (if available) has company size and seniority filters built in — use `linkedin.com/sales/search/people`
- **Boolean search** in keywords: `"VP Engineering" AND (SaaS OR "B2B") NOT "looking for"`
- **2nd connections** are warm intro opportunities — prioritize them
- **"People Also Viewed"** sidebar on profiles surfaces similar decision makers
- **Batch by company**: When you find one good person at a company, check if there are other relevant contacts there too
