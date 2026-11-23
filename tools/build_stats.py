"""assets/stats-{dark,light}.svg - a stats card generated from the GitHub API.

Written because the alternatives are both unreliable. The public github-readme-stats
instance returns 503 for long stretches, and streak-stats.demolab.com takes 10-30s on a
cold URL, which is longer than GitHub's camo proxy will wait. Both put a broken image on
the profile when they fail. This one is rendered by a GitHub Action into the `output`
branch, so the profile only ever loads an SVG that GitHub itself is serving.

Run in CI with GITHUB_TOKEN, or locally - it falls back to `gh auth token`.

Only PUBLIC repositories are counted, deliberately. A local run with a `repo`-scoped
token can see private repositories that the Actions token cannot, and the card would
then report different numbers depending on where it was built.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request

import design as D
import fonts
from design import SIZE, T, w

W, H = 1180, 344
BAR = 34
USER = "Rohit-ATS"

# Markup and generated files are excluded from the language mix. Counting them makes a
# TypeScript-and-Python profile look like a web-design one - CSS and HTML were 8.7% of
# bytes at time of writing, none of it the work the repos are actually about.
SKIP_LANGS = {"HTML", "CSS", "SCSS", "MDX", "Handlebars", "Dockerfile", "Makefile"}

QUERY = """
{ user(login: "%s") {
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes {
        name stargazerCount forkCount
        languages(first: 15, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalRepositoryContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  } }
""" % USER


def token() -> str:
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if t:
        return t
    return subprocess.run(["gh", "auth", "token"], capture_output=True,
                          text=True, check=True).stdout.strip()


def fetch() -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY}).encode(),
        headers={"Authorization": f"bearer {token()}",
                 "Content-Type": "application/json",
                 "User-Agent": "rohit-profile-stats"})
    with urllib.request.urlopen(req, timeout=45) as r:
        body = json.load(r)
    if "errors" in body:
        raise SystemExit(f"GraphQL errors: {body['errors']}")
    return body["data"]["user"]


def streaks(cal: dict) -> tuple[int, int]:
    """Current and longest daily streak from the contribution calendar.

    The current streak deliberately skips a zero on the most recent day: the day is not
    over yet, and counting it as a break resets the number every morning."""
    days = [d["contributionCount"]
            for w in cal["weeks"] for d in w["contributionDays"]]
    longest = run = 0
    for n in days:
        run = run + 1 if n > 0 else 0
        longest = max(longest, run)
    tail = days[:-1] if days and days[-1] == 0 else days
    current = 0
    for n in reversed(tail):
        if n == 0:
            break
        current += 1
    return current, longest


def digest(u: dict) -> dict:
    repos = u["repositories"]["nodes"]
    cc = u["contributionsCollection"]
    langs: dict[str, int] = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            if n in SKIP_LANGS:
                continue
            langs[n] = langs.get(n, 0) + e["size"]
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    cur, longest = streaks(cc["contributionCalendar"])
    return dict(
        contributions=cc["contributionCalendar"]["totalContributions"],
        streak=cur,
        longest=longest,
        commits=cc["totalCommitContributions"],
        prs=cc["totalPullRequestContributions"],
        issues=cc["totalIssueContributions"],
        repos=u["repositories"]["totalCount"],
        stars=sum(r["stargazerCount"] for r in repos),
        followers=u["followers"]["totalCount"],
        langs=[(n, v / total * 100) for n, v in top],
    )


LANG_COLOUR = {
    # A language's own colour is how it is recognised at a glance, so this is the one
    # place colour still earns its keep. Muted toward the ground so four bars read as
    # data rather than as decoration.
    "Python": "#5B7FA6", "TypeScript": "#4E76B0", "JavaScript": "#B3A24A",
    "C++": "#A9647A", "Dart": "#3E8C88", "Shell": "#6E9159", "Swift": "#B0705A",
    "Kotlin": "#7E6FA6", "Go": "#4C8494", "Rust": "#9A8069", "Java": "#8A6A4C",
    "Ruby": "#A15A56", "C": "#6E7681", "PLpgSQL": "#4A6E92",
}

SMALL = [("COMMITS", "commits", None), ("PULL REQUESTS", "prs", None),
         ("CURRENT STREAK", "streak", "d"), ("LONGEST STREAK", "longest", "d")]
NOTE = "public repositories  ·  regenerated twice daily"


def build(theme: str, d: dict) -> str:
    """Activity as a dot-matrix readout.

    The headline figure is drawn in the same material as the portrait - a field of dots
    on a 5x7 grid, unlit cells included - so the card belongs to the same page rather
    than looking like a chart library dropped next to it. The supporting figures are set
    in type, because six identical dot numbers would flatten the hierarchy that makes
    the headline worth looking at.

    Stars and followers are deliberately absent: on an account opened in 2024 they
    measure reach and age rather than work, the same argument that makes hide_rank the
    right call on a github-readme-stats card.
    """
    c = D.THEMES[theme]
    hero = f"{d['contributions']:,}"

    chars = fonts.charset("".join(l for l, _, _ in SMALL) + NOTE
                          + "ACTIVITYLANGUAGECONTRIBUTIONS IN THE LAST YEAR"
                          + "by bytes, markup excludeddays"
                          + "".join(n for n, _ in d["langs"]) + "%.,")
    css, _ = fonts.embed_faces(chars)

    o = [D.svg_open(W, H, f"GitHub activity for {USER}",
                    "Contributions, commits, pull requests and streaks, with the "
                    "language mix by bytes.", css),
         D.defs(c),
         D.page(W, H, c)]

    PAD = 64
    o.append(D.eyebrow(PAD, 48, "ACTIVITY", c))
    o.append(T(W - PAD, 48, NOTE, size=SIZE["micro"], fill=c["text3"], anchor="end"))
    o.append(D.dot_rule(PAD, 66, W - PAD * 2, c, pitch=8, r=1.5, fade=False))

    # ---- the headline figure, as lit and unlit cells
    o.append(D.glow(PAD + 110, 128, 200))
    marks, _ = D.dot_number(PAD, 100, hero, pitch=10.5, r=3.7,
                            fill=c["ink"], dim=c["line"])
    o.append(marks)
    o.append(T(PAD, 196, "CONTRIBUTIONS IN THE LAST YEAR", size=SIZE["micro"],
               weight=700, fill=c["text3"], track=0.24))

    # ---- language mix, right of the headline
    LX = 640
    o.append(D.eyebrow(LX, 100, "LANGUAGE", c, colour=c["ink2"]))
    o.append(T(W - PAD, 100, "by bytes, markup excluded", size=SIZE["micro"],
               fill=c["text3"], anchor="end"))
    bar_x = LX + 132
    bar_w = W - PAD - 66 - bar_x
    for i, (name, pct) in enumerate(d["langs"][:4]):
        y = 136 + i * 32
        o.append(T(LX, y + 4, name, size=SIZE["small"], fill=c["text2"]))
        o.append(D.dot_bar(bar_x, y, bar_w, pct / 100, c, pitch=8, r=2.7,
                           fill=LANG_COLOUR.get(name, c["ink2"]), begin=0.15 * i))
        o.append(T(W - PAD, y + 4, f"{pct:.1f}%", size=SIZE["small"], mono=True,
                   fill=c["text3"], anchor="end"))

    # ---- supporting figures, across the foot
    o.append(D.dot_rule(PAD, 246, W - PAD * 2, c, pitch=8, r=1.5, fade=False))
    colw = (W - PAD * 2) / len(SMALL)
    for i, (label, key, unit) in enumerate(SMALL):
        x = PAD + i * colw
        val = f"{d[key]:,}"
        o.append(T(x, 300, val, size=SIZE["head"], weight=300, fill=c["text"],
                   track=-0.01))
        if unit:
            o.append(T(x + w(val, size=SIZE["head"], weight=300, track=-0.01) + 6, 300,
                       unit, size=SIZE["small"], fill=c["text3"]))
        o.append(T(x, 322, label, size=SIZE["micro"], weight=700, fill=c["text3"],
                   track=0.2))

    o.append("</svg>")
    return "".join(o)


def main() -> None:
    out = sys.argv[1] if len(sys.argv) > 1 else "../assets"
    d = digest(fetch())
    print("stats:", {k: v for k, v in d.items() if k != "langs"})
    print("langs:", [(n, round(pc, 1)) for n, pc in d["langs"]])
    os.makedirs(out, exist_ok=True)
    for theme in ("dark", "light"):
        svg = build(theme, d)
        path = os.path.join(out, f"stats-{theme}.svg")
        open(path, "w", encoding="utf-8").write(svg)
        print(f"{path}: {len(svg.encode()) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
