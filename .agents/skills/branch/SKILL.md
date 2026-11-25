---
name: branch
description: Run the blog workflow with /branch merge to publish a finished snack and monitor deployment.
disable-model-invocation: true
---

# Blog workflow

Invocation arguments: `$ARGUMENTS`

The first argument must be `merge`. If it is missing or unknown, reply with `Usage: /branch merge [notes]` and do not run any commands. Treat any remaining text as notes for the merge workflow.

1. Commit the finished snack and push the current branch to `origin`.
2. Once the branch is ready upstream, merge it into `main`. Use the branch's pull request if one exists, or open one if needed. Do not bypass required checks.
3. Fetch `origin` and fast-forward local `main` to `origin/main` without discarding local commits or changes. Refresh `main` before waiting on deployment so it stays current even if the deploy fails.
4. Monitor the `Deploy Hugo site to Pages` workflow for the commit that landed on `main`, not a run from the snack branch or an older deployment.
5. Only after a successful deploy, switch this worktree to a new branch from `origin/main`. Use the next unused `b<number>` name (for example, `b6` after `b5`), checking both local and remote branches.

If any step fails or is blocked, report what happened and stop. Do not switch to a new branch after a failed or unverified deployment.
