# Rule: Memory Generation & Synchronization Protocol

## Objective
This rule instructs the AI Agent to automatically inspect the codebase and generate or update two core persistent state files: `long_term_memory.md` and `short_term_memory.md` under the `.agents/memory/` directory.

---

## 1. Trigger Conditions
Execute this memory generation protocol whenever:
1. **Project Initialization:** The `.agents/memory/` files are missing or empty.
2. **Session Start:** The user begins a new conversation or asks to resume context.
3. **Task Completion:** A significant feature, bug fix, or refactor is completed.
4. **Phase Transition:** Moving from one feature phase or sprint to the next.
5. **Explicit Command:** The user types `/sync-memory` or asks to generate/update project memory.

---

## 2. Memory Generation Instructions

### Step 1: Scan and Inspect Codebase
The agent MUST run system inspection commands (or inspect file structures) to extract context:
- Scan directory tree to identify stack (e.g., `package.json`, `requirements.txt`, `prisma/schema.prisma`, `Dockerfile`).
- Check `git status` and recent commit logs to identify active changes.
- Check `.env.example` to understand required environment configs.

---

### Step 2: Generate / Update `long_term_memory.md`
Write or update `.agents/memory/long_term_memory.md` using the standard structure:

```markdown
# Long-Term Memory (LTM)

## 1. Executive Project Overview
- **Project Name:** [Extract from root package/repo name]
- **Core Purpose:** [Extract high-level business logic / purpose]
- **Primary Tech Stack:** [Languages, Frameworks, DBs, ORMs, UI Libraries]

## 2. Architectural Blueprint & Core Principles
- **Pattern:** [e.g., MVC, Modular Monolith, Serverless, Microservices]
- **Design Rules:** Type safety, modularity, environment separation.
- **Core Invariants:** Non-negotiable security, schema validation, and config rules.

## 3. Persistent Decisions Log (ADRs)
- Maintain a running table of key architectural choices (e.g., Auth strategies, DB choices, third-party API integrations).

## 4. Environment & Tooling Configuration
- Package managers, test runners, linter configurations, and deployment setups.

### Step 3: Generate / Update short_term_memory.md
Write or update .agents/memory/short_term_memory.md using the active session context:
# Short-Term Memory (STM)

## 1. Active Development Context
- Current sprint/phase and active component being developed or debugged.

## 2. Immediate Task Checklist
- Checkbox list (`[ ]`, `[/]`, `[x]`) tracking current active sub-tasks.

## 3. Active Blockers & Dependencies
- Pending approvals, missing API keys, or upstream bugs hindering progress.

## 4. Session Scratchpad & Temporary Notes
- Temporary debug commands, working routes, curl examples, or test logs.

### Three important Execution Rules
 1. Never Overwrite ADRs: Long-term memory history should only be appended to, never deleted.

 2. Keep Short-Term Memory Lean: Once tasks in short-term memory are verified and completed, archive or clear them.

 3. Always Maintain Folder Structure: Ensure files always reside in .agents/memory/.