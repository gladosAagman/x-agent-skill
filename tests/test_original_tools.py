"""Regression tests for the nine tools that shipped in v1.

These pin the behaviour the README documents, so v2 work cannot silently
change it. No network: weights.py runs --offline, pull.py is tested on its
parsers only.
"""

from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SK = os.path.join(ROOT, "skills")
for sub in ("x-post", "x-thread", "x-human", "x-viral"):
    sys.path.insert(0, os.path.join(SK, sub))

import count       # noqa: E402
import hookscore   # noqa: E402
import pull        # noqa: E402
import thread      # noqa: E402


def run(tool, *args, stdin=None):
    return subprocess.run([sys.executable, os.path.join(SK, tool), *args], input=stdin,
                          capture_output=True, text=True, timeout=60)


def tmp(text, suffix=".txt"):
    f = tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False, encoding="utf-8")
    f.write(text)
    f.close()
    return f.name


class CountTests(unittest.TestCase):
    def test_link_is_23(self):
        self.assertEqual(count.weighted("https://example.com/a/very/long/path/that/goes/on")[0], 23)

    def test_emoji_is_2_even_when_composed(self):
        self.assertEqual(count.weighted("👨‍👩‍👧‍👦")[0], 2)
        self.assertEqual(count.weighted("🇬🇧")[0], 2)

    def test_ellipsis_and_cjk_are_2(self):
        self.assertEqual(count.weighted("…")[0], 2)
        self.assertEqual(count.weighted("日本")[0], 4)

    def test_latin_is_1(self):
        self.assertEqual(count.weighted("hello")[0], 5)

    def test_over_limit_fails_and_exits_1(self):
        a = count.analyse("x" * 281)
        self.assertFalse(a["fits"])
        self.assertEqual(a["checks"][0]["status"], "FAIL")
        self.assertEqual(run("x-post/count.py", "-", stdin="x" * 281).returncode, 1)

    def test_premium_allows_long_and_draws_fold(self):
        a = count.analyse("word " * 200, premium=True)
        self.assertTrue(a["fits"])
        self.assertIsNotNone(a["fold"])

    def test_lints(self):
        a = count.analyse("A thread 🧵 on growth #a #b #c\n\nThoughts?")
        status = {c["check"]: c["status"] for c in a["checks"]}
        self.assertEqual(status["FIRST LINE"], "WARN")
        self.assertEqual(status["HASHTAGS"], "WARN")
        self.assertEqual(status["ENDING"], "WARN")

    def test_empty_input_exits_2(self):
        self.assertEqual(run("x-post/count.py", "-", stdin="   ").returncode, 2)


class HookTests(unittest.TestCase):
    def test_strong_beats_weak(self):
        good = hookscore.score_payload("I posted every day for 90 days. Here's what actually moved the numbers.")
        bad = hookscore.score_payload("Hey guys, here are some thoughts on growing on X")
        self.assertGreater(good["score"], bad["score"])
        self.assertTrue(bad["flags"])

    def test_thread_label_is_dealbreaker(self):
        self.assertTrue(hookscore.score_payload("A thread 🧵")["flags"])

    def test_classifies_formula(self):
        self.assertIsNotNone(hookscore.classify("Nobody tells you your first 1,000 followers come from replies")[0])

    def test_hooks_json_has_21_with_regex(self):
        with open(os.path.join(SK, "x-post", "hooks.json"), encoding="utf-8") as fh:
            hooks = json.load(fh)["hooks"]
        self.assertEqual(len(hooks), 21)
        for h in hooks:
            for k in ("template", "example", "match"):
                self.assertIn(k, h)


class ThreadTests(unittest.TestCase):
    def test_every_post_fits(self):
        text = "\n\n".join(f"Point {i}. " + "This is a sentence that carries an idea. " * 6 for i in range(8))
        posts, _ = thread.build(text, number=True)
        self.assertGreater(len(posts), 1)
        for p in posts:
            self.assertLessEqual(p["weighted"], 280)
        self.assertTrue(posts[-1]["text"].endswith(f"{len(posts)}/{len(posts)}"))

    def test_explicit_separators_respected(self):
        posts, explicit = thread.build("one\n---\ntwo\n---\nthree")
        self.assertTrue(explicit)
        self.assertEqual([p["text"] for p in posts], ["one", "two", "three"])


class HumanTests(unittest.TestCase):
    def test_strips_dash_and_invisibles_keeps_zwj_emoji(self):
        src = tmp("We delve into this — it​ is robust. 👨‍💻 ships.\n")
        out = src + ".out"
        r = run("x-human/humanize.py", src, "-o", out)
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(out, encoding="utf-8") as fh:
            text = fh.read()
        self.assertNotIn("—", text)
        self.assertNotIn("​", text)
        self.assertNotIn("delve", text.lower())
        self.assertIn("👨‍💻", text)

    def test_detect_scores_rewrite_higher(self):
        bad = tmp("In today's fast-paced world, it is crucial to leverage robust synergies — "
                  "moreover, we must delve into the tapestry of growth. Let that sink in.\n")
        good = tmp("I raised prices 40% in March and lost 2 of 31 clients. The two we lost were the two "
                   "we argued with most. I'd do it again, and I'd do it sooner.\n")
        r = run("x-human/detect.py", bad, good, "--json")
        payload = json.loads(r.stdout)
        self.assertLess(payload[0]["human_score"], payload[-1]["human_score"])


class ViralTests(unittest.TestCase):
    def test_swipe_ranks_by_own_median(self):
        rows = ["url\taccount\ttext\tviews"]
        for acct, base in (("big", 100000), ("small", 1000)):
            for i in range(6):
                rows.append(f"https://x.com/{acct}/status/{i}\t@{acct}\tPost number {i} about things\t{base}")
        rows.append("https://x.com/small/status/99\t@small\tThe hottest new design tool is a text file.\t9000")
        r = run("x-viral/swipe.py", tmp("\n".join(rows) + "\n", ".tsv"), "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("text file", r.stdout)

    def test_pull_parses_only_post_urls(self):
        urls = pull.parse_urls(["https://x.com/a/status/123", "https://example.com/x", "not a url"])
        self.assertEqual(len(urls), 1)


class AuditTests(unittest.TestCase):
    def test_audit_runs_and_sets_replies_aside(self):
        path = tmp("", ".csv")
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["Post text", "Date", "Impressions", "Likes", "Replies", "Reposts"])
            for i in range(20):
                w.writerow([f"Post {i} with a number {i * 3}", "2026-09-%02d" % (i + 1), 1000 + i * 10, 20, 3, 1])
            w.writerow(["@someone great point", "2026-09-25", 500, 2, 0, 0])
        r = run("x-audit/audit.py", path, "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertEqual(d["posts"], 20)
        self.assertEqual(d["replies_set_aside"], 1)


class WeightsTests(unittest.TestCase):
    def test_offline_mode_runs(self):
        r = run("x-plan/weights.py", "--offline")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("reply", r.stdout.lower())


if __name__ == "__main__":
    unittest.main()
