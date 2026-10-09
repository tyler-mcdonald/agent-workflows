# agent-workflows

Reusable workflows that run a coding agent on PRs.

## handle-review

Comment `@claude <anything>` on a PR (repo owner only) to run [`handle-pr-review`](https://github.com/tyler-mcdonald/skills/tree/main/handle-pr-review) on its open review threads. One run per PR at a time.

To use it, add this to the calling repo as `.github/workflows/handle-review.yml` and set the `CLAUDE_CODE_OAUTH_TOKEN` secret:

```yaml
name: Handle review

on:
  issue_comment:
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

Only Claude is supported for now.
