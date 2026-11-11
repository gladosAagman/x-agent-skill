---
name: x-crisis
description: >-
  Handle a post that went wrong on X - a pile-on, a ratio, a factual mistake,
  a misread joke, a screenshot of the user circulating out of context - and
  decide between correcting, clarifying, apologising, or saying nothing, then
  draft exactly that. Use when the user says "I'm getting ratioed", "this
  blew up badly", "people are angry at my post", "should I delete this",
  "how do I apologise", "someone quote-tweeted me to dunk", or is in the
  middle of a pile-on.
---

# x-crisis

The first hour of a bad post decides how long it lasts. Most of the damage
in a pile-on comes from the second post: the defensive reply, the sarcastic
quote, the deletion followed by a screenshot of the deleted post. This skill
slows that down and picks one move.

## First, the facts

Ask, in one batched question, and do not draft anything until you have them:

1. **The post**, exactly as posted, and when.
2. **What people are saying**, pasted: the ten most-liked replies and quotes,
   not the worst ones. The worst ones are not representative; the most-liked
   ones are what new readers see.
3. **Is any of it right?** The user's honest answer, in private.
4. **What is at stake:** employer, clients, legal exposure, someone's safety.
   If there is legal or safety exposure, say plainly that this needs a person
   (a lawyer, an employer's comms team, the platform's reporting tools), and
   stop here.

## Then sort it

| what happened | the move |
| --- | --- |
| **A factual error** | Correct it, in a reply to the original, today. Say what was wrong and what is right. No "for those who misunderstood". |
| **Right, but read wrong** | One clarifying reply. If the same misreading appears in most top replies, the post was unclear, and that is on the post. |
| **Wrong, and it hurt people** | Apologise. One post, named harm, no "if anyone was offended", no explanation of intent. Then stop posting about it. |
| **A disagreement, loudly** | Nothing, or one reply to the best-faith critic. Volume is not evidence of being wrong. |
| **Bad faith / brigading** | Nothing. Mute, block, hide replies, report what breaks the rules. A reply gives it reach. |

## Delete or keep

- **Delete** when the post contains a factual error that could hurt someone,
  private information, or something the user now believes is wrong. Say that
  it was deleted and why, in one line, because screenshots outlive deletions.
- **Keep** when it is a defensible position people disagree with. Deleting
  that reads as conceding the bad-faith version.

## What the ranker does here

X's published weights put mute, block, "not interested" and report far below
zero (`python3 ../x-plan/weights.py`). A defensive reply or a dunk-quote
creates exactly those signals, from the people already annoyed. That is the
practical case for saying less.

## Drafting

Every draft here is short and plain, then goes through `/x-human` and
`/x-preflight --kind reply`. A crisis reply with an em dash or a stock phrase
in it reads as a PR team, which is worse than silence.

Then a 48-hour plan: what not to post (anything about it, any subtweets), when
normal posting resumes, and which replies to leave unanswered.

## Never

- Never post, delete, block or report on the user's behalf.
- Never draft a reply that attacks a specific critic by name.
- Never invent context ("I was hacked", "it was a joke") the user did not
  confirm as true.
