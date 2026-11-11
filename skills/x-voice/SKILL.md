---
name: x-voice
description: >-
  Measure the user's actual X voice from their own past posts and write
  voice.md from evidence, then check any draft for drift before it goes out.
  Use when the user says "write my voice.md", "learn how I write", "does this
  sound like me", "this doesn't sound like me", "make it sound more like me",
  sets up the pack for the first time, or pastes a batch of their own posts.
---

# x-voice

Every skill in this pack reads `~/.claude/x/voice.md`. Filled in by hand, it
says how the user would like to sound. Measured from their posts, it says how
they do sound. On X that gap is visible in one line: someone who writes in
lower-case with no full stops gets a draft in sentence case with a semicolon,
and the replies notice before the user does.

One tool lives in this folder and it runs:

```bash
python3 voice.py samples.txt                              # measure, print the profile
python3 voice.py samples.txt --save ~/.claude/x/voice.json
python3 voice.py --profile ~/.claude/x/voice.json --check draft.txt
```

## Input

Ten to twenty of the user's own posts, one file, `---` on its own line between
posts. Posts they wrote themselves, not ones a tool wrote. Replies count too,
and on X they are often the truest sample of how someone talks.

Fewer than five and the tool says so. Do not pad the sample with posts you
drafted for them: that measures you.

## What it measures

Sentence length and spread, contractions, I / we / you, questions and
exclamations, **casing** (the one that matters most on X), emoji, em dashes,
numbers, length in words and lines, the words that recur across posts, and
how posts open. Each is a mean and a spread, so a draft is judged against the
user's own range.

## Then write voice.md

1. `voice.py samples.txt --save ~/.claude/x/voice.json`
2. Fill `templates/voice.md` from what the user tells you: audience, positions,
   niche accounts, off limits, proof.
3. Paste the **Measured voice** block under "What I sound like on X". Where the
   hand-written answers disagree with the measurement, say so. The
   measurement wins unless the user is changing on purpose.
4. Save to `~/.claude/x/voice.md`.

## Checking a draft

`--check` scores 0-100 against the profile, names the metric furthest from the
user, and raises hard flags: emoji or an em dash when they never use one,
sentence case when they write lower-case, no contractions when they always use
them. `/x-preflight` runs this automatically when the profile exists.

Under 25 words, sentence rhythm cannot be judged and sits out as n/a, the same
way `/x-human` handles short posts.

## Say this honestly

Stylometry on a small sample. It catches drift. It cannot tell you a post is
good, and it is not a way to imitate someone else: run it on the user's own
writing only.
