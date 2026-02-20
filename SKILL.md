---
name: outreach-research
description: Generate targeted LinkedIn search queries based on problem space and outreach phase, then research and qualify contacts for problem discovery outreach. User tells the skill what problem they're exploring and what phase they're in (problem discovery, validation, or decision). Skill generates tailored search queries, then handles company research via public sources, Google-cached LinkedIn enrichment, scoring, and A/B outreach draft generation. Triggers on "find people to interview about X", "I'm exploring Y problem", "who should I talk to about Z problem", "generate search queries for [problem]", "qualify these contacts", "draft outreach for these people".
---

# Outreach Research

Generate persona-specific LinkedIn search queries, qualify contacts, and generate A/B-tested outreach drafts. The user tells the skill their problem space and outreach phase. The skill generates search queries tailored to who actually feels the pain (not just who owns the company). User manually browses LinkedIn using those queries and pastes contact info. The skill does everything else: company research via public sources, scoring, and draft generation.

**Core principle: zero LinkedIn automation.** All LinkedIn activity is done by the user manually. The skill never touches LinkedIn — it researches companies through websites, Crunchbase, Google, and other public sources. This keeps the user's LinkedIn account safe.

## Phase 1: Research Brief & Search Query Generation

**IMPORTANT: When the user invokes this skill, the first thing you do is ask them about their problem space and outreach phase, then immediately generate tailored LinkedIn search queries for them to use.**

Collect from the user:

- **Problem space**: What problem are they exploring? (e.g., "SOP handling in Pharma", "sales onboarding at SaaS companies", "AI agent evaluation workflows")
- **Outreach phase**: What phase are they in?
  - **Phase A (Problem Discovery)**: Early exploration, need to understand the pain deeply → target people who FEEL the pain daily
  - **Phase B (Validation)**: Problem understood, validating scope and willingness to solve → target people accountable for the problem
  - **Phase C (Decision)**: Solution direction clear, testing willingness to pay → target budget holders and decision makers
- **Company sweet spot**: Industry, stage, size range (default: 5-200 employees)
- **Geography** (optional): Location constraints
- **Interview goal**: What specific insight do they need?
- **Already contacted** (optional): Names of people they've already reached out to. Parse into a simple exclusion list of `name + company` pairs. Skip these throughout the process.

### Persona Mapping Framework

**The key insight: match search filters to who FEELS the pain, not who OWNS the company.**

Before generating searches, determine:
1. **Who experiences this problem daily?** (the doer)
2. **Who gets blamed when it goes wrong?** (accountability holder)
3. **Who has budget authority to fix it?** (decision maker)

**Persona tiers by phase:**

| **Phase** | **Target Tier** | **Who to Search For** | **Why** |
|-----------|-----------------|----------------------|---------|
| **Phase A (Problem Discovery)** | Tier 1 | Individual contributors, specialists, managers who do the work daily | Deep operational knowledge, specific pain examples, frustrated enough to talk |
| **Phase B (Validation)** | Tier 2 | Directors, Heads of Function, Senior Managers accountable for outcomes | Understand scope + business impact, connect pain to priorities |
| **Phase C (Decision)** | Tier 3 | VPs, C-suite in relevant function | Buying authority, budget allocation, strategic priorities |

**EXCEPTION - Founder-Led Companies (<50 employees):**
When the problem space naturally sits with **founders/CEOs of small companies** (e.g., AI agent tooling, developer tools, early-stage product challenges), search for founders REGARDLESS of phase, but filter by:
- Company size: 5-50 employees (founders still feel operational pain)
- Stage: Seed to Series A (founders still in the weeds)
- Industry match: Their company must work in the problem domain

### Search Query Generation

**After collecting the brief, immediately generate 3-5 LinkedIn search queries tailored to the problem space and phase.**

#### Query Structure Principles

**IMPORTANT: Keep queries BROAD. Over-filtering in the search query returns zero results. Use LinkedIn's UI filters instead.**

**Winning pattern:**
- Search query: 2-3 broad terms maximum
- Refinement: Use LinkedIn's company size, location, industry filters in the UI

**For Problem Spaces in Established Companies (Pharma, Manufacturing, Enterprise):**

```
Phase A (Problem Discovery):
"[Job Title]" [Industry]
Example: "Quality Manager" Pharma

Phase B (Validation):
"Head of [Function]" [Industry]
Example: "Head of Quality" Pharma

Phase C (Decision):
"VP [Function]" [Industry]
Example: "VP Quality" Pharma
```

Then use LinkedIn filters: Company size (50-1000), Location (Germany), etc.

**For Founder-Led Problems (Startups, Tech, AI):**

```
All Phases (target founders at small companies):
founder [Industry/Tech]
Example: founder AI
Example: CEO SaaS

Then use LinkedIn filters: Company size (1-50), Location, Industry
```

#### Example: SOP Handling in Pharma

**User says:** "I'm exploring SOP handling in Pharma companies, Phase A (problem discovery)"

**You generate:**

```
Phase A - Tier 1 (Problem Discovery):

LinkedIn People Search (copy these one by one):
1. "Quality Manager" Pharma
2. "Regulatory Affairs" Pharma
3. "Compliance Manager" Biotech

Then apply these LinkedIn UI filters:
- Company size: 50-1,000 employees
- Location: Germany (or your target region)
- Current company (to filter out job seekers)

Google alternative (no LinkedIn login):
site:linkedin.com/in "Quality Manager" Pharma Germany
```

**Expected results:** 200-500+ profiles per search. Pick 10-15 who have Manager/Director titles and paste their info back.

#### Example: AI Agent Evaluation Workflows

**User says:** "I'm exploring AI agent evaluation workflows, Phase A (problem discovery)"

**You generate:**

```
Phase A - Founders at AI-Agent Companies (5-50 employees):

LinkedIn People Search (copy these one by one):
1. founder AI
2. CEO "machine learning"
3. CTO agent

Then apply these LinkedIn UI filters:
- Company size: 1-50 employees (founders still feel operational pain)
- Industry: Software Development, Internet
- Location: San Francisco, Berlin, London (or your target)

Google alternative (no LinkedIn login):
site:linkedin.com/in founder AI Berlin
site:linkedin.com/in CEO "AI agent" "San Francisco"

**Where to find AI-agent startups:**
- YC W24/S24/W25 batches — filter for AI/agent companies
- EU AI startup lists: Sifted, Tech.eu, HTGF portfolio pages
- Product Hunt launches tagged "AI agent" in last 6 months
- VC portfolios: HTGF, Earlybird, Cherry Ventures, La Famiglia, Accel — filter for AI
- GitHub trending — founders of popular agent frameworks often have startups
```

**Expected results:** 1000+ profiles. Pick 10-15 founders whose companies are building AI agents as core product (not just using AI internally).

#### Example: Sales Onboarding at SaaS Companies

**User says:** "I'm exploring sales onboarding at SaaS companies, Phase B (validation)"

**You generate:**

```
Phase B - Tier 2 (Validation):

LinkedIn People Search (copy these one by one):
1. "Sales Enablement" SaaS
2. "VP Sales" SaaS
3. "Revenue Operations" SaaS

Then apply these LinkedIn UI filters:
- Company size: 50-500 employees (sales teams large enough to have onboarding pain)
- Industry: Software Development
- Location: US, Europe (or your target)

Google alternative:
site:linkedin.com/in "Sales Enablement" SaaS
```

**Expected results:** 500+ profiles. Pick 10-15 who are VP/Director level at B2B SaaS companies.

### When to Default to Founders (Small Companies)

**Use founder searches (regardless of phase) when:**
1. The problem space is inherently a startup/tech problem (AI agents, developer tools, early-stage product decisions, PLG growth, etc.)
2. The user mentions "AI startups", "SaaS companies", "tech companies" without specifying a function
3. The problem requires technical depth + decision authority in one person (only true at <50 employee companies)

**Always add these filters for founder searches:**
- Company size: 5-50 employees (at 50+, founders are too far from operational pain)
- Stage: Seed to Series A (Series B+ founders are in board meetings, not feeling daily pain)

**Do NOT use founder searches when:**
1. The problem sits in a specific department of larger companies (QA in Pharma, Sales Ops in Enterprise SaaS)
2. The user explicitly mentions a non-founder role ("I want to talk to sales managers")
3. The company size is >100 employees (founders are too removed from operational reality)

### Output Format

After collecting the research brief, output:

```markdown
## Search Queries for [Problem Space] - Phase [A/B/C]

**Target Persona:** [Tier 1/2/3 description]
**Why this persona:** [1 sentence explaining why they're the right people to talk to in this phase]

### LinkedIn People Search (copy-paste these):

1. [Query 1]
2. [Query 2]
3. [Query 3]

### Google Site Search (no LinkedIn login needed):

[Google query]

### Filters to Apply on LinkedIn:
- Company size: [range]
- Location: [if specified]
- Industry: [if relevant]
- [Any other relevant filters]

### Additional sourcing ideas:
[If applicable: YC batches, VC portfolios, industry lists, conferences, etc.]

---

**Next step:** Browse these searches, pick 10-15 people who look relevant, and paste their info (name, title, company, LinkedIn URL if available). I'll research their companies and draft personalized outreach.
```

Tell the user to browse these, pick people who look relevant, and paste what they find.

## Phase 2: User Pastes Contacts → Auto-Filter & Prioritize

**CRITICAL: When user pastes contacts, DO NOT ask them for more information. Immediately start enriching and filtering.**

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

**Immediate next step after parsing:**
1. For each contact, enrich via Google cache (see Phase 3) to get missing title/company/location
2. Do quick company research (website check, Crunchbase if available)
3. Apply scoring rules (see Phase 4) to identify high-value contacts (score 3+)
4. Output a filtered list showing:
   - **HIGH PRIORITY (score 4-5):** [Name, Title, Company, why they're high-value]
   - **MEDIUM PRIORITY (score 3):** [Name, Title, Company]
   - **SKIP (score 1-2):** [Name, Company, reason to skip]

5. For HIGH and MEDIUM priority contacts, immediately proceed to Phase 3 (research for personal hooks)

**What to do with partial info:**
- If the user gives only a profile URL: enrich via Google cache
- If the user gives only a name + company: enrich via Google cache, then start company research
- NEVER ask the user to go back to LinkedIn for more data. Work with what you have + Google cache.

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

### Google the Person (CRITICAL FOR OUTREACH HOOKS)

**ALWAYS do this automatically for score 3+ contacts. This is how you find personal hooks without asking the user.**

For each contact, search for public content to find the `[Personal Hook]` needed for outreach:

**Priority 1 - LinkedIn Posts (via Google):**
```
site:linkedin.com/posts/<profile-slug>
site:linkedin.com/feed/update (if recent posts are indexed)
```
LinkedIn posts are the BEST source because they're recent, specific, and show what the person is currently thinking about.

**Priority 2 - Interviews, Podcasts, Talks:**
```
"<full-name>" "<company>" podcast OR interview OR talk
"<full-name>" "<company>" conference OR speaking OR panel
```

**Priority 3 - Twitter/X Posts:**
```
"<full-name>" site:twitter.com OR site:x.com
"<full-name>" "<company>" site:twitter.com
```

**Priority 4 - Company Blog:**
Check the company blog for posts written by the contact. Often reveals their interests and current technical focus.

**Priority 5 - GitHub Activity (for technical founders):**
```
"<full-name>" "<company>" site:github.com
```

### Decision Tree for Personal Hooks

After Googling each HIGH/MEDIUM priority contact:

**IF you find a LinkedIn post, interview quote, talk, or tweet where they discussed the problem space:**
→ Extract the quote/observation
→ Immediately proceed to Phase 5 (draft outreach)
→ Use that quote as the `[Personal Hook]`
→ Include the source URL in citation

**IF you find nothing after Googling but contact is score 4-5 (HIGH PRIORITY):**
→ Tell the user: "**HIGH PRIORITY - NEED MANUAL RESEARCH:** [Name] at [Company] scores [X]/5. No public posts found via Google. Please check their LinkedIn profile manually and paste any relevant posts or quotes they've made about [problem space]."
→ Wait for user input
→ When user pastes content, use it as the hook
→ Source citation: "Quelle: LinkedIn Post (bereitgestellt vom User)" or "Source: LinkedIn post (user-provided)" — NO URL needed

**IF you find nothing and contact is score 3 (MEDIUM PRIORITY):**
→ Mark as "SKIP - no verifiable personal hook found"
→ Move to next contact
→ Do NOT ask user to do manual research for score 3 contacts

**Source citation rules:**
- **You found it via Google:** Include full URL (LinkedIn post, article, podcast, etc.)
- **User provided it manually:** Just note the source type, no URL needed
  - Examples: "Quelle: LinkedIn Post (bereitgestellt vom User)" or "Source: Podcast interview (user-provided)"

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

**Rule 9 — Source citation (flexible based on source):**
After every generated message, add a source line showing where the hook came from.

**If YOU found the hook via Google/public search:**
- Add "Quelle:" (German) or "Source:" (English) with the full URL
- LinkedIn post: full LinkedIn post URL
- Interview/article: full article URL
- Podcast: episode URL or show notes URL

**If USER manually provided the hook (after you asked for manual research):**
- Add "Quelle:" or "Source:" with just the content type, NO URL needed
- Examples:
  - "Quelle: LinkedIn Post (bereitgestellt vom User)"
  - "Source: LinkedIn post (user-provided)"
  - "Quelle: Podcast-Interview (bereitgestellt vom User)"

**If you cannot find a hook via Google:**
- High-relevance (score 4-5): Ask user "HIGH PRIORITY - NEED MANUAL RESEARCH: [Name] at [Company] scores [X]/5. Please check their LinkedIn profile and paste any relevant posts or quotes."
- Medium-relevance (score 3): Skip contact, move to next

Examples (YOU found it):
```
Quelle: https://www.linkedin.com/posts/lennard-schmidt_langdock-prompt-regression-activity-123456789
Source: https://www.businessinsider.com/langdock-growth-2026-02
```

Examples (USER provided it):
```
Quelle: LinkedIn Post (bereitgestellt vom User)
Source: Podcast interview (user-provided)
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
