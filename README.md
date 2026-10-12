# agent-workflows

Reusable workflows to run coding agents.

## handle-review

Start a PR comment, review, or inline review comment with `@claude` to run [`handle-pr-review`](https://github.com/tyler-mcdonald/skills/tree/main/handle-pr-review) on open review threads.

To use it, add this to the calling repo at `.github/workflows/handle-review.yml` and set the `CLAUDE_CODE_OAUTH_TOKEN` secret:

```yaml
name: Handle review

on:
  issue_comment:
    types: [created]
  pull_request_review:
    types: [submitted]
  pull_request_review_comment:
    types: [created]

jobs:
  handle-review:
    permissions:
      contents: write
      pull-requests: write
      issues: write
      id-token: write
    uses: tyler-mcdonald/agent-workflows/.github/workflows/handle-review.yml@main
    # with:
    #   extra_allowed_tools: "Bash(make:*)"  # extra tools to allow, comma-separated
    secrets:
      CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```
