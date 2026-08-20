# World-Class Agentic Analytics in Production

Build an analytics agent that can answer with evidence. It should also ask for clarification, route work to review, or refuse when the data and authority are not good enough.

This repository is the companion for a five-hour, hands-on course. You can bring an approved data source or use the included synthetic lab. The workflow works with Codex, Cursor, Claude Code, or another file-capable harness.

## Start here

- [Open the live workshop](https://parasdoshicom.github.io/world-class-agentic-analytics-in-production/)
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
| [`assets/agentic-analytics-lab/`](assets/agentic-analytics-lab/README.md) | Synthetic data, approved context, SQL, evals, and verifier |
| [`assets/agentic-analytics-workshop-lab.zip`](assets/agentic-analytics-workshop-lab.zip) | Downloadable copy of the full lab |
| [`scripts/validate_course.py`](scripts/validate_course.py) | Link, prompt-sync, ZIP-integrity, and public-safety checks |
| [`.github/workflows/quality-and-pages.yml`](.github/workflows/quality-and-pages.yml) | Tests every change and refreshes GitHub Pages from `main` |

## Updating the course

Edit the smallest owning file. If a prompt changes, update both `index.html` and its matching file under `prompts/`. If the lab changes, rebuild the lab ZIP so the browser download matches the visible source.

Before pushing:

```bash
python3 scripts/validate_course.py
cd assets/agentic-analytics-lab
python3 verify.py
```

A push to `main` runs the same checks and publishes the refreshed workshop through GitHub Pages.

## Evidence boundary

The included case and results are synthetic. They show the operating pattern. This repository does not claim that a specific customer uses this system or achieves these results.

## License

MIT. See [LICENSE](LICENSE).
