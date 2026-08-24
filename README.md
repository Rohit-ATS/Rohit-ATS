<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/banner-light.svg">
  <img alt="Rohit Maruri - developer infrastructure. Computer Science at San Francisco Bay University. Graph databases, semantic caches, agent runtimes." src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/banner-dark.svg" width="100%">
</picture>

<br><br>

[![Email](<https://img.shields.io/badge/Email-0A101F?style=for-the-badge&labelColor=0A101F&logo=gmail&logoColor=10B981>)](mailto:rohitmaruriats@gmail.com)
&nbsp;·&nbsp;
[![LinkedIn](<https://img.shields.io/badge/LinkedIn-0A101F?style=for-the-badge&labelColor=0A101F&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iIzIyZDNlZSIgZD0iTTIwLjQ0NyAyMC40NTJoLTMuNTU0di01LjU2OWMwLTEuMzI4LS4wMjctMy4wMzctMS44NTItMy4wMzctMS44NTMgMC0yLjEzNiAxLjQ0NS0yLjEzNiAyLjkzOXY1LjY2N0g5LjM1MVY5aDMuNDE0djEuNTYxaC4wNDZjLjQ3Ny0uOSAxLjYzNy0xLjg1IDMuMzctMS44NSAzLjYwMSAwIDQuMjY3IDIuMzcgNC4yNjcgNS40NTV2Ni4yODZ6TTUuMzM3IDcuNDMzYy0xLjE0NCAwLTIuMDYzLS45MjYtMi4wNjMtMi4wNjUgMC0xLjEzOC45Mi0yLjA2MyAyLjA2My0yLjA2MyAxLjE0IDAgMi4wNjQuOTI1IDIuMDY0IDIuMDYzIDAgMS4xMzktLjkyNSAyLjA2NS0yLjA2NCAyLjA2NXptMS43ODIgMTMuMDE5SDMuNTU1VjloMy41NjR2MTEuNDUyek0yMi4yMjUgMEgxLjc3MUMuNzkyIDAgMCAuNzc0IDAgMS43Mjl2MjAuNTQyQzAgMjMuMjI3Ljc5MiAyNCAxLjc3MSAyNGgyMC40NTFDMjMuMiAyNCAyNCAyMy4yMjcgMjQgMjIuMjcxVjEuNzI5QzI0IC43NzQgMjMuMiAwIDIyLjIyNSAweiIvPjwvc3ZnPg%3D%3D>)](https://www.linkedin.com/in/rohitmaruri/)
&nbsp;·&nbsp;
[![Blast Radius](<https://img.shields.io/badge/Blast_Radius-0A101F?style=for-the-badge&labelColor=0A101F&logo=neo4j&logoColor=22D3EE>)](https://github.com/Rohit-ATS/blast-radius)
&nbsp;·&nbsp;
[![The stack](<https://img.shields.io/badge/The_Stack-0A101F?style=for-the-badge&labelColor=0A101F&logo=typescript&logoColor=A78BFA>)](#the-stack)

</div>

---

First-year CS student at **San Francisco Bay University**. I build things that actually
ship — with tests, migrations, signed webhooks, and an answer for what happens when
they break at 3 AM.

Most of my time goes to **developer infrastructure**. I'm drawn to the problems where
the popular tool is the wrong *shape* for the question — where everyone reaches for a
vector index and the question was never about similarity.

The throughline in all of it is the same: **the shape of the data decides which
questions you are allowed to ask.** Blast Radius stores one graph twice because traversal
speed and forensic precision want different shapes. The cache keys on meaning because an
exact-match key never hits on LLM traffic. Meridian tracks tax lots individually because
an average cost basis makes harvesting advice quietly wrong.

Choose that wrong and no amount of application code rescues it. Choose it right and the
query everyone told you was expensive collapses into one hop.

<br>

## Blast Radius

> **When an npm package is compromised, defenders have minutes to answer one question:
> *who is actually exposed, right now?***

Every AI dev tool shipping today indexes code as embeddings and retrieves by similarity.
A transitive reverse-dependency closure is not a similarity problem — it is a graph
traversal, five hops deep, over tens of millions of versioned nodes. Similarity cannot
answer it. Not badly. **At all.**

So I built the thing that can.

<a href="https://github.com/Rohit-ATS/blast-radius">
  <img src="https://raw.githubusercontent.com/Rohit-ATS/blast-radius/main/docs/images/hero.png" alt="The Blast Radius landing page" width="100%">
</a>

|   | The question | How it's answered |
| - | ------------ | ----------------- |
| **1** | **Who is transitively exposed?** Everything that pulls it, five levels down. | One variable-length traversal from a known vertex |
| **2** | **Whose semver range would *actually* have pulled the poison?** Declaring a dependency and resolving to the bad version are different facts. | Every declared range, evaluated against the bad version |
| **3** | **Is anything in my lockfile already malicious?** | Live against `osv.dev` — no crawl coverage required |
| **4** | **How do I fix it?** | The safe version, an `overrides` block, a brief an agent can act on |

<table>
<tr>
<td width="50%"><a href="https://github.com/Rohit-ATS/blast-radius"><img src="https://raw.githubusercontent.com/Rohit-ATS/blast-radius/main/docs/images/blast-map.png" alt="The blast radius, drawn as concentric rings by depth"></a></td>
<td width="50%"><a href="https://github.com/Rohit-ATS/blast-radius"><img src="https://raw.githubusercontent.com/Rohit-ATS/blast-radius/main/docs/images/check.png" alt="The incident console"></a></td>
</tr>
<tr>
<td><b>The radius, drawn.</b> Concentric rings by depth, red attenuating outward. Click any package to pivot the entire console onto it.</td>
<td><b>The console.</b> Blast radius, semver split, lockfile verdict, OSV audit, graph explorer, live publish feed — one port, no build step.</td>
</tr>
</table>

**The data model is the whole trick.** Two layers in one graph: a collapsed
`Package-[:REQUIRES]->Package` layer so traversal stays flat as depth grows, and a
version-precise `Release-[:DEPENDS_ON]->Package` layer underneath so the forensic
questions stay answerable. Traversal speed and forensic precision want different
shapes — so I store both and let the planner pick.

<sub>**Python · FastAPI · HydraDB (OpenCypher) · SQLite · Supabase · Docker · vanilla JS, zero build step**<br>27k lines &nbsp;·&nbsp; 381 tests &nbsp;·&nbsp; MIT &nbsp;·&nbsp; built solo over a hackathon weekend for Hack Hydra</sub>

<br>

## Also building

<table>
<tr>
<td width="33%" valign="top">

### [Vivedly AI](https://github.com/Rohit-ATS/Vivedly-AI)
**~11k lines · Electron + React**

A proactive desktop coworker — it watches what you're working on and surfaces the
right action *before* you ask. A five-tier memory hierarchy (RAM → SQLite → patterns →
vector → long-term) instead of one vector DB. Native desktop control, an MCP tool layer,
streaming voice, and connectors for Gmail, Slack, Notion, and GitHub.

</td>
<td width="33%" valign="top">

### [Meridian](https://github.com/Rohit-ATS/meridian)
**~20k lines · Next.js 16 + React 19**

An AI-native financial terminal — fifteen views, options priced with Black-Scholes,
and tax lots tracked individually rather than by average basis. Market data is
**simulated**, deliberately: it runs with no API key, and the feed swaps at one
function.

</td>
<td width="33%" valign="top">

### [Semantic Output Cache](https://github.com/Rohit-ATS/semantic-output-cache)
**~4.8k lines · Postgres + pgvector**

Exact-match caches never hit on LLM traffic — nobody phrases it twice the same way.
This one embeds each output and serves it when cosine similarity clears a threshold.
Only SHA-256 key hashes stored, JS + Python SDKs, and a threat model in the repo.

</td>
</tr>
</table>

<br>

## The stack

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/stack-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/stack-light.svg">
  <img alt="Stack: Python, TypeScript, SQL and Cypher, Bash · HydraDB, PostgreSQL, pgvector, SQLite, Redis, Prisma · Claude API, MCP servers, Ollama, Whisper, embeddings · React 19, Next.js 16, Electron, Tailwind v4 · Docker, FastAPI, Render, Vercel, GitHub Actions" src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/stack-dark.svg" width="100%">
</picture>

<br>

## Activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com/?user=Rohit-ATS&amp;hide_border=false&amp;border_radius=8&amp;background=0A101F&amp;border=1B4A5C&amp;stroke=1B4A5C&amp;ring=22D3EE&amp;fire=10B981&amp;currStreakNum=C7D2E4&amp;sideNums=C7D2E4&amp;currStreakLabel=22D3EE&amp;sideLabels=5FBBD0&amp;dates=5FBBD0">
  <source media="(prefers-color-scheme: light)" srcset="https://streak-stats.demolab.com/?user=Rohit-ATS&amp;hide_border=false&amp;border_radius=8&amp;background=FFFFFF&amp;border=A9CFDC&amp;stroke=A9CFDC&amp;ring=0891B2&amp;fire=059669&amp;currStreakNum=1E293B&amp;sideNums=1E293B&amp;currStreakLabel=0891B2&amp;sideLabels=64748B&amp;dates=64748B">
  <img alt="Contribution streak: current streak, total contributions, and longest streak" src="https://streak-stats.demolab.com/?user=Rohit-ATS&amp;hide_border=false&amp;border_radius=8&amp;background=0A101F&amp;border=1B4A5C&amp;stroke=1B4A5C&amp;ring=22D3EE&amp;fire=10B981&amp;currStreakNum=C7D2E4&amp;sideNums=C7D2E4&amp;currStreakLabel=22D3EE&amp;sideLabels=5FBBD0&amp;dates=5FBBD0" width="100%">
</picture>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/output/snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/output/snake-light.svg">
  <img alt="A snake eating a year of my contribution graph" src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/output/snake-dark.svg" width="100%">
</picture>

<!-- STREAK CARD, if you ever re-theme it: streak-stats.demolab.com recomputes from
     scratch for every distinct URL, and a cold one takes 10-30s to first byte (measured;
     it also returns the odd 503). GitHub's camo proxy gives up well before that, caches
     the failure, and the card renders as alt text.

     Fix: request the new URL directly until it 200s quickly, THEN request the camo URL
     from the rendered page until that 200s too. Once camo has cached it, visitors are
     served from camo and it is fast. Changing any colour param starts this over.

     STATS CARDS - waiting on a self-hosted instance. The public github-readme-stats
     deployment returns 503 on every endpoint (verified /api, /api/top-langs, /api/pin),
     which is why the two cards below are not wired to it. Deploy the fork at
     github.com/Rohit-ATS/github-readme-stats to Vercel with PAT_1 set, replace INSTANCE,
     and uncomment. Self-hosting also makes the 35 private contributions countable - the
     public instance cannot see them at all.

<div align="center">
  <img width="49%" src="https://INSTANCE/api?username=Rohit-ATS&show_icons=true&hide_rank=true&include_all_commits=true&count_private=true&bg_color=0A101F&title_color=22D3EE&text_color=C7D2E4&icon_color=10B981&border_color=1B4A5C&border_radius=8" alt="GitHub stats">
  <img width="49%" src="https://INSTANCE/api/top-langs?username=Rohit-ATS&layout=compact&langs_count=8&hide=html,css&bg_color=0A101F&title_color=22D3EE&text_color=C7D2E4&border_color=1B4A5C&border_radius=8" alt="Top languages">
</div>
-->

<br>

## How I build

Four rules I hold every project to. They're unglamorous, and they're where most of the
real decisions end up.

**No mocked data. Anywhere.** Every number on every screen comes back from a query that
was actually run — including empty states. A demo that lies is worse than no demo.

**Measured, not claimed.** Every panel in Blast Radius carries the latency of the query
that produced it. If I say it's fast, there's a number next to the claim.

**Secrets are a design problem, not a checklist item.** From that repo's `.gitignore`,
verbatim:

```gitignore
# Deliberately a glob: .env.production was not covered by the explicit list,
# which is the failure mode this pattern exists to prevent.

# SQLite side files, for every database this project grows. Listing each one by
# name has already failed once: the -shm and -wal here were git added first and
# ignored second, and .gitignore does not apply to anything already in the
# index, so they stayed staged and would have been committed.
```

**Commits explain the change, not the diff.** `Answer the lockfile question from the
lockfile.` `Keep the site up when its dependencies are not.` You can read the history
and know what happened.

<br>

## Reach me

I'm a freshman, I move fast, and I'd rather build the hard version. If you're working on
graph systems, agent infrastructure, or developer tooling — or you want someone who ships
over a hackathon weekend and still writes the tests — I'd like to hear from you.

**[rohitmaruriats@gmail.com](mailto:rohitmaruriats@gmail.com)** &nbsp;·&nbsp; open to internships, hackathon teams, and OSS collaboration

<div align="center">
<br>
<sub><i>Everything above is a link. The code is public and the tests are in the repo.</i></sub>
</div>
