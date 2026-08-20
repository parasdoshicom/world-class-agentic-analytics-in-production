# Systems Paras built

These examples show how recurring analytics questions became products people could inspect, challenge, and use. The visible numbers use the included course dataset so you can follow the same path yourself.

## Acquisition War Room

[Open the full example](acquisition-war-room.html)

The War Room is the executive sensing layer. It turns a recurring operating question into one reviewed briefing:

1. state what changed;
2. decompose the movement;
3. compare it with an independent benchmark;
4. show freshness, caveats, and verification state;
5. recommend the next investigation without overstating causality.

The design used parallel specialist agents for headline metrics, deep dives, segment or market movement, qualitative signals, and business context. Each specialist returned a compact analyzed summary. The synthesis step assembled the briefing and preserved the validation state.

## Abandonment Intelligence

[Open the full example](abandonment-intelligence.html)

Abandonment Intelligence is the investigation-and-action layer. It rejects a generic finding such as “conversion is down.” A useful finding names the affected population, the broken rule or flow, and the durability evidence. It also needs an owner, a work item or next test, and a confidence level.

The design used parallel investigators across funnel breakpoints plus operational signals, then ranked the findings into an action list.

## Conversational Data Agent

The conversational agent is the front door. It routes direct questions, investigations, and recurring briefings through approved sources and review rules. One early test produced a fluent but incorrect answer after choosing the wrong source. That failure drove the visible SQL, source citation, semantic context, validation, caching, time-window, security, and PII controls taught in this course.

Use the examples to ask five questions: What decision is this helping someone make? Which meaning and source does it trust? What can the user verify? When does it ask for review? How does a correction improve the next run?
