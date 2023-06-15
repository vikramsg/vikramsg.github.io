---
layout: single
title:  "Comparing GPT with Open Source LLM's"
date:   2023-06-15
---

Last [week](../blog_49travel/) I talked about how I created [49travel](https://49travel.vercel.app/). 
I went over broadly on the ingredients and often glossed over many details.
This week I want to talk about one particular aspect which was pretty interesting for me.
It was a nice introduction to the various projects going on in the LLM world that are being furiously worked on
since the entry of ChatGPT. 

## The problem

As I mentioned in the last post, the reason I wanted to use an LLM was to produce a short summary of the WikiVoyage
page so that a visitor to the page could get a nice overview. 
I originally tried to do this by simply trying to extract the list of places to see and things to do using
some ill-formed Regex, but it was soon obvious that this would require a lot of effort.
Not all Wikivoyage pages follow the same format and some listings can have really strange formatting. 
I then thought that an LLM could be a good candidate to solve this problem. 
What if we simply give it the page, and it summarizes the page for us? 
But how do I go about doing this? 


## Langchain 

The idea to use Langchain came to me while I was attending a [Machine Minds Hackathon](https://www.meetup.com/machine-minds-hamburg/events/293740181/). 
Sebastian was kind enough to show me what he had been doing using `gpt` on Discord for summarizing and so I thought this would be the right time
to dive into [langchain](https://github.com/hwchase17/langchain). 
But there was a catch. One of the constraints that I had put on myself while developing [49travel](https://49travel.vercel.app/) was to use 
only free stuff. There was no specific reason for this except for me to find out if this was even possible. 
`gpt` is of course not free. So what do I do?

There was another development in LLM that I had been following. 
This was the [open-assistant](https://open-assistant.io/) project. This was trying to recreate the ChatGPT training process but with open models. 
They actually already had a model up and running, but there was a problem. This was using LLAMA, and I didn't want to touch
it with all its licensing issues. But they had also done the same with a different model, which was the [Pythia](https://github.com/EleutherAI/pythia) model
with 12 Billion parameters. 
But how do I run this? I don't have a GPU lying around. Turns out there's an easier way to do this. 
[HuggingFace](https://huggingface.co/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5) provides a Hosted Inference API with rate limits, 
with which you can run models of reasonable size but with rate limits. 


## Making it work 

The way the [summarization](https://python.langchain.com/en/latest/modules/chains/index_examples/summarize.html) works is that bigger documents
are split up into smaller documents, then each chunk is summarized and finally they are all combined and then the combined text is summarized. 
This in a way is `MapReduce` and that is exactly what the `langchain` API calls it.  

```python
chain = load_summarize_chain(
    llm, chain_type="map_reduce", combine_prompt=combine_prompt
)
```

However, at this point I hit a hitch. `langchain` has inbuilt functions for `gpt` as well as other models that are loaded locally. 
But I couldn't quite figure out how to use it for an API that was not `gpt`. 
So, I did the most obvious thing, and built a simple `MapReduce` loop. 
I get the WikiVoyage text, break it up into chunks, summarize each one using the API and then combine the summaries and then use
the API again to summarize it. 

## GPT4ALL

I also wanted to test out [gpt4all-groovy](https://github.com/nomic-ai/gpt4all) since it was supposed to be small enough to run locally. 
No API calls required! But that was a bit of a pain.
It has an installer, but it did not support my older MacOS. So I installed it from source, which was in fact not so painful, 
but there were multiple steps. Then there were some `pip` installs required and so I had to mix `poetry` with `pip`. 
Finally, it did work though, which was a win.
So, what were the results? 


## Summaries

The first thing I noticed was that prompting the `Pythia` model was a bit of a pain. At the [Hackathon](https://www.meetup.com/machine-minds-hamburg/events/293740181/),
we discussed some possible prompts, and initially it seemed to work. 
But I realized when trying to do multiple WikiVoyage pages that it was very unpredictable. 
Sometimes, it would produce very nice summaries. Other times, it wouldn't produce anything at all.
And sometimes it would spit out complete nonsense.

`gpt4all` is fairly slow, but in my experience, fairly consistent. However, it is more or less impossible to steer. 
It spits out whatever it wants to spit out and nothing else!
Of course, as you know, at the end I gave up and just used `gpt-3.5-turbo`. That turned out to cost about $4
and it was incredibly reliable and required very little prompt tuning. 
On the other hand, as some of you may have noticed, it likes the word `charming` a bit too much when describing touristy places. 

I have created a [comparison](https://github.com/vikramsg/blog_code/blob/main/langchain_summarizer/summaries.md) 
of summaries for the WikiVoyage page of [Allgäu](https://en.wikivoyage.org/wiki/Allg%C3%A4u). 
The prompts are all more or less the same. First, I ask it to summarize each chunk using

```
Summarize the following text.
```

Then I combine the resulting summaries, and ask it to use the following prompt to produce an overall summary. 

```
Combine all the summaries on {city} provided within backticks ```{total_summary}```.
Can you summarize it as a tourist destination in 8-10 sentences.
```

Notice how well `gpt` performs. `Pythia` seems to do an ok job, but it completely misses some of the nice places to visit such as Neuschwanstein castle. 
And it does not really stick to `8-10` sentences. `gpt4all` is very formal and answers like its a college exam question! 


## Final thoughts

I think this was an interesting exercise to do, just to find out what the state of the art is. 
The first thing I learnt was that `langchain` is incredibly useful. Summarization is just one
of its many intended usecases. I need to explore more. 
Using `Pythia` was interesting. First, I learnt of the hosted inference API, which seems very useful
for just testing out models that you don't want to self-host without having a go. 
HuggingFace seem to be doing a very nice job. 
Don't expect to use the free API in production though. The rate limits kick in very quickly. 
`gpt4all` seems more like a toy. But the very fact that it even runs on my CPU only system is remarkable. 
Of course, `gpt` just works. But I look forward to other models atleast try to catch up. 


## Code

The code is available [here](https://github.com/vikramsg/blog_code/blob/main/langchain_summarizer/src/summarize.py). 
`gpt-3.5-turbo` and `pythia` are fairly easy to use since they are both API's but `gpt4all` requires some setup work. 
This is explained in the README file.


