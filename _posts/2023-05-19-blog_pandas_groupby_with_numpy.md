---
layout: single
title:  "Using NumPy "
date:   2023-05-19
---

At my dayjob we are starting to use PyPpark a lot. 
The DataFrame API is great however there are times when it is not sufficient
because it does not cover every single piece of functionality we may want.
This is where the [Pandas UDF](https://spark.apache.org/docs/3.1.2/api/python/user_guide/arrow_pandas.html) functionality comes in. 
The nice thing about the Pandas UDF functionality is that it uses Arrow for data transfer
between Spark and Pandas which minimizes serialization-deserialization costs. 
I have a slight preference for Pandas Function API over Pandas UDF 
but let's now get to the 

