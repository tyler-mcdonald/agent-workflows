# Agent Workflows

Reusable workflows to run agents in GitHub Actions. 

## handle-review

Tag `@claude` on PR comments, review summaries, or inline review comments to run the [`handle-pr-review`](https://github.com/tyler-mcdonald/skills/tree/main/handle-pr-review) agent skill. Anything after `@claude` is passed to the agent as instructions. The agent cannot change files under `.github/workflows/`.

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
    # with:
    #   model: "<model id>"  # model the agent runs on (see workflow file for defaults)
    secrets:
      CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }} # set this in the calling repo
```
