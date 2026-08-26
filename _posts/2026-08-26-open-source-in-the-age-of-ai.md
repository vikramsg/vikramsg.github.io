---
layout: single
title: "Open Source in the age of AI"
date: 2026-08-26
---

If I go through the halls of X, I would probably come back with a very confused opinion on the state of open source today.
On the one hand there are examples like [`opencode`](https://github.com/anomalyco/opencode/pulls) with tons and tons of open PRs with seemingly no moderation mechanism.
On the other hand there is [`ghostty`](https://github.com/ghostty-org/ghostty/blob/main/CONTRIBUTING.md) which has introduced a [`Vouch`](https://github.com/ghostty-org/ghostty/pull/10559) system meaning only approved contributors can submit PRs.
But overall the feeling I get is that maintainers on popular open source projects are overwhelmed with PRs.
And the worst offenders among these PRs are usually purely agent-written code.

I would assume that way more repositories are also being created, mostly via pure agent driven code.
Github [incidents](https://github.blog/news-insights/company-news/the-august-17-outage-and-the-work-ahead/) is obvious evidence.
So the obvious first conclusion that many people seem to have come to is `Open source is dead`.
First because new contributions are being cut off from popular projects.
And second because in a flood of new repos how would one find new projects?

But what is happening is different and I am going to divide my observations into 2 themes that I am thinking about. 

### Taste

First, taste.
It's a trending theme among on X. There are strong opinions being shared on what the most important characteristics required in engineers are right now.
In fact, some claim it may be the only remaining characteristic required - [Citation](https://x.com/Saboo_Shubham_/status/2024173597443707149)
And I agree to an extent because I am seeing some projects coming up where the main distinguishing element is probably taste.

Some examples of projects I have started to use are [`opencode`](https://github.com/anomalyco/opencode) and [`herdr`](https://github.com/herdrdev/herdr).
I am not sure how much taste was part of my choice for `opencode` but the look of `opencode` matching my `neovim` setup was certainly a nudging factor!
As for `herdr` I am a long time user of `tmux`.
And `tmux` is very much from the `neovim` school.
Meaning, lots of config tinkering, plugins, subtle bugs etc.
And like `neovim` I have always wished for something where I just got on with doing stuff rather than fixing it, hence my on and off relationship with `Zed`!
So when I started using `herdr` it felt like someone had listened to my inner thoughts.
Lots of very opinionated takes on how a multiplexer should work.
For example, having an indicator in tabs showing if I am in a zoomed pane (I had to configure tmux to do this).
Or just having a single config line to pick my theme (I had to install a plugin in tmux and to install a plugin in tmux I first need to install a plugin manager).
So, basically taste.
And I did not even talk about how good the agent integration is with `herdr` because that's an evolving area overall.
But the rest was something that `tmux` itself could have done. But chose not to.

### Craft

Which brings me to my second theme.
I am fairly certain that taste will increasingly determine how more projects will rise to the top of the pile of popular open source projects.
Rehashing existing concepts won't cut it since it's so easy to copy using agents now.
However the thing that will start to cause issues in sustaining popularity is how good the engineering in the project is.
I am already starting to see projects starting to see a lot of pressure in sustaining features.
[`opencode`](https://opencode.ai/v2/docs/migrate-v1) and [`pi`](https://github.com/earendil-works/pi), 2 very popular open source harnesses are going through a v1 to v2 transition.
`opencode` V1 had started to become really painful for me to use and while `v2` is certainly way better, I don't yet know how good it is to sustain whatever new directions the project wants to go in.

Another popular open source project that I used to hear more about but much less so these days is [`cmux`](https://github.com/manaflow-ai/cmux).
Which is on [`0.64.x`](https://github.com/manaflow-ai/cmux/releases) since May and I believe is also trying to create a `v2`.
And I have been seeing [issues with `herdr`](https://github.com/herdrdev/herdr/issues/3018) when it comes to seeing images using the `kitty` protocol.
I don't want to make it feel like I am throwing these projects under the bus because both `cmux` and `herdr` are really good.
But I also feel like a lot of these projects will suffer from 2 things.

1. Needing to create unrelated primitives, meaning a lot of project time is spent not on core areas but on a necessary abstraction (or abstractions) that enables the product.
2. How much the maintainers are going to lean on agents.

[`openclaw`](https://github.com/openclaw/openclaw) is a big example of 1. It started off as a very, very popular project but it suffered from needing to create so many primitives.
An example of a question it needed to answer was how an agent accesses email without doing [destructive operations](https://docs.openclaw.ai/gateway/security), which is important but not really a responsibility that `openclaw` should be handling.
As for 2, I am not going to cite any examples since I am not privy to how maintainers are working with agents,
but a lot of open source projects seem to be relying heavily on AI.
My current belief is, the heavier agents are relied on, the more complicated the architecture becomes and the harder it will be to evolve in the future.
And depending on the volume of code that agents create, that future could come in weeks, rather than years.

## It's still going to be exciting

Having said all that I am still really excited about what is coming.
After all 6 months ago, I had not used `opencode`. But right now it feels like most of my day is spent interacting with it.
2 weeks ago, I had not used `herdr`. Now it's a core part of my daily workflow.
So, I am rooting for more such projects succeeding.
And hopefully there's enough Taste and Craft in them to make sure they become sustainable projects.

## Disclaimer

The entire post was hand-written (shocking!) by me (in `NeoVim` inside `herdr`). However I used GPT5.6 Sol to research all citations and put them in the slots I put in the post.
