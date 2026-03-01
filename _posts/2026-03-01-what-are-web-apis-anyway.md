---
layout: single
title: "What are Web APIs anyway?"
date: 2026-03-01
---

## Notes

1. Browser as OS/Runtime
2. API's are created in the language the browser is implemented in. C++ for Chrome inside Blink engin.
    - The web api engine and the JS engine (V8) are different.
    - Firefox, the engine is Gecko and parts of it is C++ and parts of it is Rust.
    - On ios, all browsers must call WebKit! - probably focus on this as notes
    - Mobile is complicated. API's often have to call os api's.
3. Notes about WASM but as a side note. Its not quite in place to natively talk to Web APIs. So still Javacsript.
    - Some are called by browser internally when rendering HTML which is declarative.
4. Examples are console.log, dom.something  session storage etc. 
    - Want to talk about websockets but probably too much info.
    - console.log, document.getElementById(), localStorage, and fetch(
5. There are web workers that can be used for offload tasks. Workers `do not` have access to all Web APIs.
    - For example document. etc is not available on worker.
6. Strong sandboxing. Not easy to access files directly from inside Chrome.

## Ref

MDN Web Docs - Introduction to Web APIs:
    *   Link: https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Introduction (https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Introduction)


## Diagrams

1. Engine split between JS and Runtime
2. React fn to web api sequence diagram
    - Note React is staying within V8 somehow?

### Diagram: React to Web API Execution Flow

```mermaid
sequenceDiagram
    autonumber
    
    participant User
    
    box rgb(240, 240, 240) JavaScript Engine (V8/JSC)
        participant App as Your React Code
        participant React as React Core (Reconciler)
        participant ReactDOM as ReactDOM (Renderer)
    end
    
    box rgb(220, 230, 240) Browser Engine (Blink/WebKit)
        participant WebAPI as DOM Web API (C++)
        participant Paint as Rendering Pipeline
    end
    User->>WebAPI: Clicks <button>
    Note over WebAPI: Browser detects hardware interrupt, creates PointerEvent
    WebAPI->>ReactDOM: Dispatches synthetic event (onClick)
    ReactDOM->>App: Calls your handler: setCount(count + 1)
    
    App->>React: Triggers state update
    Note over React: React is pure JS. It compares the old Virtual DOM to the new Virtual DOM (Reconciliation).
    
    React->>ReactDOM: Commits the changes
    Note over ReactDOM: ReactDOM translates the Virtual DOM diff into actual DOM API calls.
    
    ReactDOM->>WebAPI: document.getElementById('counter').textContent = '1'
    Note over WebAPI: JS engine hits WebIDL binding. C++ execution begins. Memory is updated.
    
    WebAPI->>Paint: Trigger Recalculate Style & Layout
    Paint-->>User: Screen updates with new number
```
