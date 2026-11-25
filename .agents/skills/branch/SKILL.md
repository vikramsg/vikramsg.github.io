---
name: branch
description: Commit and push a snack with /branch commit, or publish a pushed branch with /branch merge.
disable-model-invocation: true
---

# Blog workflow

Invocation arguments: `$ARGUMENTS`

The first argument must be `commit` or `merge`. If it is missing or unknown, reply with `Usage: /branch {commit|merge} [notes]` and do not run any commands. Treat any remaining text as notes for the selected action. Both actions require a checked-out branch other than `main`.

## `/branch commit [notes]`

1. Review the changes and commit only the finished snack. Leave unrelated changes out of the commit, even if they are already staged. If there are no relevant changes, do not make an empty commit; push only if the branch has unpublished commits. Otherwise, report there is nothing to commit or push.
2. Push the current branch to `origin`, setting its upstream if needed. Do not force-push. Report the commit and branch, then stop. Do not open or merge a pull request, deploy, or switch branches.

## `/branch merge [notes]`

1. Check that the worktree is clean and the current commit matches the current branch on `origin`. If there are uncommitted changes or unpublished local commits, stop and tell the user to run `/branch commit` for the snack or put unrelated work aside. If the remote is ahead or has diverged, report that and stop. Do not commit or push as part of merge. If the branch has no changes to merge, report that and stop.
2. Merge the pushed branch into `main`. Use its pull request targeting `main` if one exists, or open one if needed. Make sure the pull request is still at the verified commit before merging. Do not bypass required checks.
3. Fetch `origin` and fast-forward local `main` to `origin/main` without discarding local commits or changes. Refresh `main` before waiting on deployment so it stays current even if the deploy fails.
4. Monitor the `Deploy Hugo site to Pages` workflow for the commit that landed on `main`, not a run from the snack branch or an older deployment.
5. Only after a successful deploy, switch this worktree to a new branch from `origin/main`. Use the next unused `b<number>` name (for example, `b6` after `b5`), checking both local and remote branches.

If any step fails or is blocked, report what happened and stop. Do not switch to a new branch after a failed or unverified deployment.
