# Step 0: Prove readiness

Run this before asking the business question. It establishes the source, context, permissions, and write boundary.

```text
This session is for the extracted agentic-analytics lab only. Before reading the data, list every connected tool and MCP. If the tool list includes ChatData, a warehouse, a company MCP, or any other real-data or externally write-capable tool, stop and tell me to disconnect it. Do not call external tools.

Confirm that the current folder is the lab root and contains README.md, verify.py, data/, context/, evals.yaml, and work/. Treat data/ and context/ as read-only. Write every generated artifact only under work/. Every work/... path is relative to this folder.

Do not analyze the business question yet. List the local files you can access, row counts and date bounds, the business and metric context you found, and your access limits. Run one harmless local read check. If anything required is missing, stop and name the smallest repair. Save the result as work/00_readiness.md.
```

Stop when the harness can name the active source and context, prove a harmless read, and state what it cannot access or do.
