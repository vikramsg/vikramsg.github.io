---
layout: single
title: "Adjusting to Sol"
date: 2026-08-16
---

I have been working only with GPT models since about January.
I actually made the choice because of subscriptions available at day job, so not necessarily a 1-1 comparison before deciding.

However, I have been changing my approach so much over the past few months that I wanted to record it just so that I do not forget this point of time.
The reason that actually compelled me to think about writing was because Adjusting from 5.5 to 5.6 Sol has been a much bigger jump that any adjustments I had to do through 5.3 (when it was called Codex), 5.4 or 5.5.
In other words all models through 5.3, 5.4, 5.5 were more or less in terms of configuration.

## Initial days with pre Sol models

Sometime in August/September 2025 we were building document extraction AI Agents at Day job.
We were working with mostly OpenAI models and sometimes experimenting with Gemini.
Claude was reserved mostly for coding because our initial tests with Claude showed it hallucinated quite a bit. 
We worked by building basically a `DAG` by making the agent doing very specific steps one after the other since they weren't very reliable on somewhat open ended tasks.
However, then `GPT O4` came out.
Which was the first time I felt a step change in what kind of things we could build AI agents for.
We collapsed most of our custom `DAG` and just let `O4` do the entire thing via 1 prompt.
However this entire exercise was not about coding agents.
I was still mostly using Cursor with auto complete.
And trying to make Claude Code do small things.
Then Opus 4.5 came out and it was a phase shift moment.

### Opus 4.5

Suddenly Cursor seemed too limited.
We started to see that a lot of code could be written by just using English.
And Claude Code became what I spent more time in, rather than Cursor. 
However, with time what I also noticed that Opus would often take decisions I did not ask it to and which required a lot of fixing.
In addition, I was a bit frustrated by Claude Code issues like flickering, but more importanly the lock in wherein I could not try other models.
And sometimes I would think of my initial experience with O4, on how well it followed instructions.

### OpenCode

Around January, I decided to do more experimentation.
I started using OpenCode on and off.
Initially I even tried Gemini a lot because we had started using it for some document extraction work and I wanted to try how well it worked as an agent.
In doing so I became the Gemini guy at my company, almost pushing people to try it out.
But it was always frustrating.
Gemini was amazing at very specific things.
It was great in the Gemini app at coming up with some frontend stuff.
It was great at debugging Terraform issues with GCP.
And it was pretty good at doing code reviews.
But it was never very agentic.
I had to almost push it to do simple things which needed no extra instructions with Claude Code.
I also used to go back and forth between the Gemini CLI and OpenCode thinking it maybe a harness issue.
Turns out Gemini behaved better in OpenCode, but it was never really good enough.

### GPT 5.3 Codex

Frustrated with lack of development

## Notes

1 year ago I was all in into [devcontainers](https://github.com/vikramsg/Experiments/pull/19/changes) because I did not trust coding agents would not just delete stuff wholesale.

## ToDo - Research

1. Dates when Sol was released
2. Date when I changed my OpenCode setup
3. All OpenCode setup changes I have done since Sol

## Sol

1. Doesn't understand `gh stack` so always need to remind.
2. Too happy to invoke subagents
3. I need to create commands that do not invoke subagents
4. We need a build prompt that has sections about invoking subagents that have the same lessons as our orchestrator
  - Provide full context to implementation agent, especially if any decisions have already been made.
  - Ask it to provide all decisions that it did during implementation not already decided 
5. Need more control
  - Planner should be smaller and always instruction to add implementation notes.md 
6. docs, tickets everything leans how not what. Do not write a plan in a doc unless its specifically a plan

