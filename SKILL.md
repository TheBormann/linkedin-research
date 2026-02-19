---
name: outreach-research
description: Research and qualify contacts for problem discovery outreach. User pastes contacts from LinkedIn or other sources. Skill handles company research via public sources, Google-cached LinkedIn enrichment, scoring, and A/B outreach draft generation. Triggers on "find people to interview about X", "research contacts", "who should I talk to about Z problem", "qualify these contacts", "draft outreach for these people".
---

# Outreach Research

Qualify decision-maker contacts and generate A/B-tested outreach drafts. The user manually browses LinkedIn and pastes contact info. The skill does everything else: company research via public sources, scoring, and draft generation.

**Core principle: zero LinkedIn automation.** All LinkedIn activity is done by the user manually. The skill never touches LinkedIn — it researches companies through websites, Crunchbase, Google, and other public sources. This keeps the user's LinkedIn account safe.

## Phase 1: Research Brief

Collect from the user:

- **Problem space**: What problem are they exploring?
- **Target persona**: Seniority + function (e.g. "heads of product at B2B SaaS")
- **Company sweet spot**: Industry, stage, size range (default: 5-200 employees)
- **Geography** (optional): Location constraints
- **Interview goal**: What specific insight do they need?
- **Already contacted** (optional): Names of people they've already reached out to. Parse into a simple exclusion list of `name + company` pairs. Skip these throughout the process.

Default to the **AI-startup sweet spot**: 5-200 employees, Seed through Series B, AI agents as core product. Bootstrapped with visible traction also works.

**Avoid enterprise (>1000) and vertical SaaS where AI is a bolt-on.** Response rate from outreach data is near zero for these profiles.

### Search Guidance for the User

Give the user these LinkedIn search queries to run manually. They copy-paste the results back to you.

**LinkedIn People Search queries:**
```
"VP Engineering" AND (SaaS OR "developer tools")
"Head of Product" AND "B2B"
founder AND ("AI agent" OR "agentic" OR "autonomous agent")
"CTO" AND ("LLM" OR "RAG" OR "agent") AND (Berlin OR Munich OR Hamburg)
```

**Google-indexed LinkedIn profiles (no LinkedIn login needed):**
```
site:linkedin.com/in "founder" ("AI agent" OR "agentic") Germany
site:linkedin.com/in "CEO" ("LLM" OR "RAG" OR "agent") Berlin OR Munich OR Hamburg
```

**Where to find AI-agent startups:**
- YC W24/S24/W25 batches — filter for AI/agent companies with EU founders
- EU AI startup lists on Sifted, Tech.eu, or HTGF portfolio pages
- Product Hunt launches tagged "AI agent" in last 6 months
- HTGF, Earlybird, Cherry Ventures, La Famiglia portfolios — filter for AI
- GitHub trending — founders of popular agent frameworks often have startups

Tell the user to browse these, pick people who look relevant, and paste what they find.

## Phase 2: User Pastes Contacts

The user browses LinkedIn manually and pastes contact information. Accept **any format** — the skill must parse all of these:

**Accepted input formats:**
- Plain text: `"Max Müller, CTO at AgentStack, linkedin.com/in/maxmueller"`
- Bullet lists or numbered lists
- Pasted LinkedIn search result snippets (name, headline, company from the cards)
- Pasted LinkedIn profile URLs (one per line)
- CSV or spreadsheet paste
- Screenshot descriptions ("I see these 5 people...")
- Partial info: just names and companies, or just profile URLs

**What to extract from user input:**
- Name
- Title / headline
- Company name
- LinkedIn profile URL (if provided)
- Location (if visible)
- Any other context the user mentions

**What to do with partial info:**
- If the user gives only a profile URL: enrich via Google cache (see Phase 3).
- If the user gives only a name + company: enrich via Google cache, then start company research.
- Never ask the user to go back to LinkedIn for more data. Work with what you have + Google cache.

**Deduplication:** Cross-check against the exclusion list from Phase 1. Skip anyone already contacted.

## Phase 3: Enrich and Research (Public Sources Only)

For each contact, enrich missing data and research their company using **only public sources**. Never open LinkedIn directly.

### Google-Cached LinkedIn Enrichment

This is the primary tool for filling gaps in the user's pasted data. Google indexes LinkedIn profiles and shows name, headline, company, and location in the search snippet — **without ever visiting LinkedIn**.

**When to use:** For every contact where you're missing title, company, location, or profile URL.

**How it works:**

```bash
# If you have a name + company:
openclaw browser navigate "https://www.google.com/search?q=site%3Alinkedin.com%2Fin+%22<Name>%22+%22<Company>%22" --browser-profile openclaw
openclaw browser snapshot --browser-profile openclaw

# If you have only a profile URL slug:
openclaw browser navigate "https://www.google.com/search?q=site%3Alinkedin.com%2Fin%2F<slug>" --browser-profile openclaw
openclaw browser snapshot --browser-profile openclaw

# If you want to find more decision makers at a qualified company:
openclaw browser navigate "https://www.google.com/search?q=site%3Alinkedin.com%2Fin+%22<Company>%22+%22CTO%22+OR+%22founder%22+OR+%22VP%22" --browser-profile openclaw
openclaw browser snapshot --browser-profile openclaw
```

**What you get from Google snippets (without visiting LinkedIn):**
- Full name
- Headline (usually title + company)
- Location (city, country)
- Profile URL
- Sometimes first ~200 chars of About section

**What you do NOT get (and that's fine):**
- Full work history
- Connections
- Contact info
- Full activity feed

**This is enough.** Name + title + company + location is all you need for scoring and outreach drafting. The `[Company Detail]` for outreach comes from the company website and Google searches about the person — not from their LinkedIn profile.

**Important:** Never click through to the LinkedIn profile from Google results. Only read the snippet text visible on the Google results page itself.

### Company Website

Use web fetch or the openclaw browser to check the company website:

```bash
openclaw browser navigate "<company-website>" --browser-profile openclaw
openclaw browser snapshot --browser-profile openclaw
```

Check: `/about`, `/team`, `/about-us`, `/careers`, `/pricing`, `/blog`

**Green flags (general):**
- Professional site, clear product, customer logos/case studies
- Active blog (<3 months), hiring page with open roles, pricing page

**Green flags (strong — from outreach learnings):**
- AI agents / autonomous workflows are the **core product** (not a feature)
- Founder talks publicly about agent reliability, hallucination, context, eval
- Company has raised seed-Series B in the last 18 months
- Product involves RAG, multi-agent, agentic workflows, or LLM orchestration
- Visible customer base (not just "coming soon")

**Red flags:**
- Dead/parked site, no product (just buzzwords), "coming soon", 2+ year old blog
- AI is a bolt-on feature, not the core product
- No visible agent/LLM work — just classical ML or analytics
- Founder has no public presence (no posts, no talks, no blog)

### Crunchbase / Funding

```bash
openclaw browser navigate "https://www.crunchbase.com/organization/<company-slug>" --browser-profile openclaw
openclaw browser snapshot --browser-profile openclaw
```

Extract: funding stage, amount, date, employee count, investors.

### Google the Person

For each contact, search for public content to find the `[Company Detail]` needed for outreach:

```
"<full-name>" "<company>" podcast OR interview OR talk OR blog
"<full-name>" "<company>" site:twitter.com OR site:github.com
"<full-name>" "<company>" site:youtube.com
```

People who speak at conferences, write blog posts, or post on Twitter about the problem space are easier to personalize outreach for and more likely to respond.

### Company Blog

Check the company blog for posts by the contact. Often reveals their interests and current technical focus — this is where you find the `[Company Detail]` that passes the swap test.

### Size Estimation

Use website (team page, careers page) + Crunchbase for employee count. Don't rely on LinkedIn employee count (we're not checking it).

### Company Rating

| Rating | Profile | Action |
|--------|---------|--------|
| A | 5-200 employees, AI-agent-first product, funded/growing, active online | Research further — highest response rate |
| B | 20-500 employees, AI is a significant product line but not sole focus | Research if A-tier is thin |
| C | <5 (too early), >1000 (enterprise), AI is tangential, or stale presence | Skip |

## Phase 4: Score and Rank

### Title Priority

| Tier | Titles | Why |
|------|--------|-----|
| 1 | Founder, CEO, CTO, COO | Own the problem and the budget |
| 2 | VP, SVP, Head of [Function] | Direct authority over team/budget |
| 3 | Director | Influence + context, often closer to the problem |
| 4 | Senior Manager | Only at small companies (<100) where this is effectively director-level |

**Skip:** ICs, analysts, associates, coordinators, interns. "Lead ML Engineer" at a 200+ person company is still an IC — skip unless they're effectively running the team.

### Company Targeting Priority

| Priority | Company type | Size | Why |
|----------|-------------|------|-----|
| 1 (Best) | AI-agent-first startup — agents ARE the product | 5-80 employees | Founder feels the pain, can decide in 5 min |
| 2 | AI platform / infra (eval, observability, orchestration) | 20-200 employees | Adjacent problem space, sees many agent teams |
| 3 | Vertical SaaS actively shipping AI agents | 50-300 employees | Has the problem but may not prioritize it |
| 4 (Skip) | Enterprise with "AI transformation" initiatives | >1000 employees | Too slow, wrong level of access |

### Combined Score (1-5)

| Score | Person | Company | Verdict |
|-------|--------|---------|---------|
| 5 | Tier 1, AI-agent-first, active online | Priority 1 | Interview immediately |
| 4 | Tier 1-2, relevant domain, agents are core | Priority 1 or 2 | Strong candidate |
| 3 | Tier 1-2, somewhat relevant, AI is a feature | Priority 2 or 3 | Worth reaching out |
| 2 | Right title wrong domain, or right domain but IC | Priority 3 | Only if pipeline is thin |
| 1 | IC, enterprise, or no visible agent work | Priority 4 | Do not contact |

**Disqualify (omit from CSV):**
- ICs at large companies
- Dead company websites
- Role tenure <3 months
- Companies where AI/agents are not core
- Anyone on the exclusion list from Phase 1

## Phase 5: Draft Outreach (A/B Testing Framework)

For contacts scored 3+, strictly generate TWO distinct outreach variations based on [references/outreach-templates.md](references/outreach-templates.md). Read that file before drafting.

### Hard Enforcement Rules

These are non-negotiable. If a draft violates any of them, it is a failure. Regenerate.

**Rule 1 — Personal Hook, Not Company Description:**
The opening MUST reference something the person *said, wrote, or publicly decided*. NEVER describe what their company does, how big they are, who their customers are, what their tech stack is, or what stage they are at. They founded it. They live it every day. Telling them facts about their own company is condescending.

BANNED OPENERS (all variations of telling them what they already know):
- FAIL: "Synthflow processes 65M voice calls" → describing their scale
- FAIL: "You build AI agents for contact centers" → describing their product
- FAIL: "ihr verarbeitet 65 Millionen Calls und habt nach der Series A noch mehr Volumen vor euch" → describing their scale AND funding
- FAIL: "Brand Eins schrieb über dich als Mitverantwortlichen für das DSGVO-konforme Langdock-Stack" → describing their tech stack
- FAIL: "Cognigy powers enterprise CX agents for Fortune 500s" → describing their customers
- FAIL: "Nexus lets non-technical teams build agents" → describing their value prop

CORRECT OPENERS (reference something they personally said or decided):
- PASS: "du hast beim SaaStock erwähnt, dass die Qualitätsmessung im letzten Schritt das eigentliche Problem ist" → references what they said
- PASS: "your LinkedIn post about proving prompt changes to stakeholders hit home" → references what they wrote
- PASS: "ihr habt euch bewusst für EU-Infrastruktur entschieden statt US-Cloud" → references a specific decision they made (not what the company does)

If you cannot find something they personally said, wrote, or decided, DO NOT SEND. Use a fallback contact where you do have a personal hook.

**Rule 2 — Honest Framing, No Fake Credibility:**
NEVER say "my 20 teams", "the teams I work with", or imply you have clients or a consultancy. You are having research conversations with founders. Say "ich spreche gerade mit ein paar Gründern darüber" or "I've been talking to a few founders about this." That is true from the first conversation.

**Rule 3 — Forward-Selling Arbitrage:**
End with the trade: offer to share what you are hearing from other founders in exchange for their perspective. Do not quantify it falsely. "Ich teile dir gerne, was ich höre" is enough. Honest and open.

**Rule 4 — 40-Word Ceiling:**
Maximum 3-4 sentences. Maximum 40 words total. Cut everything that is not load-bearing.

**Rule 5 — Flat, Normal Tone:**
Write like a normal person texting a peer. No marketing verbs, no cool-sounding language, no words that try to sound energetic ("jagt durch", "spannend", "krass", "revolutioniert"). Slightly boring is correct. Authenticity beats style.
Avoid words that sound negative or accusatory in German: "betonst du überall", "rumklicken", "herumexperimentieren". Re-read each draft and ask: does any word make the recipient feel criticized or looked down on? If yes, rewrite.
Avoid words that minimize their writing or work: "blurb", "snippet", "little post". Treat what they wrote as something worth taking seriously.

**Rule 6 — One Language Per Message:**
Each message must be entirely in one language. German for DACH contacts, English otherwise. Do not mix. The only exception is proper nouns, product names, and established technical terms (e.g. "Prompt", "RAG", "Eval") that have no natural German equivalent.

**Rule 7 — No Em-Dashes (—):** Use commas or periods.

**Rule 8 — No Disclaimers:** Drop "kein Pitch", "not selling", "rein explorativ". If the message is interesting it will not read as a pitch.

**Rule 9 — Always add a source line with URL below each draft:**
After every generated message, add a line starting with "Quelle:" (German) or "Source:" (English) that provides the full URL where the hook information comes from.
- If the hook comes from a LinkedIn post: provide the full LinkedIn post URL.
- If it comes from an interview or article: provide the full article URL.
- If it comes from a company website observation: provide the exact page URL.

**CRITICAL: If you cannot provide a full, clickable URL, DO NOT generate that draft.** Mark it as "SKIP - no verifiable source found" and move to the next contact. "VERIFY NEEDED:" is not acceptable. The user should not have to hunt for sources. Either you have a URL or you skip the contact.

Example (acceptable):
```
Quelle: https://www.linkedin.com/posts/lennard-schmidt_langdock-maus-prompt-regression-activity-123456789
```
```
Source: https://www.businessinsider.com/langdock-growth-2026-02
```

Example (not acceptable - skip this contact instead):
```
VERIFY NEEDED: Hakob mentioned "last mile" problem at SaaStock
```

### Variations

Generate these two variations for every contact:
- **Winkel A (The Reality Check):** Based on Template 1. Provokes a reaction about a specific, ugly bottleneck.
- **Winkel B (The Contrarian):** Based on Template 3. Poses a counter-intuitive market observation.

Output both drafts in the JSON under `outreach_draft_A` and `outreach_draft_B`. Add `source_A` and `source_B` fields with the verification sources.

**Language:** Default to German for DACH-region contacts, English otherwise. Ask user if unclear.

## Phase 6: Generate CSV

```bash
python3 ~/.openclaw/skills/linkedin-research/scripts/generate_csv.py \
  --output ~/.openclaw/workspace/linkedin_research_$(date +%Y-%m-%d).csv \
  --data '<JSON array>'
```

Options: `--min-score 3`, `--append`.

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
  "outreach_draft_A": "Hi Jane, since Acme ships async evals for enterprise pipelines. Solved regression testing on prompt updates yet or still manual diffs? Mapping this across 20 teams, insight briefing comes back next week.",
  "outreach_draft_B": "Hi Jane, since Acme ships async evals. Everyone obsesses over latency, but my data from 20 teams shows regression on prompt updates is the real blocker. Am I wrong? Happy to share the briefing."
}
```

## Tips

- **Google `site:linkedin.com/in` is your best friend** — gets profile URLs and titles without logging into LinkedIn
- **Company-first saves time:** Qualifying 20 companies (5 min each via their website) then finding 1-2 people each is faster than researching people one by one
- **Sales Navigator** (if available) has better filters: `linkedin.com/sales/search/people`
- **Boolean search:** `"VP Engineering" AND (SaaS OR "B2B") NOT "looking for"`
- **Batch by company:** Find one good person → ask the user if they see more relevant contacts at the same company
- **2nd connections** are warm intro opportunities — if the user mentions mutual connections, prioritize those contacts
