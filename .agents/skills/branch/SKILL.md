---
name: branch
description: Commit, push, and publish with /branch merge, or just commit and push with /branch commit.
disable-model-invocation: true
---

# Blog workflow

Invocation arguments: `$ARGUMENTS`

The first argument must be `commit` or `merge`. If it is missing or unknown, reply with `Usage: /branch {commit|merge} [notes]` and do not run any commands. Treat any remaining text as notes for the selected action. Both actions require a checked-out branch other than `main`.

## Commit and push (both actions)

1. Review the working tree and the changes already on the branch. Commit only the finished work the user wants included. Leave unrelated changes and unpublished drafts untouched, even if already staged. Do not make an empty commit.
2. Push the current branch to `origin` if it has unpublished work to push, setting its upstream if needed. Check what will be pushed first: stop if it includes work the user wants excluded or if the remote branch is ahead or has diverged. Do not force-push.
3. If the action is `commit`, report the result and stop. Do not open or merge a pull request, deploy, or switch branches. If the action is `merge`, continue directly; the user does not need to invoke `/branch commit` first.

## Merge and deploy (`/branch merge` only)

1. Verify the current commit matches the branch on `origin`. If there are no changes to merge into `main`, report that and stop. Unrelated local changes that were left out of the commit do not block the PR.
2. Merge the pushed branch into `main`. Use its pull request targeting `main` if one exists, or open one if needed. Make sure the pull request is still at the verified commit before merging. Do not bypass required checks.
3. Fetch `origin` and fast-forward local `main` to `origin/main` without discarding local commits or changes. Refresh `main` before waiting on deployment so it stays current even if the deploy fails.
4. Monitor the `Deploy Hugo site to Pages` workflow for the commit that landed on `main`, not a run from the snack branch or an older deployment.
5. Only after a successful deploy, switch this worktree to a new branch from `origin/main`. Use the next unused `b<number>` name (for example, `b6` after `b5`), checking both local and remote branches. Use a normal, non-forced switch so unrelated local changes are preserved. If Git refuses the switch because of local changes, report that and leave them untouched.

If any step fails or is blocked, report what happened and stop. Do not switch to a new branch after a failed or unverified deployment.
