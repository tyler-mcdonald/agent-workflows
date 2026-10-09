# agent-workflows

Reusable GitHub Actions workflows that run a coding agent on pull requests. Only Claude is supported for now.

## handle-review

Runs the [`handle-pr-review`](https://github.com/tyler-mcdonald/skills/tree/main/handle-pr-review) skill when you tag `@claude` in a PR comment, so the agent addresses the PR's open review threads, commits by concern, and pushes. The repo's own CI runs on that push.

It only runs when the comment is on a PR, starts with `@claude` followed by a space (e.g. `@claude please fix the typo`), and was written by the repo owner. Reviews are never handled automatically.

Runs are queued per PR (`agent-pr-<number>`), capped at 30 minutes and 60 turns.

### Usage

Add `.github/workflows/handle-review.yml` to the calling repo and set the `CLAUDE_CODE_OAUTH_TOKEN` secret:

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

### Inputs

| Input | Default | Description |
| --- | --- | --- |
| `extra_allowed_tools` | `""` | Comma-separated tools to allow on top of the defaults (`gh`, `git`, skill scripts, Read/Edit/Write/Glob/Grep), e.g. `Bash(make:*)`. |
