---
name: forensic-read
description: Read any document the way a detective reads a witness statement — surface what it is NOT saying. Unlike a summarizer (which tells you what a text says), this skill exposes the subtext: hedging and weasel words, conspicuous omissions, buried leads, frequency tells, tone shifts, and non-answers. Use it on earnings calls, shareholder letters, job postings, press releases, politician statements, news articles, performance reviews, legal language, and the email that's clearly avoiding something. Trigger on phrases like "what are they really saying?", "read between the lines", "decode this earnings call", "is this a red flag?", "what's this not telling me?", "what are they hiding?", or any request to analyze the subtext, spin, or evasion in a document rather than just summarize it.
---

# Forensic Read

A summary tells you what a document *says*. A forensic read tells you what it's **avoiding** saying.

Treat the text like a witness statement: assume every word was chosen on purpose, and that the choices are evidence. The goal is not paranoia — it's noticing the gap between what was stated, what was implied, and what was conspicuously left out.

## Core principle

> Don't ask "what does this document say?"
> Ask "what would I expect an honest, complete version to contain — and what's missing or hedged?"

## The read process

1. **Surface read.** State plainly what the document claims, in one or two sentences. This is the baseline everything else is measured against.
2. **Collect evidence.** Go through the text for the tells below. Quote them. (For longer texts, run `scripts/scan.py` first — see below — to ground this in numbers.)
3. **Find the gap.** What would a complete, candid version include that this one doesn't? Missing numbers, unnamed actors, undated promises, unanswered questions.
4. **Separate evidence from inference.** Facts about the text (it hedges, it omits the salary) are evidence. What you think it *means* is inference. Always label which is which.
5. **Render the bottom line.** One honest paragraph: what's really going on, and how confident you are.

## What to hunt for

- **Hedging / weasel words** — "we believe", "aims to", "up to", "many", "generally". Density of deniability.
- **Conspicuous omissions** — the number that should be there and isn't; the question dodged; the actor never named.
- **Buried leads** — the most important fact placed in paragraph nine, in a subordinate clause.
- **Frequency tells** — what gets repeated obsessively (reassurance is often anxiety).
- **Tone shifts** — where confident prose suddenly goes vague or passive. That seam is usually where the body is buried.
- **Non-answers** — answering a question that wasn't asked; reframing instead of responding.
- **Passive voice that hides the actor** — "mistakes were made" by whom?

## Evidence scanner (bundled)

For anything longer than a few paragraphs, run the bundled scanner first — it quantifies the tells so the read is grounded in numbers, not vibes:

```bash
python scripts/scan.py earnings_transcript.txt
# or pipe it:
cat statement.txt | python scripts/scan.py -
```

It reports **emphasis** (what gets repeated), **hedging density** (weasel words per 1,000 words, flagged above a threshold), and **passive-voice signals** (where the actor is hidden). Pure Python 3, no dependencies. The scanner collects evidence; the interpretation stays with you and Claude.

## Output format

Lead with the read, keep it tight:

1. **Surface read** — what it claims (1–2 sentences).
2. **The subtext** — what's actually going on (2–3 sentences).
3. **Tells** — bullets, each a quoted phrase → what it signals.
4. **Conspicuously missing** — what an honest version would include but this omits.
5. **Bottom line** — the verdict + your confidence level.

## A note on honesty (important)

This skill is calibrated **not** to manufacture conspiracy. A forensic read that finds nothing suspicious is a valid, valuable result — say "this reads as clean and direct" when it does. Distinguish evidence (facts about the text) from inference (your interpretation) so the reader always knows which is which. Don't invent motive the text doesn't support.

## Worked example

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
> - "Unlimited PTO" → often *less* time off in practice, since nothing accrues
>
> **Conspicuously missing:** Any salary range, team size, reporting line — or a description of what the work actually *is*.
>
> **Bottom line:** "Fast-paced family" + no salary number is a yellow flag. Ask hard questions about scope and comp before investing time. *(Confidence: medium-high — these are common patterns, not proof.)*

## Anti-patterns to avoid

- Manufacturing a conspiracy where the text is simply clear and honest
- Presenting inference as if it were evidence
- Summarizing instead of reading the subtext (that's a different job)
- Over-reading a single word into a grand theory

---

> Part of the [clear-eye](https://github.com/3243dwon/clear-eye) pack — Claude skills for seeing what others miss.
