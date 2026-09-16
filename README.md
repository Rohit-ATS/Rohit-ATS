<!--
  Minecraft-inspired profile README.
  Visual language: pixel UI, inventory hotbar, crafting stations, quests,
  achievements, world stats, and an original overworld scene.
-->

<div align="center">

<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/minecraft-hero-dark.svg" width="100%" alt="Rohit Maruri — systems builder in a pixel-art world" />

### The systems builder for hard problems.<br>AI infrastructure, graph systems, developer tools, and software worth shipping.

<a href="#projects"><img src="https://raw.githubusercontent.com/k1lst1x/DOCKET/main/docs/readme/buttons/play.svg" height="40" alt="Projects"></a>
<a href="#inventory"><img src="https://raw.githubusercontent.com/k1lst1x/DOCKET/main/docs/readme/buttons/features.svg" height="40" alt="Inventory"></a>
<a href="#how-i-build"><img src="https://raw.githubusercontent.com/k1lst1x/DOCKET/main/docs/readme/buttons/how.svg" height="40" alt="How I build"></a>
<a href="#architecture-minded"><img src="https://raw.githubusercontent.com/k1lst1x/DOCKET/main/docs/readme/buttons/architecture.svg" height="40" alt="Architecture"></a>
<a href="#quest-log"><img src="https://raw.githubusercontent.com/k1lst1x/DOCKET/main/docs/readme/buttons/quickstart.svg" height="40" alt="Quest log"></a>
<a href="#connect"><img src="https://raw.githubusercontent.com/k1lst1x/DOCKET/main/docs/readme/buttons/docs.svg" height="40" alt="Connect"></a>

<br><br>

<img src="https://img.shields.io/badge/STATUS-BUILDING-6DB33F?style=for-the-badge&labelColor=262626" alt="Building">
<img src="https://img.shields.io/badge/CLASS-SYSTEMS%20BUILDER-7E57C2?style=for-the-badge&labelColor=262626" alt="Systems builder">
<img src="https://img.shields.io/badge/MODE-SHIP-C8352B?style=for-the-badge&labelColor=262626" alt="Ship">
<img src="https://img.shields.io/badge/FOCUS-AI%20%2F%20INFRASTRUCTURE-3D7CC9?style=for-the-badge&labelColor=262626" alt="AI infrastructure">

<br><br>

<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-hotbar.svg" width="760" alt="Rohit's engineering hotbar">

<sub>▲ Projects, agents, graphs, caching, systems, security, and developer tools.</sub>

</div>

<br>

<details>
<summary><b>📜 WORLD MAP · TABLE OF CONTENTS</b></summary>

<br>

| | | |
| --- | --- | --- |
| 🌲 [Spawn Point](#spawn-point) | 🎒 [Inventory](#inventory) | ⚒️ [Crafting Table](#crafting-table) |
| ⛏️ [How I Build](#how-i-build) | 🧱 [Projects](#projects) | 🧰 [Tech Stack](#tech-stack) |
| 🟩 [Quest Log](#quest-log) | 🏆 [Achievements](#achievements) | 📊 [World Stats](#world-stats) |
| 🧪 [Rules of the World](#rules-of-the-world) | 🗺️ [Current Coordinates](#current-coordinates) | ✉️ [Connect](#connect) |

</details>

<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-divider.svg" width="100%" alt="pixel grass divider" />

<a id="spawn-point"></a>

## 🌲 Spawn Point

<table>
<tr>
<td width="62%" valign="top">

I'm **Rohit Maruri** — a CS student and obsessive builder who likes taking difficult engineering problems and turning them into systems that actually run.

I'm especially interested in the layer underneath the UI: **data models, graph traversal, retrieval, agents, caching, testing, observability, security, and failure modes.**

The projects I build tend to start with a question that sounds deceptively simple:

> **"What if we designed the system around the real problem instead of the convenient implementation?"**

Then I disappear into the cave for a while.

</td>
<td width="38%" valign="top">

```text
╔══════════════════════╗
║   PLAYER PROFILE     ║
╠══════════════════════╣
║ NAME     Rohit       ║
║ CLASS    Builder     ║
║ LEVEL    Always ↑    ║
║ MODE     Ship        ║
║ BIOME    Software    ║
║ TOOL     Keyboard    ║
║ STATUS   Building    ║
╚══════════════════════╝
```

**Current biome:** AI × infrastructure  
**Favorite block:** the one nobody has documented yet.

</td>
</tr>
</table>

### ❤️ Why I code

I love the moment where something that was only an idea becomes a working system — especially when the system has enough depth that you can keep pulling on the thread and discover another interesting problem underneath it.

**No fake demos. No hand-wavy architecture. No hiding the hard parts.**

<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-divider.svg" width="100%" alt="pixel grass divider" />

<a id="inventory"></a>

## 🎒 Inventory

> Everything currently sitting in the hotbar — the systems I have built, broken, rebuilt, and learned from.

<table>
<tr>
<th width="50%">💎 RARE ITEM · BLAST RADIUS</th>
<th width="50%">🧠 EPIC ITEM · VIVEDLY AI</th>
</tr>
<tr>
<td valign="top">

**Dependency intelligence for security teams.**

A graph-based system for answering the question that matters after a dependency compromise: **what is actually exposed?**

It traverses transitive dependencies, resolves semver ranges, checks OSV, and turns the resulting graph into actionable remediation paths.

`Python` `FastAPI` `HydraDB` `OpenCypher` `SQLite` `Docker`

<a href="https://github.com/Rohit-ATS/blast-radius"><b>⛏ View Blast Radius →</b></a>

</td>
<td valign="top">

**A proactive AI desktop coworker.**

Instead of waiting for a prompt, Vivedly watches the work context and tries to surface the next useful action — with layered memory, MCP tools, streaming voice, and native desktop control.

`Electron` `React` `TypeScript` `SQLite` `MCP` `AI`

<a href="https://github.com/Rohit-ATS/Vivedly-AI"><b>🧠 View Vivedly AI →</b></a>

</td>
</tr>
<tr>
<th>📈 EPIC ITEM · MERIDIAN</th>
<th>⚡ UNCOMMON ITEM · SEMANTIC OUTPUT CACHE</th>
</tr>
<tr>
<td valign="top">

**An AI-native financial terminal.**

Fifteen views, options priced with Black-Scholes, and tax lots represented individually because financial software should preserve the information required to make correct decisions.

`Next.js` `React` `TypeScript` `PostgreSQL` `AI`

<a href="https://github.com/Rohit-ATS/meridian"><b>📈 View Meridian →</b></a>

</td>
<td valign="top">

**Caching for the way humans actually talk to LLMs.**

Exact-match caching assumes users phrase the same request twice. They don't. Semantic similarity turns repeated intent into a cache hit.

`Postgres` `pgvector` `SHA-256` `Python` `JavaScript`

<a href="https://github.com/Rohit-ATS/semantic-output-cache"><b>⚡ View Semantic Cache →</b></a>

</td>
</tr>
</table>

### 🎒 More items in the chest

`AI agents` · `MCP tooling` · `developer infrastructure` · `security systems` · `graph data` · `semantic retrieval` · `financial systems` · `desktop applications` · `performance experiments`

<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-divider.svg" width="100%" alt="pixel grass divider" />

<a id="crafting-table"></a>

## ⚒️ Crafting Table

> Ideas are cheap. The interesting part is what happens between the idea and the shipped system.

<table>
<tr>
<td width="25%" align="center"><b>🪵 RAW MATERIAL</b><br><br><sub>Find the real problem.<br>Talk to the constraints.<br>Remove assumptions.</sub></td>
<td width="25%" align="center"><b>🧱 BUILD PLAN</b><br><br><sub>Choose the data model.<br>Define boundaries.<br>Make failure explicit.</sub></td>
<td width="25%" align="center"><b>⚙️ REDSTONE</b><br><br><sub>Wire the system.<br>Instrument it.<br>Test the ugly paths.</sub></td>
<td width="25%" align="center"><b>💎 DIAMOND</b><br><br><sub>Measure the result.<br>Polish the rough edges.<br>Ship it to reality.</sub></td>
</tr>
</table>

<div align="center">
<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-pipeline.svg" width="100%" alt="Minecraft-inspired software crafting pipeline" />
</div>

### ⛏️ The rule

**Model first. Build second. Measure always.**

If the architecture cannot answer the important question, it doesn't matter how good the UI looks.

If the benchmark isn't measured, it's a claim.

If the failure mode isn't tested, it isn't finished.

<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-divider.svg" width="100%" alt="pixel grass divider" />

<a id="how-i-build"></a>

## ⛏️ How I Build

### 01 · Dig for the problem

I try to get underneath the first formulation of the problem. The best engineering work usually appears when the obvious implementation is questioned.

### 02 · Lay the blocks

Data model, interfaces, invariants, boundaries, failure modes. Before the code gets large, I want to know what the system *means*.

### 03 · Turn on the redstone

Connect the components. Add instrumentation. Build the smallest useful path. Then intentionally stress it.

### 04 · Enchant the tool

Benchmark it. Remove unnecessary work. Improve the developer experience. Add the boring safeguards that become invaluable later.

### 05 · Open the world

Ship. Get real feedback. Learn what was wrong. Return to the crafting table.

```text
                 ┌───────────────┐
                 │    PROBLEM    │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │     MODEL     │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │     BUILD     │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │     TEST      │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │    MEASURE    │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │     SHIP      │
                 └───────┬───────┘
                         │
                         └──────→ LEARN → back to PROBLEM
```

<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-divider.svg" width="100%" alt="pixel grass divider" />

<a id="projects"></a>

## 🧱 Projects · The Builds

> Four builds from the world: civic intelligence, supply-chain security, autonomous software repair, and safe agentic change control.

<table>
<tr>
<td width="50%" valign="top">

### 🏘️ DOCKET · The Village

**The problem:** neighborhood information is scattered across city-hall packets, news sites, emergency feeds, maps, and group chats.

**The build:** a neighborhood operating system for Fremont. Two Strands agents on Amazon Bedrock AgentCore crawl and retrieve public records, generate short updates with numbered citations, power context-aware chat, and refuse to publish claims that fail evidence checks.

**The engineering loot:** Next.js, React, TypeScript, Python, FastAPI, Aurora DSQL, S3 Vectors, BM25, Google Maps, Rekognition, AWS Amplify.

**What I learned:** useful AI is not a chat box. It is retrieval, provenance, verification, trust boundaries, and a product people can actually use.

<a href="https://github.com/k1lst1x/DOCKET"><b>🗺️ Enter DOCKET →</b></a>

</td>
<td width="50%" valign="top">

### 💎 BLAST RADIUS · The Mine

**The problem:** when an npm package is compromised, a dependency list cannot answer who is actually exposed—or which semver ranges would have pulled the poisoned version.

**The build:** a graph-based supply-chain incident console that traverses transitive dependencies five levels deep, evaluates every declared range, checks live OSV data, draws the blast radius, and generates concrete remediation paths.

**The engineering loot:** Python, FastAPI, HydraDB, OpenCypher, SQLite, Docker, OSV, SSE, and a no-build-step frontend.

**What I learned:** the data model decides which security questions are cheap to answer. Graph shape is not an implementation detail; it is the product.

<a href="https://github.com/Rohit-ATS/blast-radius"><b>⛏️ Explore the blast radius →</b></a>

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🔨 FORGE · The Factory

**The problem:** AI can ship a page in seconds, then leave behind missing security headers, open admin routes, leaked keys, inaccessible images, and nobody responsible for fixing them.

**The build:** a software factory that keeps checking the applications it creates. FORGE discovers security and quality findings, classifies whether a fix is safe, writes the code and its test, re-checks the result, and opens a pull request for a human to approve.

**The engineering loot:** Python 3.14, FastAPI, Bright Data Scraper Studio, SigNoz, OpenTelemetry, traced workflows, and a verified test loop.

**What I learned:** autonomous repair needs a loop, not a one-shot prompt: inspect → reason → write → prove → ask.

<a href="https://github.com/k1lst1x/FORGE"><b>🏭 Enter the factory →</b></a>

</td>
<td width="50%" valign="top">

### 🛡️ AIRLOCK · The Gate

**The problem:** asking a human to approve an agent's production change before showing whether it is reversible turns approval into a trust ritual.

**The build:** a change-control system that executes proposed changes against a throwaway copy of real data, rolls them back, checksums before/after/after-rollback state, measures blast radius, and only then asks for human approval. The agent can propose, but it has no tool that writes to production.

**The engineering loot:** TypeScript, React, Next.js, Node.js, Postgres, MCP, TrueForge, policy-as-code, shadow verification, tamper-evident receipts, and 347 passing tests.

**What I learned:** safety is strongest when it is a gate enforced by evidence—not a sentence in a prompt and not a button rendered too early.

<a href="https://github.com/Rohit-ATS/Airlock"><b>🚪 Pass through AIRLOCK →</b></a>

</td>
</tr>
</table>

### 🧭 The common thread

Each build asks the same question in a different biome:

> **Can the system prove what it knows, what it changed, and why a human should trust the next step?**


<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-divider.svg" width="100%" alt="pixel grass divider" />

<a id="tech-stack"></a>

## 🧰 Tech Stack · My Tools

<div align="center">

<img src="https://skillicons.dev/icons?i=python,typescript,js,react,nextjs,electron,fastapi,nodejs,postgres,sqlite,redis,docker,git,github,linux&perline=8" alt="Technology inventory" />

<br><br>

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
<img src="https://img.shields.io/badge/SQL-8B8B8B?style=for-the-badge" alt="SQL" />
<img src="https://img.shields.io/badge/Cypher-4581C3?style=for-the-badge" alt="Cypher" />
<img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
<img src="https://img.shields.io/badge/Next.js-111111?style=for-the-badge&logo=nextdotjs&logoColor=white" alt="Next.js" />
<img src="https://img.shields.io/badge/Electron-47848F?style=for-the-badge&logo=electron&logoColor=white" alt="Electron" />
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
<img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
<img src="https://img.shields.io/badge/pgvector-5E8C6A?style=for-the-badge" alt="pgvector" />
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
<img src="https://img.shields.io/badge/Redis-9B1C1C?style=for-the-badge&logo=redis&logoColor=white" alt="Redis" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
<img src="https://img.shields.io/badge/MCP-7E57C2?style=for-the-badge" alt="MCP" />

<br><br>

`Python` · `TypeScript` · `JavaScript` · `SQL` · `Cypher` · `React` · `Next.js` · `Electron` · `FastAPI` · `Node.js` · `PostgreSQL` · `pgvector` · `SQLite` · `Redis` · `Docker` · `MCP` · `LLMs`

</div>

<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-divider.svg" width="100%" alt="pixel grass divider" />

<a id="quest-log"></a>

## 🟩 Quest Log

<div align="center">

```text
╔══════════════════════════════════════════════════════════════════════╗
║                         QUEST LOG                                  ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  [✓] Build systems that solve real problems                         ║
║  [✓] Learn by shipping                                               ║
║  [✓] Break things → understand them → rebuild them better            ║
║  [✓] Build with AI without treating AI as magic                      ║
║                                                                      ║
║  [→] Go deeper on agent infrastructure                               ║
║  [→] Build stranger, harder developer tools                          ║
║  [→] Explore distributed systems and reliability                     ║
║  [→] Make security tooling easier to use                             ║
║  [→] Keep finding problems worth obsessing over                      ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

</div>

### 🌱 Current exploration

`Agentic systems` · `Graph databases` · `AI infrastructure` · `Developer experience` · `Semantic retrieval` · `Distributed systems` · `Security tooling` · `Human-computer interaction`

<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-divider.svg" width="100%" alt="pixel grass divider" />

<a id="achievements"></a>

## 🏆 Achievements Unlocked

<div align="center">
<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-achievements.svg" width="100%" alt="Minecraft-inspired engineering achievements" />
</div>

<table>
<tr>
<td width="33%" align="center">🟩 <b>BUILD FIRST</b><br><sub>Learn by making the thing.</sub></td>
<td width="33%" align="center">💎 <b>MODEL THE HARD PART</b><br><sub>Make the system reflect reality.</sub></td>
<td width="33%" align="center">🔥 <b>BREAK YOUR OWN CODE</b><br><sub>Find the failure before users do.</sub></td>
</tr>
</table>

<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-divider.svg" width="100%" alt="pixel grass divider" />

<a id="world-stats"></a>

## 📊 World Stats

<div align="center">

<img src="https://github-readme-stats.vercel.app/api?username=Rohit-ATS&show_icons=true&hide_border=true&bg_color=0d1117&title_color=6ee77f&text_color=d7e4d5&icon_color=6ee77f&ring_color=6ee77f&cache_seconds=86400" height="180" alt="GitHub statistics" />
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Rohit-ATS&layout=compact&hide_border=true&bg_color=0d1117&title_color=6ee77f&text_color=d7e4d5&icon_color=6ee77f&cache_seconds=86400" height="180" alt="Top languages" />

<br><br>

<img src="https://github-readme-streak-stats.herokuapp.com/?user=Rohit-ATS&hide_border=true&background=0d1117&ring=6ee77f&fire=ffb300&currStreakLabel=6ee77f&sideLabels=9fb09f&dates=6f806f&currStreakNum=eaf5e9&sideNums=eaf5e9" width="78%" alt="GitHub contribution streak" />

<br><br>

<img src="https://github-readme-activity-graph.vercel.app/graph?username=Rohit-ATS&bg_color=0d1117&color=8bd98d&line=5bbf63&point=ffffff&area=true&hide_border=true" width="95%" alt="GitHub activity graph" />

</div>

<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-divider.svg" width="100%" alt="pixel grass divider" />

<a id="rules-of-the-world"></a>

## 🧪 Rules of the World

<table>
<tr><td width="50%"><b>01 · Real data beats pretty demos.</b><br><sub>If the number came from nowhere, the number is lying.</sub></td><td width="50%"><b>02 · Architecture should answer questions.</b><br><sub>A diagram is useful only when the system can actually support it.</sub></td></tr>
<tr><td><b>03 · Tests are part of the feature.</b><br><sub>The boring edge case is usually the one waiting in production.</sub></td><td><b>04 · Security starts in the model.</b><br><sub>Trust boundaries and failure paths belong in design.</sub></td></tr>
<tr><td><b>05 · Measure before claiming.</b><br><sub>Fast, scalable, reliable — each deserves evidence.</sub></td><td><b>06 · Curiosity is a technical skill.</b><br><sub>Getting stuck is fine. Staying stuck because you stopped digging isn't.</sub></td></tr>
</table>

<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-divider.svg" width="100%" alt="pixel grass divider" />

<a id="current-coordinates"></a>

## 🗺️ Current Coordinates

```text
╔══════════════════════════════════════════════════════════════╗
║  WORLD        SOFTWARE                                      ║
║  BIOME        AI / INFRASTRUCTURE                            ║
║  X            developer tools                               ║
║  Y            systems depth                                 ║
║  Z            somewhere between "this should work" and     ║
║               "why is the database doing THAT?"             ║
║                                                              ║
║  WEATHER      ☀ curious                                     ║
║  DIFFICULTY   hard                                           ║
║  INVENTORY    full                                           ║
║  NEXT MOVE    build                                          ║
╚══════════════════════════════════════════════════════════════╝
```

### 🌌 What I'm exploring right now

- How agents become genuinely useful software rather than chat wrappers.
- How graph structures can make security and dependency reasoning easier.
- How semantic systems can make AI infrastructure cheaper and faster.
- How to design developer tools that feel obvious once they exist.
- How to keep ambitious systems understandable as they grow.

<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-divider.svg" width="100%" alt="pixel grass divider" />

<a id="connect"></a>

## ✉️ Connect

<div align="center">

If you're building something ambitious, working on open source, exploring AI infrastructure, or simply love going deep on engineering problems — **say hello.**

<br>

<a href="mailto:rohitmaruriats@gmail.com"><img src="https://img.shields.io/badge/EMAIL-rohitmaruriats%40gmail.com-4CAF50?style=for-the-badge&labelColor=242424&logo=gmail&logoColor=white" alt="Email Rohit" /></a>
<a href="https://www.linkedin.com/in/rohitmaruri/"><img src="https://img.shields.io/badge/LINKEDIN-Rohit%20Maruri-2867B2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
<a href="https://github.com/Rohit-ATS"><img src="https://img.shields.io/badge/GITHUB-Rohit--ATS-111111?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>

<br><br>

<img src="https://raw.githubusercontent.com/Rohit-ATS/Rohit-ATS/main/assets/mc-footer.svg" width="100%" alt="Minecraft-inspired pixel world footer" />

### `keep building. keep learning. keep shipping. ❤️`

<sub>Made with unreasonable curiosity, too much coffee, and a lot of love for code.</sub>

</div>
