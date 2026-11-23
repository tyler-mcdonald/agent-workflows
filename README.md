# Agent Workflows

Reusable workflows to run agents in GitHub Actions. 

## handle-review

Tag `@claude` on PR comments, review summaries, or inline review comments to run the [`handle-pr-review`](https://github.com/tyler-mcdonald/skills/tree/main/handle-pr-review) agent skill. 

### How to use this workflow

Set the `CLAUDE_CODE_OAUTH_TOKEN` in your repository
```bash
gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo <owner>/<repo>
```

Add this to the calling repo at `.github/workflows/handle-review.yml`
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
    secrets:
      CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

### Optional settings

Pass inputs under `with:` and secrets under `secrets:`.

| Name | Kind | Default | Description |
| --- | --- | --- | --- |
| `model` | input | `claude-opus-5-5` | Model the agent runs on |
| `agent_instructions_repo` | input | none | Repo (`owner/name`) to load user-level agent instructions from, like a global `CLAUDE.md` |
| `agent_instructions_path` | input | `claude/CLAUDE.md` | Path of the instructions file in `agent_instructions_repo` |
| `AGENT_INSTRUCTIONS_REPO_TOKEN` | secret | `github.token` | Token with read access to `agent_instructions_repo`, if it's private |
