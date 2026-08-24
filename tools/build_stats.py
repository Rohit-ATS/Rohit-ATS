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

from svgkit import MONO, THEMES, ch, esc, svg_open, text, window

W, H = 1180, 268
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
      contributionCalendar { totalContributions }
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
    return dict(
        contributions=cc["contributionCalendar"]["totalContributions"],
        commits=cc["totalCommitContributions"],
        prs=cc["totalPullRequestContributions"],
        issues=cc["totalIssueContributions"],
        repos=u["repositories"]["totalCount"],
        stars=sum(r["stargazerCount"] for r in repos),
        followers=u["followers"]["totalCount"],
        langs=[(n, v / total * 100) for n, v in top],
    )


LANG_COLOUR = {
    "Python": "#3572A5", "TypeScript": "#3178C6", "JavaScript": "#F1E05A",
    "C++": "#F34B7D", "Dart": "#00B4AB", "Shell": "#89E051", "Swift": "#F05138",
    "Kotlin": "#A97BFF", "Go": "#00ADD8", "Rust": "#DEA584", "Java": "#B07219",
    "Ruby": "#701516", "C": "#555555", "PLpgSQL": "#336790", "Jupyter Notebook": "#DA5B0B",
}


def build(theme: str, d: dict) -> str:
    c = THEMES[theme]
    chrome, _ = window(W, H, c, f"gh api / {USER} / public", titlebar=BAR)
    o = [svg_open(W, H, f"GitHub statistics for {USER}",
                  "Contribution, repository and language statistics, generated from the "
                  "GitHub API by a scheduled Action."),
         chrome]

    # ---- headline tiles
    tiles = [("CONTRIBUTIONS", f"{d['contributions']:,}", c["mark"]),
             ("COMMITS",       f"{d['commits']:,}",       c["chrome"]),
             ("PULL REQUESTS", f"{d['prs']:,}",           c["chrome"]),
             ("REPOSITORIES",  f"{d['repos']:,}",         c["violet"]),
             ("STARS EARNED",  f"{d['stars']:,}",         c["warn"]),
             ("FOLLOWERS",     f"{d['followers']:,}",     c["violet"])]
    tw, th = 176, 74
    for i, (label, value, col) in enumerate(tiles):
        cx = 26 + (i % 3) * (tw + 12)
        cy = 58 + (i // 3) * (th + 12)
        o.append(f'<rect x="{cx}" y="{cy}" width="{tw}" height="{th}" rx="7"'
                 f' fill="{c["panel"]}" stroke="{c["chrome_dim"]}"/>')
        o.append(text(cx + 14, cy + 24, label, 9.5, c["title"]))
        # Not locked with textLength: the tile value is the one number a reader
        # actually looks at, and squeezing it to a computed width makes it look wrong.
        o.append(f'<text x="{cx + 14}" y="{cy + 58}" font-size="30" font-weight="bold"'
                 f' font-family="{MONO}" fill="{col}">{esc(value)}</text>')

    # ---- language bars
    LX = 610
    o.append(text(LX, 76, "LANGUAGE", 12, c["chrome"], weight="bold"))
    o.append(text(W - 26, 76, "by bytes, markup excluded", 10, c["title"], anchor="end"))
    o.append(f'<rect x="{LX}" y="86" width="{W - 26 - LX}" height="1" fill="{c["rule"]}"/>')

    bar_x = LX + 128
    bar_w = W - 26 - bar_x - 58
    for i, (name, pct) in enumerate(d["langs"]):
        y = 112 + i * 26
        col = LANG_COLOUR.get(name, c["chrome"])
        o.append(text(LX, y + 4, name[:14], 12, c["value"]))
        o.append(f'<rect x="{bar_x}" y="{y - 7}" width="{bar_w}" height="12" rx="6"'
                 f' fill="{c["chrome_dim"]}" opacity="0.35"/>')
        o.append(f'<rect x="{bar_x}" y="{y - 7}" width="0" height="12" rx="6" fill="{col}">'
                 f'<animate attributeName="width" values="0;{bar_w * pct / 100:.1f}"'
                 f' dur="1.1s" begin="{0.15 * i:.2f}s" fill="freeze"'
                 f' calcMode="spline" keySplines="0.2 0.8 0.2 1"/></rect>')
        o.append(text(W - 26, y + 4, f"{pct:5.1f}%", 11.5, c["title"], anchor="end"))

    o.append(text(26, H - 14,
                  "regenerated twice a day by .github/workflows/assets.yml / "
                  "no third-party service in the path", 10, c["title"], opacity=0.85))
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
