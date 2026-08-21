# World-Class Agentic Analytics in Production

Build an analytics agent that can answer with evidence. It should also ask for clarification, route work to review, or refuse when the data and authority are not good enough.

This repository is the companion for a five-hour, hands-on course. You can bring an approved data source or use the included practice lab. The workflow works with Codex, Cursor, Claude Code, or another file-capable harness; Python provides an optional independent check.

The material runs on three linked spines. You learn the production framework, inspect systems Paras built, and practice with an approved source or the included lab.

The live workshop page is the canonical course experience. Share that one URL for class; it contains the agenda, explanations, prompts, examples, checkpoints, practice-data links, reference answers, and exports. The standalone files give students direct access to the prompts and practice lab.

## Start solo. Earn multiplayer.

The course supports three different starting points. Do not begin with enterprise infrastructure when one person is still proving the workflow.

1. **Solo, n=1:** use one harness, one recurring decision, a local folder or private Git repository, approved context, proof, and a small eval set. Modules 0–4 are enough to make your own work faster and safer.
2. **Small team, n=3–10:** put the working contract, context, evals, and corrections in one versioned place. Use Module 5 to prove that another person can run it, flag a miss, review the evidence, and reuse an approved correction.
3. **Organization:** move common guarantees behind a shared MCP or gateway only after the team path works. Add centralized permissions, semantic context, review queues, telemetry, rollout controls, cost limits, and incident ownership in Module 6.

Solo proof earns a team pilot. A team pilot earns shared infrastructure. Two fresh harness sessions can rehearse the multiplayer loop, but another person must complete the handoff before you call it adopted.

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

For the live workshop, download the ZIP rather than cloning the repository. Unzip it, open the extracted `agentic-analytics-lab` folder in a clean local harness session, and disconnect real company data tools. Then run the spoiler-free readiness check when Python is available:

```bash
python3 verify.py --readiness-only
```

The check should report `READINESS: PASS` without calculating the business result. Students who cloned the repository to inspect its source should still open `assets/agentic-analytics-lab/` as the lab root before running prompts.

## What you will build

By the end of the course, you will have:

1. a readiness check that proves what the agent can access;
2. an approved use-case brief and seven-field contract;
3. a client-neutral production architecture;
4. a reviewed metric-context proposal;
5. an executed analysis with independent verification and a proof receipt;
6. an evaluation set and one complete user-feedback → data-admin review → shared correction → fresh-session rerun loop;
7. observed run and review data, production controls, and a one-page Scale, Hold, or Stop launch memo.

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

## License

MIT. See [LICENSE](LICENSE).
