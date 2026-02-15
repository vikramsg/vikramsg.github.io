---
layout: single
title: "A Backend Engineer's Guide to Understanding React and Next.js"
date: 2026-02-15
---

{% include mermaid.html %}

I am not completely new to React.
A couple of years ago I spent a few weeks struggling with frontend tools to create [49travel](https://49travel.vercel.app).
I learnt a lot about tooling, especially Vercel, a little bit about React but I can hardly say I really understood it.
Now it is part of my job, so I do want to understand it better.
And what better way to understand it than by trying to write a blog post about it.

A side note about that last statement.
I often have vague understanding about various concepts that I gather from various sources I skim or read.
But often there are gaps in my understanding.
However, when I write as if I am introducing a concept to an audience (real or virtual), I have to concretize these vague concepts.
And in doing so, I realize gaps in my understanding which I then research and fill.
And hopefully in the process be a useful introduction to others on the internet.
Now let's start.

In the beginning, there was HTML.
You went to a website in your browser, entered a URL, and the browser would do a server request.
The server would send back some HTML, and the job of the browser was to accurately render the HTML.
But that was mostly it.
The browser's main job was to be a renderer and send whatever interactive requests you made to the server.

<div class="mermaid">
sequenceDiagram
    participant User
    participant Browser
    participant Server

    User->>Browser: Enter URL
    Browser->>Server: GET /index.html
    Server-->>Browser: HTML (Full Page)
    Browser-->>User: Render Page
    User->>Browser: Click Link
    Browser->>Server: GET /about.html
    Server-->>Browser: HTML (Full Page)
    Browser-->>User: Render New Page
</div>

And then came Javascript.
Javascript allowed the browser to not just be a renderer + HTTP client, but also a runtime.
The server could send back HTML + Javascript, and in interacting with the site you could be interacting with HTML.
Or you could be interacting with Javascript which could be doing things that programming languages do, like do calculations etc.
This allowed even more interactivity.
You could click a button and it could increment a counter!
Among other things.

And then came React. 
(I know, I know, that is a really bad chronology but I am not a historian so I will do my version!)
React flipped the model to be more Javascript heavy.
As against the server deciding completely what would show up on the browser,
now it became common for websites to become completely client side.
In other words it was an app now!
When you visited a website that was React based,
the server would send a thin HTML but heavy Javascript bundle.
Once you had completely downloaded it (completely unaware of course),
the entire site could in theory never interact with the server again.
Your site was now more or less like an app installed on your machine
doing some computations, rendering etc using browser APIs.

<div class="mermaid">
sequenceDiagram
    participant User
    participant Browser
    participant Server

    User->>Browser: Enter URL
    Browser->>Server: GET /index.html
    Server-->>Browser: HTML (Empty Div) + bundle.js
    Browser->>Browser: Execute JS (React)
    Browser->>Server: GET /api/data (JSON)
    Server-->>Browser: { "data": ... }
    Browser-->>User: Render Content
    User->>Browser: Click Link
    Browser->>Browser: Update DOM (Client-side Routing)
    Note over Browser, Server: No page reload!
</div>

But people had issues with this model. The so called `Single Page App` (SPA) model.
React is famously unopinionated and so one usually introduces a lot of dependencies which directly affects bundle size. 
As apps became more sophisticated, bundle sizes ballooned, and so load times increased.
Many were also very nostalgic for the old simpler server first approach. 
And meantime Typescript was exploding in popularity because the developer experience is nicer with a types first approach.
This coincided with the creation of Next.
It was the answer to the question, what if we could create a server first React framework but completely in React so that developers could build entire apps without changing language or git repo.

Next has an opinionated way of how you structure apps.
One can have some functionality that is pure React, that is, client side.
But it is server first meaning if you lean into the Next way of thinking,
when you open a url in the browser, Next renders on the server and sends the appropriate HTML + Javascript back.
Therefore bundle sizes are smaller and time to first load can be much faster.

<div class="mermaid">
sequenceDiagram
    participant User
    participant Browser
    participant Server

    User->>Browser: Enter URL
    Browser->>Server: GET /index.html
    Note over Server: Server renders React to HTML
    Server-->>Browser: HTML (Pre-rendered Content) + RSC Payload
    Browser-->>User: Show Content
    Browser->>Browser: Hydrate (Make Interactive)
    User->>Browser: Click Link
    Browser->>Browser: Client-side Navigation (like SPA)
    Browser->>Server: GET /new-page (RSC Payload)
    Server-->>Browser: RSC Payload (Streaming)
    Browser->>Browser: Reconcile React Tree
</div>

But building APIs in Next can be inelegant.
One can define APIs in Next but it can require quite some boilerplate to wire up correctly to the frontend.
And the middleware/proxy thing is really confusing.
People have resorted to various ways to make this easier.
One popular way is to use [`tRPC`](https://trpc.io/) where you write backend code and call it from your frontend
and `tRPC` handles most of the wiring and boilerplate.
But it does not help if you need to build REST/HTTP APIs.
The most elegant solution that I have found to address this is to use [`Hono`](https://hono.dev/).
It is not a full blown server like Express but is still plenty powerful.
It can sit on top of Next and can be used to build APIs while also having an RPC like interface similar to `tRPC`.
And you know for sure that any code running inside `Hono` is running on the server, including the middleware!

And that is where we will stop for today.
This was definitely a highly compressed take on React and Next.
I am sure that there were many technical nuances I completely glossed over
but my objective was to create a good mental model of the frontend world as I see it.

## Disclaimer

The blog post was completely written by a human, me!
The diagrams were completely created by an LLM, Gemini (using Gemini 3 Pro Preview in the Gemini CLI)!

## Notes

- In Next if you mark some files as `use client` they increase bundle sizes, 
even though Next will still decide how much to render on the server vs what executes on the client.
- RSC stands for React Server Components which has more technical nuance but probably a subject for another blog post. Note also that Next has a Pages router which I have completely skipped over.


