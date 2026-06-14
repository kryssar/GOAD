# Token Optimization Best Practices

## Subscription Allocation
- **Claude (Architect)**: Use for high-reasoning planning, ADR design, and complex debugging. Keep sessions short.
- **Gemini (Bulk Executor)**: Use for reading large files, multi-file edits, and initial codebase/vault audits. 1M token window allows for holding the whole vault.
- **LM Studio (Scribe)**: Use for all prose generation (session logs, reports, ADR drafts). Free tokens on local GPU.

## Context Pruning
- **Don't use `cat` on folders**: Use `grep_search` to find specific strings first.
- **Dense Context Packs**: Keep `10-llm-context/HOMELAB-CONTEXT-PACK.md` updated and dense. It should be the first file read by any agent.
- **Modular Load Order**: Only load the role-specific agent file (e.g., `attacker-agent.md`) when performing that role.

## Communication Patterns
- **Prompt Blobs**: When switching from Claude to Gemini, have Claude generate a structured JSON or Markdown blob that Gemini can consume. This prevents Gemini from having to re-derive the plan from a messy chat history.
- **MCP Offloading**: Use MCP servers (like the Proxmox bridge) to allow agents to query state directly without the user having to copy-paste CLI output.
