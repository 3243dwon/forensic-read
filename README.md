# 🔍 forensic-read

> A Claude skill that reads between the lines of any document — and surfaces what's **not** being said.

A summary tells you what a document says. `forensic-read` tells you what it's *avoiding* saying: the hedging, the deflections, the conspicuous omissions, the buried leads, and the word choices that give the game away.

It reads a text like a detective reads a witness statement — assuming every word was chosen carefully, and that the choices are evidence.

---

## See it work

**Input** — a job posting:

> "Join our fast-paced, dynamic team! We're looking for a rockstar analyst who thrives under pressure and wears many hats. Competitive salary. Must be willing to go above and beyond. We're like a family here. Unlimited PTO."

**Output:**

> **Surface read:** A growing startup hiring a versatile analyst with good perks.
>
> **The subtext:** A small, under-resourced team expecting one person to do the work of several — with culture language standing in for compensation and structure.
>
> **Tells:**
> - "Wears many hats" → the role is undefined; you'll be doing three jobs
> - "Competitive salary" with no number → almost always below market
> - "We're like a family" → boundary-blurring; expect after-hours asks framed as loyalty
> - "Unlimited PTO" → in practice often *less* time off, since nothing accrues
>
> **Conspicuously missing:** Any salary range, team size, reporting line — or any description of what the work actually *is*.
>
> **Bottom line:** "Fast-paced family" + no salary number is a yellow flag. Ask hard questions about scope and comp before investing time.

---

## What it's for

Any document where the subtext beats the summary:

**Earnings calls · shareholder letters · job postings · press releases · politician statements · news articles · performance reviews · legal language · the email that's clearly avoiding something**

It hunts for: hedging & weasel words, conspicuous omissions, frequency tells (what gets repeated obsessively), buried leads, tone shifts, and non-answers.

---

## How to use it

Just ask Claude naturally:

- *"What are they really saying here?"*
- *"Decode this earnings call"*
- *"Is this job posting a red flag?"*
- *"Read between the lines of this email"*

---

## A note on honesty

The skill is calibrated **not** to manufacture conspiracy. If a document is clean and honest, it says so — a forensic read that finds nothing suspicious is a valid result. It also separates evidence (facts about the text) from inference (interpretation), so you always know which is which.

---

## Evidence scanner (bundled)

Ships with `scripts/scan.py` — a zero-dependency Python tool that quantifies the tells a forensic read relies on, so the read is grounded in numbers rather than vibes:

- **Emphasis** — what gets repeated (and how obsessively)
- **Hedging density** — weasel words per 1,000 words, with a flag above threshold
- **Passive-voice signals** — where the actor is hidden

```bash
python scripts/scan.py earnings_transcript.txt
# or pipe it:
cat statement.txt | python scripts/scan.py -
```

It collects evidence; the interpretation stays with you and Claude.

---

## Install

### Drop-in
```
your-skills-directory/
└── forensic-read/
    ├── SKILL.md
    └── scripts/
```

### Claude Code
```bash
git clone https://github.com/3243dwon/forensic-read.git
cp -r forensic-read ~/.claude/skills/
```

Works across **Claude.ai, Claude Code, and the Claude API**; the `SKILL.md` format is portable to other agents (Cursor, Codex, Gemini CLI). The scanner needs only Python 3.

> Part of the [clear-eye](https://github.com/3243dwon/clear-eye) pack — Claude skills for seeing what others miss.

---

## License

MIT — use it, fork it, build on it.
