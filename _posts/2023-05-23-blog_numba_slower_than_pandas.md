---
layout: single
title:  "Sometimes Numba can be slower than Pandas... or why you should always benchmark"
date:   2023-05-23
---

In our last [post](../blog_pandas_groupby_with_numpy/) we saw that we can get much
more performance by rewriting Pandas GroupBy - Apply in NumPy. 
I also mentioned that I could not get Numba working with this code to see if it helps. 
In this blog, I want to talk about how I got Numba working and what were the results, 
but first, what's Numba?

Numba is a just-in-time (JIT) compiler for Python 
that specializes in optimizing the performance of numerical computations. 
Well, that's all well and good, but what is a JIT compiler?
Most people will be aware of compiled languages like C++, Rust or Java.
For these languages, the development flow is to write code, 
then compile the code to a binary and then run the binary. 
But for an interpreted language like Python, the second step is missing. 
