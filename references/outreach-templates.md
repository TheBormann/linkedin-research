# Outreach Scripts (High-Status)

**Strategy:** Do not ask for a meeting. Ask a question that provokes a reaction. If they reply, *then* you suggest a call.

## Template 1: The "Reality Check" (Phase 1 Workhorse)

*Use when: You found a founder building agents who talks about reliability/evals (Green Flag).*
*Best for: Tier 3 / early-stage founders. They are technical and insecure — they want to prove they're doing it right or vent that it's broken.*

**Why it works:** It questions their competence ("Are you actually trusting your auto-evals?"). That provokes a response — either defensive ("we solved that") or honest ("it's a mess").

**The trap:** If `[Specific Pain]` is generic (e.g., "hallucinations"), you will be ignored. Use the specific, ugly details from your research: "context drifting at 4k tokens", not "AI reliability issues."

**Strategic use:** This is your intelligence-gathering weapon. If 5 founders tell you "we don't trust auto-evals because of X," then X becomes the ammunition for Template 2.

**Subject:** The [Specific Pain] reality at [Company]

### English

Hi [Name],

I saw you're shipping agents for [Use Case]. I've been tracking how teams handle [Specific Pain, e.g., Context Drifting] at that scale.

Most founders tell me they just [Status Quo, e.g., manually review logs], but that feels unscalable.

Are you guys actually trusting your auto-evals yet, or is it still a manual grind? Just looking for a reality check from someone actually shipping.

### Deutsch

Hi [Name],

ich sehe, dass ihr Agents für [Use Case] baut.

Bei den meisten Teams in eurem Stadium bricht irgendwann [Specific Pain] zusammen. Viele versuchen das mit [Status Quo] zu fixen, aber das skaliert eigentlich null.

Vertraut ihr euren Auto-Evals da schon wirklich, oder ist das bei euch auch noch viel manuelle Arbeit? Kurzer Reality-Check wäre super.

---

## Template 2: The "Pattern Match" (The Bridge to Credibility)

*Use when: You want to validate a specific bottleneck (e.g., cost or latency).*
*Best for: VPs/Heads of Engineering at 20-500 person companies. They fear missing market patterns their peers already see.*

**Why it works:** It implies you have a bird's-eye view of the market that they don't. VPs are competitive — they need to know if they're behind.

**The trap:** The `[Number]` variable. If you say "teams hit a wall at 500 users" and the reality is 5,000, you have revealed yourself as an outsider who is guessing. You CANNOT guess this number. You must get it from the Phase 1 interviews. This is why Template 1 comes first — it gives you the real numbers for Template 2.

**Subject:** Question re: [Topic] bottlenecks

### English

Hi [Name],

I'm seeing a weird pattern with teams scaling [Topic]. They usually hit a wall at [Number] users because [Current Solution] starts costing too much [Time/Money].

Is [Company] seeing that friction yet, or did you manage to bypass it?

(Not selling anything, just trying to see if my data is skewed).

### Deutsch

Hi [Name],

ich sehe gerade ein Muster bei Teams, die [Topic] skalieren. Ab [Number] Usern wird [Current Solution] meistens extrem teuer/langsam.

Merkt ihr das bei [Company] auch schon, oder habt ihr das umschifft?

(Kein Pitch, versuche nur meine Daten abzugleichen).

---

## Template 3: The "Contrarian" (The Boss Fight)

*Use this for the "Conversational Disagreement" — the only template that works for top founders.*
*Best for: Tier 1 founders (CEO/CTO of scaled companies). They are bored by "problems." They are interested in secrets and counter-intuitive truths.*

**Why it works:** It doesn't ask for time. It offers an intellectual challenge. Top founders can't resist correcting someone who is interestingly wrong.

**The trap:** This is the "earned secret." If your `[Opposite Belief]` is just a slightly different opinion, you look arrogant. It must be a counter-narrative supported by real data from Phase 1 and 2.
- Bad: "I think manual review is better." (Boring, obvious)
- Good: "Everyone is optimizing for latency, but my data shows retention bleeds out due to context drift regardless of speed." (Insight backed by data)

**Subject:** Your take on [Controversial Topic]

### English

Hi [Name],

I saw your post about [Topic]. Everyone seems to think [Common Belief] is the answer, but looking at the failure rates, I think [Opposite Belief] is actually the bottleneck.

Am I crazy, or are you seeing that too?

### Deutsch

Hi [Name],

ich habe deinen Post zu [Topic] gesehen. Fast alle setzen da ja gerade auf [Common Belief], aber wenn man sich die Error-Rates ansieht, scheint mir [Opposite Belief] eigentlich das größere Problem.

Bin ich da auf dem Holzweg oder siehst du das ähnlich?

---

## Template 4: The Follow-Up (One only)

*Send 5 days later if no reply.*

### English

Bumping this—just curious if [Specific Problem] is even in your top 10 headaches right now. If not, I'll stop barking up this tree.

### Deutsch

Kurzes Follow-up – ist [Specific Problem] bei euch überhaupt ein relevantes Thema gerade? Falls nicht, hake ich das ab.

---

## The Escalation Sequence

These templates are a ladder. You climb it with data from each step.

1. **Send Template 1** to 10 Tier 3 / early-stage founders.
2. **Measure reply rate.**
   - **< 20% reply rate:** Your `[Specific Pain]` is wrong. Do NOT proceed to Template 2. Go back, pick a different pain point, and re-test Template 1.
   - **> 20% reply rate:** You found a nerve. Harvest the specific failure modes and numbers from these conversations.
3. **Load Template 2** with the real data from Template 1 replies. The `[Number]`, `[Current Solution]`, and `[Time/Money]` placeholders must come from actual quotes and data points — never from guessing.
4. **Send Template 2** to 10 mid-tier VPs/Heads of.
5. **Load Template 3** with the contrarian insight that emerged from Template 1 + 2 conversations. Your `[Opposite Belief]` must be something that surprised YOU during the research — if it didn't surprise you, it won't interest a top founder.
6. **Send Template 3** only to founders whose specific public content you can reference.

**The templates are empty guns. The ammunition is your research. If you skip Phase 1, Templates 2 and 3 will backfire.**

## Rules

1. **Never ask for a meeting in the first message.** Ask a binary question that they can answer in one sentence.
2. **No Calendly link in cold outreach.** The link goes in a follow-up message AFTER they've shown interest.
3. **Fill every placeholder with specific details from your research.** Generic text = instant delete. If a placeholder could apply to 100 founders, it is too generic.
4. **Never say "no pitch", "not selling", or defensive disclaimers.** If the message is interesting, they won't think it's a pitch. If it's boring, the disclaimer won't save it.
5. **One follow-up only.** If they don't reply to the follow-up, move on.
6. **Default to English for AI/dev/engineering spaces**, even in DACH. German only for non-technical founders or German-only profiles.
7. **Never send Template 2 before completing Template 1 interviews.** The numbers must be real.
8. **Never send Template 3 without a genuine contrarian insight.** If you can't finish the sentence "Everyone thinks X, but my data shows Y" with real data, you are not ready for Template 3.
