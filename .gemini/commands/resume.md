# Resume (Gemini)

Load a previously captured snapshot prompt from `tmp/resume/` and continue the work it describes.

When invoked, find the right snapshot file, read it, and **treat its contents as the user's initial instructions for this session.** This is the **load** side of the snapshot/resume pair — `/snapshot` is the save side.

Argument: `$ARGUMENTS` — optional kebab-case slug to filter by. If empty, picks the most recent snapshot regardless of slug.

## Instructions

### Step 1: Find the snapshot file

Files live in `tmp/resume/` with names like `{inv_epoch}-{slug}.md`. The `inv_epoch` prefix is monotonically *decreasing* in time, so the lexically smallest filename is the most recent.

```bash
mkdir -p tmp/resume  # idempotent
```

**If `$ARGUMENTS` is empty:** pick the lexically first file in the directory (newest).

```bash
ls tmp/resume/*.md 2>/dev/null | head -1
```

**If `$ARGUMENTS` is provided:** treat it as a slug fragment. Pick the lexically first file whose name matches `*-${ARGUMENTS}*.md`.

```bash
ls tmp/resume/*-${ARGUMENTS}*.md 2>/dev/null | head -1
```

(Lexically-first = newest, because of the inv_epoch convention.)

### Step 2: Handle edge cases

- **Directory empty or missing:** tell the user `tmp/resume/` has no snapshots; suggest `/snapshot <slug>` to capture one. Stop.
- **No match for the slug:** list available snapshot filenames so the user can pick one. Stop and wait.
- **Multiple matches:** silently pick the newest, but mention how many were considered and offer to load a different one if asked.

### Step 3: Load and act on the snapshot

1. Read the chosen file.
2. Print a one-line confirmation: `Resuming from {filename} ({slug}, captured {date if discoverable})`.
3. **Treat the file's contents as if the user had pasted them as their first message.** Follow the instructions inside — most snapshots end with a "Start by:" line that names a concrete first action; do that. If the snapshot has multiple "Pick" options, default to the recommended one unless the user said otherwise.
4. Don't summarize the snapshot back to the user before acting — they already wrote it. Just proceed. (Exception: if the snapshot is ambiguous about the next step, ask once before acting.)

### Step 4: Honor any "User direction recorded" or constraints in the snapshot

Snapshots typically capture decisions and preferences from the prior session. Treat them as binding for this session unless explicitly overridden in the user's current message.

## Notes

- Snapshots are immutable once written. If the situation has changed since capture (a referenced PR landed, an issue closed, etc.), verify before acting on stale references — `gh issue view <n>`, `git log`, etc.
- The companion `/snapshot` command writes new snapshots — point users to it if they want to capture something for later in this session.
- The `inv_epoch` prefix is a sort-only artifact; the user reads the slug, not the number. Always show the slug (or full filename) in confirmation messages, not just the prefix.
