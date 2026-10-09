# agent-workflows

Reusable GitHub Actions workflows that run a coding agent on pull requests. Only Claude is supported for now.

## handle-review

Runs the [`handle-pr-review`](https://github.com/tyler-mcdonald/skills/tree/main/handle-pr-review) skill when a review is submitted on a PR, so the agent addresses the review's threads, commits by concern, and pushes. The repo's own CI runs on that push.

It only runs when:

- the reviewer is the repo owner or `coderabbitai[bot]`,
- the PR isn't a draft,
- the review isn't an approval with no body and no comments,
- the reviewed commit wasn't authored by `claude[bot]` (one agent round per push).

Runs are queued per PR (`agent-pr-<number>`), capped at 30 minutes and 60 turns.

### Usage

Add `.github/workflows/handle-review.yml` to the calling repo and set the `CLAUDE_CODE_OAUTH_TOKEN` secret:

```yaml
name: Handle review

on:
  pull_request_review:
    types: [submitted]

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
