# Phase Transition Safety Protocol (Rules)

This protocol enforces strict verification gates before any AI Agent or Developer transitions the project from one development phase to the next.

---

## 1. Phase Transition Gates (The Checklist)

Before declaring any Phase complete and moving to the next:

### A. Code & Quality Gate
- [ ] **Zero Unhandled Errors:** All main paths run cleanly without runtime crashes.
- [ ] **Type Checking:** Zero TypeScript or Python type-checker errors (`tsc --noEmit` or `mypy` passes).
- [ ] **Linter Check:** All linting checks pass with zero fatal warnings (`npm run lint` or `ruff check`).

### B. Testing & Validation Gate
- [ ] **Unit / Integration Tests:** All tests pass with 100% success rate on existing test suites.
- [ ] **Edge Case Verification:** Boundary conditions and invalid inputs tested on newly introduced endpoints/features.

### C. Security & Environment Gate
- [ ] **No Exposed Secrets:** Hardcoded API keys, DB strings, or tokens removed from codebase.
- [ ] **Environment Audit:** All new `.env` variables documented in `.env.example`.
- [ ] `.gitignore` Audit: Verification that `.env`, logs, and build artifacts are explicitly ignored.

### D. Documentation & Memory Gate
- [ ] **Short-Term Memory Sync:** Completed tasks cleared from `short_term_memory.md`.
- [ ] **Long-Term Memory Sync:** Key architectural changes or new models appended to `long_term_memory.md`.
- [ ] **Git State Sync:** Working directory clean; code committed with clear convention (`feat:`, `fix:`, `refactor:`).

---

## 2. Violation Protocol
If any check fails:
1. **HALT:** Do not begin tasks in the next Phase.
2. **LOG:** Create a Blocker entry in `short_term_memory.md`.
3. **REMEDIATE:** Fix the issue in the current phase context before requesting phase approval.
