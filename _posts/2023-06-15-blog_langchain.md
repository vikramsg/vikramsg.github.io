---
layout: single
title:  "Comparing GPT with Open Source LLM's"
date:   2023-06-15
---

Last [week]((../blog_49travel/) I talked about how I created [49travel](https://49travel.vercel.app/). 
I went over broadly on what were the various ingredients and so glossed over many details.
This week I want to talk about one particular aspect which was pretty interesting
and for me a nice introduction to the various projects that are being furiously worked on
since the entry of ChatGPT. 

## The problem

As I mentioned

## Enter gpt-3.5-turbo

I now had a trip API and all cities worth visiting in Germany. 
But what do I put on the website?
My initial idea was that I would put the list of cities,
sorted by journey time and a short touristy description for the city.
But where do I get the description?
Initially I thought I would just scrape WikiVoyage.
But the text was very unstructured and I get very weird output.
The solution, and it took some time for me to figure this out,
was to actually use `gpt-3.5-turbo` to summarize the pages. 
I will write another post about that since I had to do quite a bit of experimentation for that.
That was the only part that cost money. A whopping $4 for summarizing ALL cities
in Germany on Wikivoyage!

## Final thoughts

## Code

The code is available [here](https://github.com/vikramsg/blog_code/blob/main/langchain_summarizer/src/summarize.py). 
`gpt-3.5-turbo` and `pythia` are fairly easy to use since they are both API's but `gpt4all` requires some setup work. 
This is explained in the README file.


