#!/usr/bin/env python3
"""
forensic-scan — evidence collector for the forensic-read skill.

Scans a text document and surfaces the quantitative tells a forensic read
relies on: word-frequency emphasis, hedging/weasel language, passive-voice
markers, and uncertainty signals. The skill uses this output as evidence —
it does NOT replace the qualitative read, it grounds it in numbers.

Usage:
    python scan.py <file.txt>
    cat transcript.txt | python scan.py -
"""

import sys
import re
from collections import Counter

# Exit quietly if output is piped into something that closes early (e.g. `| head`)
try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (ImportError, AttributeError):
    pass

# Hedging / low-confidence / deniability language
HEDGE_TERMS = [
    "believe", "expect", "anticipate", "aim", "aims", "intend", "hope",
    "should", "could", "may", "might", "potentially", "possibly",
    "approximately", "roughly", "around", "up to", "as much as",
    "many", "some", "several", "certain", "various", "a number of",
    "generally", "typically", "largely", "mostly", "in part",
    "we think", "we feel", "it seems", "appears to", "tends to",
]

# Passive-voice signal (rough heuristic: "was/were/been + past participle-ish")
PASSIVE_RE = re.compile(
    r"\b(was|were|been|being|is|are)\s+\w+(ed|en)\b", re.IGNORECASE
)

# Common stopwords to exclude from the emphasis count
STOPWORDS = set("""
a an the and or but if then else of to in on at by for with from as is are was
were be been being this that these those it its we our you your they their he
she his her i me my mine us them not no nor so than too very can will would
shall should may might must do does did have has had what which who whom whose
about into over under again further once here there when where why how all any
both each few more most other such only own same s t just don now
""".split())


def read_input(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def emphasis(text, top=12):
    words = re.findall(r"[A-Za-z][A-Za-z'-]+", text.lower())
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    return Counter(words).most_common(top)


def hedges(text):
    low = text.lower()
    found = []
    for term in HEDGE_TERMS:
        n = low.count(term)
        if n:
            found.append((term, n))
    return sorted(found, key=lambda x: -x[1])


def passives(text):
    return [m.group(0) for m in PASSIVE_RE.finditer(text)]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    text = read_input(sys.argv[1])
    words_total = len(re.findall(r"\w+", text))

    print("=" * 60)
    print("FORENSIC SCAN — evidence for the read")
    print("=" * 60)
    print(f"Total words: {words_total}\n")

    print("— EMPHASIS (what gets repeated) —")
    print("  High repetition can signal what the writer is steering toward,")
    print("  or anxiety about a particular theme.\n")
    for word, count in emphasis(text):
        bar = "█" * min(count, 30)
        print(f"  {word:<18} {count:>3}  {bar}")

    print("\n— HEDGING / WEASEL LANGUAGE —")
    print("  Density of deniability and low-confidence phrasing.\n")
    h = hedges(text)
    if h:
        hedge_total = sum(n for _, n in h)
        for term, count in h:
            print(f"  \"{term}\"{' ' * (20 - len(term))} {count}")
        rate = (hedge_total / words_total * 1000) if words_total else 0
        print(f"\n  Total hedge instances: {hedge_total}  "
              f"({rate:.1f} per 1,000 words)")
        if rate > 15:
            print("  ⚠  Elevated hedging density — read confidence claims skeptically.")
    else:
        print("  None detected. (Unusually direct — itself worth noting.)")

    p = passives(text)
    print("\n— PASSIVE-VOICE SIGNALS —")
    print(f"  {len(p)} likely passive constructions "
          f"(actors hidden behind 'was/were + verb').")
    if p[:6]:
        print("  e.g. " + ", ".join(f'"{m}"' for m in p[:6]))

    print("\n" + "=" * 60)
    print("Feed these numbers into the forensic read as EVIDENCE.")
    print("The interpretation is still the human + Claude's job.")
    print("=" * 60)


if __name__ == "__main__":
    main()
