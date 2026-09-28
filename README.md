<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mark-dark.svg">
  <img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mark-light.svg" width="120" height="120" alt="A dependency graph drawing itself — a root node, its edges, and a pulse travelling out to the leaves">
</picture>

# Rohit Maruri

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/typing-dark.svg">
  <img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/typing-light.svg" width="700" alt="I build infrastructure for agents that touch production. The shape of the data decides which questions you can ask. No mocked data, measured not claimed. Five shipped this year, every one of them has its tests.">
</picture>

CS undergrad at San Francisco Bay University building **agent and developer
infrastructure** — systems that let an autonomous agent touch something that matters
and then prove it did the right thing. Five shipped this year; all public, all MIT.

[![Open to internships](https://img.shields.io/badge/open%20to-internships-00674F?style=flat-square)](mailto:rohitmaruriats@gmail.com)
[![School](https://img.shields.io/badge/B.S.%20Computer%20Science-San%20Francisco%20Bay%20University-00674F?style=flat-square)](#education)
[![Location](https://img.shields.io/badge/Fremont,%20CA-00674F?style=flat-square&logo=googlemaps&logoColor=white)](#contact)
[![License](https://img.shields.io/badge/everything%20below-MIT-00674F?style=flat-square)](#selected-work)

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-00674F?style=flat-square&logo=python&logoColor=white">
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-00674F?style=flat-square&logo=typescript&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-00674F?style=flat-square&logo=fastapi&logoColor=white">
  <img alt="Next.js" src="https://img.shields.io/badge/Next.js-00674F?style=flat-square&logo=nextdotjs&logoColor=white">
  <img alt="React" src="https://img.shields.io/badge/React_19-00674F?style=flat-square&logo=react&logoColor=white">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-00674F?style=flat-square&logo=postgresql&logoColor=white">
  <img alt="pgvector" src="https://img.shields.io/badge/pgvector-00674F?style=flat-square&logo=postgresql&logoColor=white">
  <img alt="DynamoDB" src="https://img.shields.io/badge/DynamoDB-00674F?style=flat-square&logo=amazondynamodb&logoColor=white">
  <img alt="AWS Bedrock" src="https://img.shields.io/badge/Bedrock_AgentCore-00674F?style=flat-square&logo=amazonaws&logoColor=white">
  <img alt="AWS Lambda" src="https://img.shields.io/badge/Lambda-00674F?style=flat-square&logo=awslambda&logoColor=white">
  <img alt="MCP" src="https://img.shields.io/badge/MCP_servers-00674F?style=flat-square&logo=anthropic&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-00674F?style=flat-square&logo=docker&logoColor=white">
</p>

[**Email**](mailto:rohitmaruriats@gmail.com) · [**LinkedIn**](https://www.linkedin.com/in/rohitmaruri/) · [**LeetCode**](https://leetcode.com/u/rohitmaruriats/) · [**Codeforces**](https://codeforces.com/profile/rohitmaruriats)

</div>

<p align="center">
  <a href="#selected-work"><img alt="Selected work" src="https://img.shields.io/badge/Selected_work-1B1C14?style=for-the-badge"></a>
  <a href="#the-pattern-underneath"><img alt="The pattern" src="https://img.shields.io/badge/The_pattern-1B1C14?style=for-the-badge"></a>
  <a href="#the-stack"><img alt="Stack" src="https://img.shields.io/badge/Stack-1B1C14?style=for-the-badge"></a>
  <a href="#how-i-build"><img alt="How I build" src="https://img.shields.io/badge/How_I_build-1B1C14?style=for-the-badge"></a>
  <a href="#education"><img alt="Education" src="https://img.shields.io/badge/Education-1B1C14?style=for-the-badge"></a>
  <a href="#contact"><img alt="Contact" src="https://img.shields.io/badge/Contact-1B1C14?style=for-the-badge"></a>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/projects-dark.svg">
    <img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/projects-light.svg" width="100%" alt="Five shipped projects — LexisGuide, DOCKET, FORGE, Airlock and Semantic Output Cache — each with what it does, what it is built from, and its test or evaluation numbers">
  </picture>
  <br>
  <sub>Every number on the right is in the repository it belongs to. Nothing here is a mockup.</sub>
</p>

<br>

## Selected work

Each of these started from a question that sounded simpler than it was, and in every
case the popular tool was the wrong *shape* for it — a vector index cannot answer a
five-hop traversal, and an exact-match cache key never hits on traffic nobody phrases
the same way twice.

|  |  |
|---|---|
| **[LexisGuide](https://github.com/k1lst1x/LexisGuide)**<br><sub>React 19 · Bedrock Nova · DynamoDB · Base</sub> | Reads the legal notice you were sent and finds the deadline buried in it. A router plus specialist agents, and every edit fingerprinted with SHA-256 onto a chain, so nothing can be quietly rewritten. Built for **LexHack 2026**. |
| **[DOCKET](https://github.com/k1lst1x/DOCKET)**<br><sub>Next.js 15 · Strands Agents · Aurora DSQL</sub> | The agent that reads city hall so a volunteer neighborhood group doesn't have to. Every claim links to its source document. **81 tests**, 19 of 20 citations valid, and 5 of 5 correct refusals on the unanswerable questions. |
| **[FORGE](https://github.com/k1lst1x/FORGE)**<br><sub>Python 3.14 · FastAPI · OpenTelemetry</sub> | Ships the feature, then audits itself and proves the hole is actually closed — tests passing *and* a fresh scan agreeing. **17 live checks**, and it refuses the findings it should refuse. Stops at the pull request, deliberately. |
| **[Airlock](https://github.com/Rohit-ATS/Airlock)**<br><sub>TypeScript · Postgres · MCP</sub> | Proves an irreversible production change on a shadow copy before anyone approves it: apply, undo, three checksums, and the gate opens only if `pre == post_rollback`. **201 tests** across 24 suites. |
| **[Semantic Output Cache](https://github.com/Rohit-ATS/semantic-output-cache)**<br><sub>Postgres · pgvector · Redis</sub> | Exact-match caches never hit on LLM traffic. This one embeds each output and serves it when cosine similarity clears a threshold. Redis is an accelerator, not a dependency. Key hashes stored, never keys. |

<sub>Also: **[blast-radius](https://github.com/Rohit-ATS/blast-radius)** — npm supply-chain
exposure as a graph traversal rather than a similarity search, 381 tests, built solo over
a hackathon weekend &nbsp;·&nbsp; **[meridian](https://github.com/Rohit-ATS/meridian)** —
a financial terminal that tracks tax lots individually, because an average basis makes
harvesting advice quietly wrong &nbsp;·&nbsp;
**[Vivedly AI](https://github.com/Rohit-ATS/Vivedly-AI)** — a desktop coworker with a
five-tier memory hierarchy instead of one vector store.</sub>

<br>

## The pattern underneath

Four of the five are the same shape, and it is the shape I find most interesting: an
agent allowed to do real work, with the proof — not the promise — standing between it
and the thing it would change.

```mermaid
%%{init: {"theme": "base", "themeVariables": {
  "primaryColor": "#E9F3EA", "primaryTextColor": "#1B1C14",
  "primaryBorderColor": "#00674F", "lineColor": "#2F8A5E",
  "secondaryColor": "#FAF7EE", "tertiaryColor": "#FFFDF5",
  "fontFamily": "Inter, sans-serif" }}}%%
flowchart LR
    A["Agent<br/>proposes a change"] --> B["One doorway<br/>MCP tools, read-mostly"]
    B --> C["Sandbox<br/>apply, undo, checksum"]
    C -->|"pre == post_rollback"| D["Gate<br/>policy and quorum"]
    C -->|"drift"| X["Refused<br/>with the diff"]
    D --> E["Human decides<br/>against evidence"]
    E --> F["Sealed record<br/>hash-chained"]
```

The interesting part is never the model. It is that the approval is impossible to
construct without the proof: in Airlock the gate's rule is a module-private symbol only
`openGate()` can mint, so a non-proven approval is not greyed out or warned about — it
is unrepresentable in the type system.

<br>

## The stack

| | |
|---|---|
| **Languages** | Python · TypeScript · SQL · Cypher · Solidity · Bash |
| **Data** | PostgreSQL · pgvector · DynamoDB · Aurora DSQL · S3 Vectors · SQLite · Redis |
| **Agents & AI** | AWS Bedrock (Nova, AgentCore) · Strands Agents · Claude API · MCP servers · embeddings and RAG |
| **Interface** | React 19 · Next.js 15 · Tailwind · Electron · vanilla JS with no build step |
| **Infrastructure** | AWS Lambda · S3 · CDK · Docker · FastAPI · Vercel · Amplify · GitHub Actions |
| **Practice** | pytest · Vitest · OpenTelemetry · CodeQL · groundedness evals · threat models in the repo |

<br>

## How I build

| | |
|---|---|
| **📊 No mocked data, anywhere** | Every number on every screen came back from a query that was actually run — including the empty states. A demo that lies is worse than no demo. |
| **📐 Measured, not claimed** | If it says fast, there is a latency beside it. If it says safe, there is a checksum, an eval score, or a test id beside it. |
| **🔑 Secrets are a design problem** | Not a checklist item at the end. The `.gitignore` globs exist because an explicit list already failed once, and the reasoning is written down in the file. |
| **📝 Commits explain the change** | Not the diff. *"Answer the lockfile question from the lockfile."* You can read the history and know what happened. |

<br>

## Education

**B.S. Computer Science** — San Francisco Bay University, since 2025. Coursework in data
structures, systems and databases; most of what is above was built outside of it, on
weekends and at hackathons — LexHack 2026, Agents for Humans, Zero Downtime, Hack Hydra.

<br>

## Activity

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/output/stats-dark.svg">
  <img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/output/stats-light.svg" width="100%" alt="GitHub statistics: contributions, commits, pull requests, repositories and the language mix">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/output/snake-dark.svg">
  <img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/output/snake-light.svg" width="100%" alt="A snake eating a year of my contribution graph">
</picture>

</div>

<!-- Both cards are generated by .github/workflows/assets.yml straight into the `output`
     branch; the mark, the typing line and the projects panel are generated by tools/
     into main. Nothing on this page comes from a third-party image host, which is
     deliberate: the streak card this profile used to carry recomputed per distinct URL,
     took longer to render cold than GitHub's camo proxy waits, and camo cached the 504
     for an hour at a time. The typing line is the same effect as readme-typing-svg,
     generated here instead. -->

<br>

## Contact

I move fast and I would rather build the hard version. If you are working on agent
infrastructure, graph systems, or developer tooling — or you want someone who ships over
a hackathon weekend and still writes the tests — I would like to hear from you.

<div align="center">

[**rohitmaruriats@gmail.com**](mailto:rohitmaruriats@gmail.com) · [**LinkedIn**](https://www.linkedin.com/in/rohitmaruri/)

<sub>Open to internships, hackathon teams, and OSS collaboration.<br>
Ink, paper, sand, green, meadow, amber — the palette is LexisGuide's own.</sub>

</div>
