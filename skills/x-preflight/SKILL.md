---
name: x-preflight
description: >-
  Run every check in the pack on one X draft - X's weighted character count,
  links, hashtags and bait, the hook score on line 1, the five-check
  humanizer panel, and drift from the user's measured voice - and return one
  READY or FIX FIRST verdict with the fixes in order. Use before any post or
  reply goes out, or when the user says "check this", "is this ready",
  "preflight", "can I post this".
---

# x-preflight

Four tools, one answer. The check that gets skipped is the one that would have
caught it, so this runs all of them on the same text.

```bash
python3 preflight.py draft.txt
python3 preflight.py draft.txt --premium        # long post: 25,000, fold at 280
python3 preflight.py reply.txt --kind reply      # no hook stage
```

| stage | tool | fails when |
| --- | --- | --- |
| COUNT | `../x-post/count.py` | over the weighted limit |
| HOOK | `../x-post/hookscore.py` | line 1 scores under 50 (posts only) |
| HUMAN | `../x-human/detect.py` | the panel says FLAGGED |
| VOICE | `../x-voice/voice.py` | the draft drifted from the measured voice (only when `~/.claude/x/voice.json` exists) |

Warnings do not block; they are listed in the order to fix them.

## Order of operations

1. Draft with `/x-post`, `/x-thread` (run each post), `/x-comment` or
   `/x-reply`.
2. `humanize.py` from `/x-human`, then rewrite the flagged lines by hand.
3. `preflight.py` on the result.
4. FIX FIRST: fix item 1, run it again. READY: show the text, then the table.
   Never the table alone.

## What READY does not mean

Nothing mechanical is wrong. It is not a reach prediction: `hookscore.py`
is a lint, and the README says what it can and cannot separate. A READY post
with nothing true in it is still empty.

Nothing is posted by this skill.
