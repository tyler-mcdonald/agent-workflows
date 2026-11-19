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
    # with:
    #   model: "<model id>"  # model the agent runs on (see workflow file for defaults)
    #   agent_instructions_repo: "<owner>/<repo>"  # load user-level agent instructions (like a global CLAUDE.md) from this repo
    #   agent_instructions_path: "claude/CLAUDE.md"  # path of the instructions file in that repo
    secrets:
      CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
      # AGENT_INSTRUCTIONS_TOKEN: ${{ secrets.AGENT_INSTRUCTIONS_TOKEN }}  # read access to agent_instructions_repo, if private
```
