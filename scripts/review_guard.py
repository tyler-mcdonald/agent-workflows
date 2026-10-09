import os
import subprocess

CLAUDE_AUTHOR = "claude[bot]"


def skip_reason(state, body, comment_count, author):
    if state == "approved" and not body.strip() and comment_count() == 0:
        return "empty approval"
    if author() == CLAUDE_AUTHOR:
        return "reviewed commit is Claude's"
    return None


def gh_api(path, jq):
    result = subprocess.run(
        ["gh", "api", path, "--jq", jq],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def main(env=os.environ, api=gh_api):
    repo = env["REPO"]
    reason = skip_reason(
        state=env["REVIEW_STATE"],
        body=env.get("REVIEW_BODY", ""),
        comment_count=lambda: int(
            api(f"repos/{repo}/pulls/{env['PR']}/reviews/{env['REVIEW_ID']}/comments", "length")
        ),
        author=lambda: api(f"repos/{repo}/commits/{env['COMMIT']}", ".commit.author.name"),
    )
    if reason:
        print(f"Skipping: {reason}")
    with open(env["GITHUB_OUTPUT"], "a") as out:
        out.write(f"skip={'true' if reason else 'false'}\n")
    return reason


if __name__ == "__main__":
    main()
