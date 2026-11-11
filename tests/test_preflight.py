"""Tests for x-preflight: the stages compose the original tools correctly."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SK = os.path.join(ROOT, "skills")
sys.path.insert(0, os.path.join(SK, "x-preflight"))

import preflight   # noqa: E402

GOOD = "I raised prices 40% in March and lost 2 of 31 clients.\n\nThe two we lost were the two we argued with most.\n"
BAD = "x" * 300


def tmp(text):
    f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
    f.write(text)
    f.close()
    return f.name


class PreflightTests(unittest.TestCase):
    def test_good_post_is_ready(self):
        r = preflight.run(GOOD, profile_path=None)
        stages = {s["stage"]: s["status"] for s in r["stages"]}
        self.assertTrue(r["ready"], r)
        self.assertEqual(stages["COUNT"], "PASS")
        self.assertIn("HOOK", stages)

    def test_over_limit_blocks(self):
        r = preflight.run(BAD)
        self.assertFalse(r["ready"])
        self.assertEqual(r["stages"][0]["status"], "FAIL")

    def test_premium_lets_long_post_fit(self):
        r = preflight.run(GOOD + ("More detail here. " * 40), premium=True)
        self.assertNotEqual(r["stages"][0]["status"], "FAIL")

    def test_reply_skips_hook(self):
        r = preflight.run(GOOD, kind="reply")
        self.assertNotIn("HOOK", [s["stage"] for s in r["stages"]])

    def test_unreadable_profile_is_skipped_not_fatal(self):
        r = preflight.run(GOOD, profile_path=tmp("not json"))
        self.assertEqual([s for s in r["stages"] if s["stage"] == "VOICE"][0]["status"], "SKIP")

    def test_cli_exit_codes(self):
        tool = os.path.join(SK, "x-preflight", "preflight.py")
        ok = subprocess.run([sys.executable, tool, tmp(GOOD), "--json"], capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertTrue(json.loads(ok.stdout)["ready"])
        self.assertEqual(subprocess.run([sys.executable, tool, tmp(BAD)], capture_output=True).returncode, 1)
        self.assertEqual(subprocess.run([sys.executable, tool, tmp("  ")], capture_output=True).returncode, 2)


if __name__ == "__main__":
    unittest.main()
