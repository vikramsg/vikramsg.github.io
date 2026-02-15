---
layout: single
title: "An introduction to React/Next from a backend engineer"
date: 2026-02-15
---

I am not completely new to React.
A couple of years ago I spent a few weeks struggling with frontend tools to create [49travel](https://49travel.vercel.app).
I learnt a lot about tooling, especially Vercel, a little bit about React but I can hardly say I really understood it.
Now its part of my job, so I do want to undestand it better.
And what better way to understand it then by trying to write a blog post about it.

A side note about that last statement.
I often have vague understanding about various concepts that I gather from various sources I skim or read.
But often there are gaps in my understanding.
However, when I write as if I am introducing a concept to an audience (real or virtual), I have to conretize these vague concepts.
And in doing so, I realize gaps in my understanding which I then research and fill.
And hopefully in the process be a useful introduction to others on the internet.
Now let's start.

In the beginning, there was HTML.
You went to a website in your browser, entered a URL, and the browser would do a server request.
The server would send back some HTML, and the job of the browser was to accurately render the HTML.
But that was nostly it.
The browser's main job was to be a rendered and send whatever interactive requests you made to the server.

And then came Javascript.
Javascript allowed the browser to not just be a renderer + HTTP client, but also a runtime.
The server could send back HTML + Javascript, and in interacting with the site you could be interacting with HTML.
Or you could be interacting with Javascript which could be doing things that programming languages do, like do calculations etc.
This allowed even more interactvity.
You could click a button and it could increment a counter!
Among other things.

And then came React. 
(I know, I know, that is a really bad chronology but I am not a historian so I will do my version!)
React flipped the model completely using Javascript.
As against the server deciding completely what would show up on the browser,
now the website became completely client side.
In other words it was an app now!
When you visited a website that was React based,
the server would send a thin HTML but heavy Javascript bundle.
Once you had completely downloaded it (completely unaware of course),
the entire site could in theory never interact with the server again.
Your site was now more or less like an app installed on your machine
doing some computations, rendering etc using browser API's.

But people had issues with this model. The so called `Single Page App` (SPA) model.
React has some batteries but not enough so one usually introduces a lot of dependencies which directly affects bundle size. 
As apps became more sophisticated, bundle sizes ballooned, and so load times increased.
Many were also very nostalgic for the old simpler server first approach. 
And meantime Typescript was exploding in popularity because the developer experience is nicer with a types first approach.
This lead to the creation of Next.
It was the answer to the question, what if we could create a server first React framework but compeltely in React so that developers could build entire apps without changing language or git repo.

Next has an opinionated way of how you structure apps.
One can have some functionality that us pure React, that is, client side.
But its server first meaning if you lean into the Next way of thinking,
when you open a url in the browser, Next renders on the server and sends the appropriate HTML + Javascript back.
Therefore bundle sizes are smaller and time to first load can be much faster.
(But remember that if you mark some files as `use client` they increase bundle sizes, 
even though Next will still decide how much to render on the server vs what executes on the client.)

But Next brings React's unopinionated nature to the server.
One can define API's in Next but its not very elegant and often can require a lot of boilerplate.
And the middleware/proxy thing is really confusing.
People have resorted to various ways to make this easier.
One popular way is to use [`tRPC`](https://trpc.io/) where you write backend code and call it from your frontend
and `tRPC` handles most of the wiring and boilerplate.
But it does not help if you need to build API's.
The most elegant solution that I have found to address this is to use [`Hono`](https://hono.dev/).
It is not a full blown server like Express but is still plenty powerful.
It can sit on top of Next and can be used to build API's while also having an RPC like interface similar to `tRPC`.
And you know for sure that any code running inside `Hono` is running on the server, including the middleware!




























