# agent-workflows

Reusable workflows that run a coding agent on PRs. Claude only, for now.

## handle-review

Comment `@claude <anything>` on a PR (repo owner only) to run [`handle-pr-review`](https://github.com/tyler-mcdonald/skills/tree/main/handle-pr-review) on its open review threads. One run per PR at a time.

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
    secrets:
      CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

Optional input `extra_allowed_tools`: extra tools to allow, e.g. `Bash(make:*)`.
