---
layout: single
title:  "Comparing GPT with Open Source LLM's"
date:   2023-06-21
---

The last couple of posts have been about [49travel](https://49travel.vercel.app/) and the way I built it.
This week I am going to be talking about decorators for a bit. 
It seems very disconnected from the last posts, but I started reflecting on this
while writing some Python for 49travel. 
So there's still a connection!

## Python requests

As a reminder, to build [49travel](../blog_49travel/), I had to use the amazing [Transport Rest API](https://transport.rest/). 
However, this is obviously not built for production and so does rate limiting. 
Which is fine since we can just add a rate limit on our side by introducing `time.sleep`. 
For eg., this would be one way to do this. 

```python
import requests

def _request():
    location_url = "https://v6.db.transport.rest/locations?query=Hamburg&results=1"
    location_response = requests.get(location_url)
    time.sleep(1)
```

This would ensure that everytime we call `_request`, we would wait 1 second after the `get` request, ensuring less than 60 requests per minute. 
But as I started working with this code, some issues started becoming annoying. 
First I had to introduce a timeout inside the `get` request. 

```
location_response = requests.get(location_url, timeout=1)
```

I really have no explaination for this, but the request would wait infinitely if I did not add this to the request. 
Which is fine, but I kept getting connection errors even after this. 
So I decided to introduce retries into the request session. Pay attention to this because we will get back to this later. 
This is how I add retries.

```python
def session_with_retry() -> requests.Session:
    session = requests.Session()

    retries = 3
    backoff_factor = 0.3

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session
```

In the function, `retries = 3` ensures that if the connection fails, `requests` will try 3 more times.  
The `backoff_factor` ensures that after each failure past the second try, the request waits [exponentially longer](https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html). 

```
{backoff factor} * (2 ** ({number of previous retries}))
```

We edit our previous function to now use the retry strategy. 

```
def _request():
    location_url = "https://v6.db.transport.rest/locations?query=Hamburg&results=1"
    request_session = session_with_retry()
    location_response = request_session.get(location_url, timeout=1)
```

Problem solved, right? Yes, but as you can see, the code isn't very nice. First, the weird `timeout` inside the request, and then the ugly `Retry` code.  


## Pyhafas

While thinking of making this cleaner, I discovered [pyhafas](https://github.com/FahrplanDatenGarten/pyhafas). 
And remarkably, it solved my first problem. I no longer had to use the `_request` function, create query parameters etc. 
Instead of a REST API, I could use the `pyhafas` API!

```python
def _journey():
    client = HafasClient()
    return client.journeys(  # type: ignore
            origin=origin,
            destination=destination,
            date=time_val,
            products={
                "long_distance_express": False,
                "long_distance": False,
                "ferry": False,
                "bus": False,
                "suburban": False,
                "subway": False,
            },
        )
```

But I still had my second problem. A few requests, and I would get Connection Error. And now I did not have direct control
over the Retry strategy. 
So, I decided to create my own!

```python
for i in range(4):
    try:
        journeys =  _journey() 
        return journeys
    except requests.exceptions.ConnectionError as e:
        print(f"Connection reset. Error: {e.args[0]}. Waiting to try again.")
        time.sleep(2 * (i + 1) * 20)
        print("Trying again")
```

Here, the `i` loop is the number of retries and I made my own custom exponential backoff with some tuning. 
It worked. I hated it!


## Tenacity 

I decided that the ideal way forward would be to actually change the code in `pyhafas`. 
But when I started to write the changes, I realized something else. 
The retry code is really ugly. Look at this monstrosity again.
Also notice that we need 3 different imports to implement it. 


```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

retries = 3
backoff_factor = 0.3

retry = Retry(...

adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)
```

At this point I discovered [tenacity](https://tenacity.readthedocs.io/en/latest/) while 
reading through some [OpenAI examples](https://github.com/openai/openai-cookbook/blob/90ef0f25e5615fa2bdd5982d6ce1162f4e3839c6/apps/embeddings-playground/embeddings_playground.py).
And this is so much nicer.


```python
from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_attempt 

@retry(
        wait=wait_exponential(multiplier=tenacity_multiplier),
        stop=stop_after_attempt(tenacity_retry_attempts),
        retry=retry_if_exception_type(requests.ConnectionError),
    )
def journey(...
```

Now I don't have to deal with creating sessions and adapters and all that jazz anymore.
The imports are all together on a single line.
And this is in fact even more general. It doesn't necessarily apply to only connection errors.
That's just the choice I want to make here.
Plus, you control the retries explicity rather than through indirections. 


## Composability using decorators

Going through this exercise really highlighted to me how powerful decorators are. 
There are many examples of how they are being used in a similar manner. 
Consider Airflow. 

```python
from airflow.decorators import dag, task

@dag
def my_dag():
    @task
    def task1():
        # Task 1 logic goes here

    @task
    def task2():
        # Task 2 logic goes here
```

This is such a nice way of defining the DAG. 
You just write the functions for a task and wrap it with a decorator and it becomes a DAG(of course you also need to define inter task dependencies). 

Or Numba, which we touched upon in a [previous post](../blog_numba_slower_than_pandas/). 

```python
from numba import njit

@njit
def plus_one(a):
    return a+1
```

I think this is a template that should be followed to make Python libraries more composable, as opposed to the boilerplate we needed to do for Retry.


## Final thoughts

This post became longer than I had originally thought, but I figured out that these are the steps I went through to make this realization. 
Library design is not easy, but recognizing these patterns will lead to better designs. 
Decorators really make trying out new stuff super simple and I wish to see more of this in the future. 


