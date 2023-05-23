---
layout: single
title:  "Sometimes Numba can be slower than even Pandas... or why you should always benchmark"
date:   2023-05-23
---

In our last [post](../blog_pandas_groupby_with_numpy/) we saw that we can get much
more performance by rewriting Pandas GroupBy - Apply in NumPy. 
I also mentioned that I could not get Numba working with this code to see if it helps. 
In this blog, I want to talk about how I got Numba working and what the results were, 
but first, what's Numba?

## Numba

Numba is a just-in-time (JIT) compiler for Python 
that specializes in optimizing the performance of numerical computations. 
Well, that's all well and good, but what is a JIT compiler?
Most people are aware of compiled languages like C++, Rust or Java.
For these languages, the development flow is to write code, 
then compile the code to a binary and then run the binary. 
But for an interpreted language like Python, the second step is missing. 
Python is dynamic so the type of variables can be anything. 
This often means that Python functions spend a lot of time
checking variable attributes to then do the correct function call on them.
The final function call usually involves a C function call which is fast, 
but the overhead of type checking and edge cases are huge.

Compiled languages are typed and so no type checking is necessary. 
Compilers can use this and other knowledge to create optimized binaries.
The question then arises: how can we leverage compilers for Python code? 
JIT is one way to solve this issue. 
While the code is running, Numba analyzes variables and code flow to create optimized functions.
This also means that the first function call can be slow and therefore JIT
is not recommended for code with low runtimes. On the other hand if your code
spends a long time on certain functions, then it can be very worthwhile.
There are ways around this but we will keep that out of scope of this post. 

Back to Numba. It is a JIT compiler for Python, especially for numeric applications. 
The simplest way to use it is to use a decorator around your function. For eg.

```
from numba import njit

@njit
def plus_one(a):
    return a+1
```

And that's it. In theory this should make the function much faster. 
But the important part is "in theory".

## Customizations

So let's get back to our problem. We were trying to speed up
the Pandas GroupBy-Apply with NumPy. And we did manage to make it much faster.
But what if we could make it even faster. Well, how about using Numba.
Almost immediately, we hit a wall. We want to use the `njit` decorator
around functions that have NumPy API calls. And the issue is that Numba
does not support all NumPy functions. And amongst the unsupported ones
is `lexsort` that we are using. We are stuck. Or are we?
Turns out others have asked the same question. And some have [answered](https://github.com/numba/numba/issues/5688). 
So, we use this version of `lexsort`. 

But then we hit another wall. `apply_along_axis` is also not supported. 
But this is simpler to solve. 
This is just an optimized for loop, so let's just create a for loop and hopefully Numba should take care of speedup.

```
    interpolate_values = np.zeros(reshape_x_size)
    for i in range(reshape_x_size):
        interpolate_values[i] = np.interp(
            x=_INTERPOLATE_AT, xp=x_unique_values, fp=y_values[i, :]
        )
```

## Benchmarking

And that's it(I make it sound simple even though I had to spend quite some time finding and fixing issues).
We now have a function decorated with `njit` and we are ready to reap the rewards. 
So, as always, we benchmark. Recall that we use `timeit` for this. What do we get?

```
Pandas times: [0.35364490200000004, 0.33443024, 0.3303176189999999, 0.32855506999999995, 0.33024766799999994]
Numpy times: [0.0469579229999999, 0.036730967, 0.03578966599999989, 0.035751120000000025, 0.03562025000000002]
Numba with NumPy times: [4.562287851, 0.6207038340000004, 0.6222665610000009, 0.584906624, 0.5903799620000001]
```

Which is... pretty bad. You can see that the first function call is pretty slow
and that is expected. It should become much faster in subsequent function calls to recoup that loss.
But actually, its so much slower. 
In fact, it is slower than the Pandas time!


## Final thoughts

I am sure that there are optimizations that could be tried.
But Numba itself was pretty finicky and it was so slow that I did not want to delve deeper
Still, I think it was an interesting exercise. 
I had the chance to look at Numba, and believe me sometimes it can really be way faster.
However, know that this is not guaranteed and so, always Benchmark!

  

