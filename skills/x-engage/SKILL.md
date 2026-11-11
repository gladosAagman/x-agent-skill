---
name: x-engage
description: >-
  Keep the user's X reply round honest - log who they replied to, catch drift
  onto the same three accounts, track the reach / peer / buyer mix from the
  weekly plan, and surface the accounts on their list they have gone quiet
  on. Use when the user says "who should I reply to today", "log this reply",
  "who have I been replying to", "am I neglecting anyone", or runs their
  daily engagement round.
---

# x-engage

For a small account on X, replies under bigger accounts are most of the
growth. `/x-plan` sets the list: 5 reach, 3 peers, 2 buyers. Without a record
two things happen. The round collapses onto the three accounts that reply
back, which everyone reading those threads can see. And the buyers, the
accounts the user meant to warm up for weeks before a DM, get dropped.

One tool lives in this folder and it runs:

```bash
python3 targets.py add @sarahbuilds --tier reach --note "added our churn number"
python3 targets.py report                     # the last 7 days
python3 targets.py due --roster roster.txt    # who on the list has gone quiet
```

The ledger is a CSV at `~/.claude/x/engage.csv`. It validates handles (letters,
digits, underscore, 15 at most), it never opens X and it never posts.

## The roster

The ten from `/x-plan`, in `~/.claude/x/roster.txt`, one per line,
`handle,tier`:

```
@sarahbuilds,reach
@devon_k,peer
@dana_ops,buyer
```

## The daily round

1. `targets.py due --roster ~/.claude/x/roster.txt`. Most overdue first.
2. The user pastes those accounts' latest posts. `/x-comment` drafts the
   replies, in batch mode.
3. The user posts each reply by hand, early, then logs it with
   `targets.py add`.

## The weekly read

`targets.py report --days 7`: count per account, the share the top three
took, and the tier mix against 50 / 30 / 20. It warns when three accounts
took over half the round, and when a tier fell below half its target.

Replies between accounts that follow each other get a boost in X's published
ranker (`python3 ../x-plan/weights.py`), which is why the peer tier matters.
Peers who never reply back after two weeks get replaced in next week's
`/x-plan`.

## Never

- Never reply, like, follow or DM on the user's behalf, and never drive a
  browser to do it. X's automation rules prohibit automated replies, likes
  and bulk follows.
- Never log a reply the user did not make.
