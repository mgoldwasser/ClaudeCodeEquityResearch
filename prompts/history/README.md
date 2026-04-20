# `prompts/history/` — Versioned Agent Prompt Evolution

This directory is the **audit trail** for every prompt edit the meta-learner
has applied to an agent file. One subdirectory per approved proposal.

## Layout

```
prompts/history/
├── <agent-name>/
│   ├── <YYYY-MM-DD>-<slug>/
│   │   ├── before.md        # full agent file pre-edit
│   │   ├── after.md         # full agent file post-edit
│   │   ├── rationale.md     # why this edit, what it costs if wrong
│   │   └── metadata.json    # proposal_id, approved_at, bias stats
```

## Why This Exists

The meta-learner (`tools/meta-learn.py`) proposes prompt edits when a named
agent's residual error shows systematic bias across graded research notes.
Every approved edit is snapshotted here so that:

1. **Every change is auditable** — `git log` tells you when an edit landed;
   the snapshot tells you exactly what the agent looked like before and after.
2. **Reversion is trivial** — if the edit turns out to make things worse over
   the next cohort, you can reset the agent file to `before.md` and commit.
3. **The prompt's evolution is visible** — diffing
   `prompts/history/dcf-analyst/2026-04/before.md` against
   `prompts/history/dcf-analyst/2027-01/after.md` shows how the DCF analyst's
   default assumptions shifted over the year, with the grading evidence behind
   each change sitting in the adjacent `rationale.md`.

## Not a Database

This directory is not queried by any tool at runtime. It is purely a record.
The live agent definition is always `agents/<agent-name>.md`; the history here
is what that file *used to say*.

## Commit Convention

When approving a proposal via `python tools/meta-learn.py review --approve <id>`,
create the follow-up commit with a message of the form:

```
meta-learn: <agent> — <one-line finding>

Approved proposal <id>. N graded notes. Mean residual <±x.x%>.

Lever: <terminal growth | WACC | exit multiple | ...>
Before: <old value>
After:  <new value>

Rationale: <one paragraph from rationale.md>
```

## Scope (v1)

Only `dcf-analyst/` is actively produced at v1. Other agents are out of scope
until their proposers ship in v1.1+ (see `agents/meta-learner.md` → Versioning).
