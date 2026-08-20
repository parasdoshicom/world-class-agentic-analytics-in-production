# Step 2: Draft and break the contract

```text
Using the approved use-case brief, draft a seven-field contract:
1. user and decision forum
2. decision and action supported
3. required output
4. evidence required before answering
5. what the agent may do
6. when it must Clarify, Review, or Refuse
7. human owner

Then try to break the contract with one vague request and one forbidden action. Revise it once.

Also draw the request path from harness to tool/MCP contract, approved context, scoped source, validation, proof, human review, and correction memory. Label which component owns permissions, persistence, versioning, and each failure.

List the minimum tools this path needs. For each tool, record its purpose, required inputs, read/write scope, risk tier, and overlap with other tools. Remove or rename any tool when it is unclear which one the agent should choose. Start with one agent unless an observed evaluation failure justifies another.

Apply the Rule of Two to this session:
- A: can it process untrusted input?
- B: can it access sensitive systems or private data?
- C: can it change state or communicate externally?
If A, B, and C are all present, require human approval or redesign the session before granting autonomy.

Save work/02_contract.yaml and work/02_architecture.md. Mark unknown owners instead of inventing them.
```

The contract should bound a decision and action. The architecture should show where each guarantee is enforced outside the client prompt.
