import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from review_guard import main, skip_reason


def fail():
    raise AssertionError("should not be called")


class SkipReasonTest(unittest.TestCase):
    def test_empty_approval_is_skipped(self):
        self.assertEqual(
            skip_reason("approved", "", lambda: 0, fail), "empty approval"
        )

    def test_whitespace_body_counts_as_empty(self):
        self.assertEqual(
            skip_reason("approved", "  \n", lambda: 0, fail), "empty approval"
        )

    def test_approval_with_comments_runs(self):
        self.assertIsNone(skip_reason("approved", "", lambda: 2, lambda: "Tyler"))

    def test_approval_with_body_runs_without_counting_comments(self):
        self.assertIsNone(skip_reason("approved", "nit", fail, lambda: "Tyler"))

    def test_non_approval_does_not_count_comments(self):
        self.assertIsNone(
            skip_reason("changes_requested", "", fail, lambda: "Tyler")
        )

    def test_claude_commit_is_skipped(self):
        self.assertEqual(
            skip_reason("commented", "fix", fail, lambda: "claude[bot]"),
            "reviewed commit is Claude's",
        )


class MainTest(unittest.TestCase):
    def setUp(self):
        fd, self.output = tempfile.mkstemp()
        os.close(fd)
        self.addCleanup(os.remove, self.output)
        self.env = {
            "REPO": "o/r",
            "PR": "7",
            "REVIEW_ID": "99",
            "REVIEW_STATE": "commented",
            "REVIEW_BODY": "please fix",
            "COMMIT": "abc",
            "GITHUB_OUTPUT": self.output,
        }
        self.calls = []

    def api(self, responses):
        def call(path, jq):
            self.calls.append((path, jq))
            return responses[path]

        return call

    def written(self):
        with open(self.output) as f:
            return f.read()

    def test_writes_skip_false_for_human_commit(self):
        main(self.env, self.api({"repos/o/r/commits/abc": "Tyler"}))
        self.assertEqual(self.written(), "skip=false\n")
        self.assertEqual(self.calls, [("repos/o/r/commits/abc", ".commit.author.name")])

    def test_writes_skip_true_for_claude_commit(self):
        main(self.env, self.api({"repos/o/r/commits/abc": "claude[bot]"}))
        self.assertEqual(self.written(), "skip=true\n")

    def test_counts_review_comments_for_empty_approval(self):
        self.env.update(REVIEW_STATE="approved", REVIEW_BODY="")
        main(self.env, self.api({"repos/o/r/pulls/7/reviews/99/comments": "0"}))
        self.assertEqual(self.written(), "skip=true\n")

    def test_missing_body_counts_as_empty(self):
        self.env.update(REVIEW_STATE="approved")
        del self.env["REVIEW_BODY"]
        main(self.env, self.api({"repos/o/r/pulls/7/reviews/99/comments": "0"}))
        self.assertEqual(self.written(), "skip=true\n")

    def test_api_failure_raises_instead_of_running(self):
        def broken(path, jq):
            raise subprocess.CalledProcessError(1, ["gh", "api", path])

        with self.assertRaises(subprocess.CalledProcessError):
            main(self.env, broken)
        self.assertEqual(self.written(), "")


if __name__ == "__main__":
    unittest.main()
