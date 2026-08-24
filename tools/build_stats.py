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

W, H = 1180, 274
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
    "Python": "#4B8BBE", "TypeScript": "#3178C6", "JavaScript": "#E8C33C",
    "C++": "#F34B7D", "Dart": "#00B4AB", "Shell": "#89E051", "Swift": "#F05138",
    "Kotlin": "#A97BFF", "Go": "#00ADD8", "Rust": "#DEA584", "Java": "#B07219",
    "Ruby": "#CC342D", "C": "#7A8B99", "PLpgSQL": "#336790",
}

LABELS = ["CONTRIBUTIONS", "COMMITS", "PULL REQUESTS",
          "CURRENT STREAK", "LONGEST STREAK", "REPOSITORIES"]
NOTE = "public repositories  ·  regenerated twice daily by a github action"


def build(theme: str, d: dict) -> str:
    """A stat card, not a dashboard of boxes.

    Six bordered tiles gave every number the same weight and made the panel read as a
    form. Here the numerals are large and light, the labels are small and tracked, and a
    single glow marks the one figure worth reading first. Stars and followers are absent
    on purpose: on an account opened in 2024 they measure reach and age, not work - the
    same argument that makes hide_rank the right call on a github-readme-stats card."""
    c = D.THEMES[theme]
    vals = [f"{d['contributions']:,}", f"{d['commits']:,}", f"{d['prs']:,}",
            f"{d['streak']}", f"{d['longest']}", f"{d['repos']}"]
    units = [None, None, None, "days", "days", None]

    chars = fonts.charset("".join(LABELS) + "".join(vals) + NOTE + "ACTIVITYLANGUAGE"
                          + "".join(n for n, _ in d["langs"]) + "days%.,")
    css, fb = fonts.embed_faces(chars)

    o = [D.svg_open(W, H, f"GitHub activity for {USER}",
                    "Contributions, commits, pull requests, streaks and repository count, "
                    "with the language mix by bytes.", css),
         D.defs(c), D.page(W, H, c)]

    PAD = 44
    o.append(D.eyebrow(PAD, 46, "ACTIVITY", c))
    o.append(T(W - PAD, 46, NOTE, size=SIZE["micro"], fill=c["text3"], anchor="end"))
    o.append(D.rule(PAD, 64, W - PAD * 2, c))

    # ---- six figures, three across
    COLS, COLW = 3, 206
    for i, (label, val, unit) in enumerate(zip(LABELS, vals, units)):
        cx = PAD + (i % COLS) * COLW
        cy = 118 + (i // COLS) * 96
        if i == 0:                       # the one number the eye should land on first
            o.append(D.glow(cx + 46, cy - 12, 108))
        o.append(T(cx, cy - 30, label, size=SIZE["micro"], weight=700,
                   fill=c["text3"], track=0.18))
        col = c["violet"] if i == 0 else c["text"]
        o.append(T(cx, cy + 14, val, size=44, weight=300, fill=col, track=-0.01))
        if unit:
            o.append(T(cx + w(val, size=44, weight=300, track=-0.01) + 8, cy + 14,
                       unit, size=SIZE["small"], fill=c["text3"]))

    # ---- divider, then the language mix
    LX = PAD + COLS * COLW + 24
    o.append(f'<rect x="{LX - 26}" y="82" width="1" height="{H - 82 - 52}"'
             f' fill="{c["line"]}"/>')
    o.append(D.eyebrow(LX, 92, "LANGUAGE", c, colour=c["cyan"]))
    o.append(T(W - PAD, 92, "by bytes, markup excluded", size=SIZE["micro"],
               fill=c["text3"], anchor="end"))

    bar_x, bar_w = LX + 116, W - PAD - 62 - (LX + 116)
    for i, (name, pct) in enumerate(d["langs"][:5]):
        y = 130 + i * 34
        col = LANG_COLOUR.get(name, c["cyan"])
        o.append(T(LX, y + 4, name, size=SIZE["small"], fill=c["text2"]))
        o.append(f'<rect x="{bar_x}" y="{y - 6}" width="{bar_w}" height="9" rx="4.5"'
                 f' fill="{c["surf2"]}"/>')
        o.append(f'<rect x="{bar_x}" y="{y - 6}" width="0" height="9" rx="4.5" fill="{col}">'
                 f'<animate attributeName="width" values="0;{bar_w * pct / 100:.1f}"'
                 f' dur="1.15s" begin="{0.12 * i:.2f}s" fill="freeze"'
                 f' calcMode="spline" keySplines="{D.EASE}"/></rect>')
        o.append(T(W - PAD, y + 4, f"{pct:.1f}%", size=SIZE["small"], mono=True,
                   fill=c["text3"], anchor="end"))

    o.append("</svg>")
    return "".join(o)


def main() -> None:
    out = sys.argv[1] if len(sys.argv) > 1 else "../assets"
    d = digest(fetch())
    print("stats:", {k: v for k, v in d.items() if k != "langs"})
    print("langs:", [(n, round(p, 1)) for n, p in d["langs"]])
    os.makedirs(out, exist_ok=True)
    for theme in ("dark", "light"):
        s = build(theme, d)
        p = os.path.join(out, f"stats-{theme}.svg")
        open(p, "w", encoding="utf-8").write(s)
        print(f"{p}: {len(s.encode()) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
