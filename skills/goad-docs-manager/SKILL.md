---
name: goad-docs-manager
description: Canonical orchestrator for the HACKLAB/GOAD Second Brain. Use when performing bulk documentation updates, auditing lab state, or managing AI-to-AI handoffs in the GOAD homelab environment.
---

# GOAD Docs Manager

## Overview
This skill provides the procedural guardrails and workflow logic for managing the GOAD Homelab documentation vault. It ensures compliance with safety rules, maintains the session "Load Order," and facilitates token-efficient handoffs between AI agents (Claude, Gemini, LM Studio).

## Core Principles
1. **Safety First:** Adhere to `15-ai-agents/agent-safety-rules.md` without exception.
2. **Context Integrity:** Maintain `10-llm-context/HOMELAB-CONTEXT-PACK.md` as the single source of truth.
3. **Token Efficiency:** Offload prose to Scribe (LM Studio) and bulk execution to Gemini.

## Mandatory Load Order
Before any task, you MUST read the following files in order:
1. `15-ai-agents/agent-safety-rules.md`
2. `10-llm-context/HOMELAB-CONTEXT-PACK.md`
3. `NEXT-ACTIONS.md`
4. `SKILLS.md`

## Workflow: Documentation Audit & Update
When auditing or updating the vault:
1. **Research:** Map the relevant vault sections (e.g., `03-inventory` for hardware changes).
2. **Verification:** Use manual commands (e.g., `ip addr`, `virsh list`) or lab scripts (e.g., `16-ai-bridge/tools/scan-ip-drift.py`) to verify documentation against reality.
3. **Drafting:** 
   - Use **Scribe** (via `15-ai-agents/skills/scribe/scribe.py`) for large prose blocks.
   - Follow the **Frontmatter Convention** (YAML at top of files).
4. **Approval:** Present a `git diff --stat` and the specific `git add` commands. Wait for user approval.
5. **Audit:** Append an entry to `/mnt/nas/goad-docs/evidence/audit/audit.log` for any state-modifying action.
6. **Cleanup:** Update `17-state/current.yaml` and `NEXT-ACTIONS.md` at the end of the session.

## Token Optimization Guidelines
- **Task Shifting:** Hand off bulk execution from Claude to Gemini by crafting a "Prompt Blob" (see `00-meta/prompt-templates/`).
- **Pruning:** Do not read the entire vault unless necessary. Use `grep_search` to find relevant files.
- **Scribe Handoff:** If an output requires more than 200 tokens of prose, draft it using Scribe templates in `15-ai-agents/skills/scribe/templates/`.

## Resources
- **references/safety-rules-summary.md**: Quick-reference guide for safety limits.
- **references/token-optimization.md**: Best practices for saving tokens across subscriptions.
