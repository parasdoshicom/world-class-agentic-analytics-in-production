# World-Class Agentic Analytics in Production

Build an analytics agent that can answer with evidence. It should also ask for clarification, route work to review, or refuse when the data and authority are not good enough.

This repository is the companion for a five-hour, hands-on course. You can bring an approved data source or use the included practice lab. The workflow works with Codex, Cursor, Claude Code, or another file-capable harness.

The material runs on three linked spines. You learn the production framework, inspect systems Paras built, and practice with an approved source or the included lab.

The live workshop page is the canonical student and instructor experience. Share that one URL for class; it contains the agenda, explanations, prompts, examples, checkpoints, practice-data links, reference answers, and exports. The standalone repository files are optional direct-access copies and testable source material.

## The operating model

Trustworthy agentic analytics needs three connected parts:

1. a semantic model that tells the agent what metrics mean, which sources to use, and which logic the data team has approved;
2. a feedback path where users can flag a wrong answer or say they could not validate it;
3. a data-admin review path that turns the accepted correction into shared context and a regression test.

The flywheel begins when the agent misses and the user flags the gap. The data team settles the canonical answer, updates the shared context and tests, and improves the next run.

The course checks that model against published practices from [OpenAI](https://openai.com/index/inside-our-in-house-data-agent/), [Anthropic](https://www.anthropic.com/engineering/building-effective-agents), [Meta](https://ai.meta.com/blog/practical-ai-agent-security/), and [Ramp](https://engineering.ramp.com/post/meet-ramp-research). The prompts and exercises turn that guidance into work instead of leaving it as a reading list.

## Start here

- [Open the live workshop](https://parasdoshicom.github.io/world-class-agentic-analytics-in-production/)
- [See the systems Paras built](https://parasdoshicom.github.io/world-class-agentic-analytics-in-production/#paras-built)
- [Run the prompts in order](prompts/README.md)
- [Download the complete lab](https://parasdoshicom.github.io/world-class-agentic-analytics-in-production/assets/agentic-analytics-workshop-lab.zip)
- [Inspect the lab before downloading](assets/agentic-analytics-lab/README.md)

If you have no warehouse connection, clone this repository and run:

```bash
cd assets/agentic-analytics-lab
python3 verify.py
```

The clean lab should report `OUTCOME: Review`, with qualified-signup conversion moving from 8.4% to 6.9%. Review is the correct state because the supplied business context documents a tagging change close to the movement.

## What you will build

By the end of the course, you will have:

1. a readiness check that proves what the agent can access;
2. an approved use-case brief and seven-field contract;
3. a client-neutral production architecture;
4. a reviewed metric-context proposal;
5. an executed analysis with independent verification and a proof receipt;
6. an evaluation set, one controlled failure, a correction, and a rerun;
7. production controls and a one-page Scale, Hold, or Stop launch memo.

Generated work stays under the lab's `work/` directory. The supplied `data/` and `context/` directories are read-only inputs.

## Repository map

| Path | Purpose |
| --- | --- |
| [`index.html`](index.html) | The canonical one-page course and browser workbook |
| [`prompts/`](prompts/README.md) | Eight copyable prompts, from readiness through launch |
| [`examples/paras-built/`](examples/paras-built/README.md) | War Room, Abandonment Intelligence, and data-agent design examples |
| [`assets/case-studies/`](assets/case-studies/) | Screenshots used in the course case studies |
| [`assets/agentic-analytics-lab/`](assets/agentic-analytics-lab/README.md) | Practice CSV data, approved context, evals, and verifier |
| [`assets/agentic-analytics-workshop-lab.zip`](assets/agentic-analytics-workshop-lab.zip) | Downloadable copy of the full lab |
| [`scripts/validate_course.py`](scripts/validate_course.py) | Link, prompt-sync, ZIP-integrity, and course checks |
| [`scripts/validate_student_journey.py`](scripts/validate_student_journey.py) | Clean-download, filename, CSV, prompt-output, verifier, and write-boundary checks |
| [`tests/course.spec.js`](tests/course.spec.js) | Browser acceptance checks for controls, downloads, preview data, export, and mobile layout |
| [`.github/workflows/quality-and-pages.yml`](.github/workflows/quality-and-pages.yml) | Tests every change and refreshes GitHub Pages from `main` |

## Updating the course

Edit the smallest owning file. If a prompt changes, update both `index.html` and its matching file under `prompts/`. If the lab changes, rebuild the lab ZIP so the browser download matches the visible source.

Before pushing:

```bash
python3 scripts/validate_course.py
python3 scripts/validate_student_journey.py
npm ci
npm run test:browser
cd assets/agentic-analytics-lab
python3 verify.py
```

A push to `main` runs the same checks and publishes the refreshed workshop through GitHub Pages.

## License

MIT. See [LICENSE](LICENSE).
