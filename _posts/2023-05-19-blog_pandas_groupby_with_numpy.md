---
layout: single
title:  "Using NumPy to replace Pandas GroupBy-Apply pattern for performance"
date:   2023-05-19
---

At my dayjob we are starting to use PyPpark a lot. 
The DataFrame API is great however there are times when it is not sufficient
because it does not cover every single piece of functionality we may want.
This is where the [Pandas UDF](https://spark.apache.org/docs/3.1.2/api/python/user_guide/arrow_pandas.html) functionality comes in. 
The nice thing about the Pandas UDF functionality is that it uses Arrow for data transfer
between Spark and Pandas which minimizes serialization-deserialization costs. 
I have a slight preference for Pandas Function API over Pandas UDF 
but let's now get to the meat of the post which is about speeding up 
the Pandas GroupBy-Apply pattern by using NumPy instead. 

## Setup data

Let's first start with example data to explain what we are doing. 
We construct an artificial dataset that has 4 columns, `category, year, x, y`. 
We will select 3 categories for `category`, namely `["red", "green", "blue"]`.
We have years representing every year from 2010 to 2020. 
The `x` column always have the same values for each category and year, `0, 0.1, 0.25, 0.5, 1`
and the `y` values monotonically increase with the `x` values. 
If you, like me, struggle to make sense of artificial data, 
let's assume this data represents the sales of 3 categories of balls for each year. 
The `y` value is the total sales after `x` fraction of the year is finished. 

```
_CATEGORIES = ["red", "green", "blue"]
_YEARS = range(2010, 2021)
_X_VALUES = [0, 0.1, 0.25, 0.5, 1.0]

def create_dataframe() -> pd.DataFrame:
    data = []
    for category in _CATEGORIES:
        for year in _YEARS:
            for x in _X_VALUES:
                y = 25.0 * x + random.uniform(0, 1)
                data.append([category, year, x, y])

    return pd.DataFrame(data, columns=["category", "year", "x", "y"])
```

## Pandas GroupBy

So, what do we want to do? Let's assume that we want to find out 
what the sales for at 30% of each year and category. 
How do we do that? Since we already spoiled this in the title,
let's get to it. We can do a GroupBy-Apply for this. 

```
def pandas_groupby(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["category", "year"])
        .apply(lambda df: np.interp(0.3, df["x"], df["y"]))
        .rename("y")
        .reset_index()
    )
```

That's pretty easy, right? This does what we want, although
Pandas does weird stuff when you do GroupBy. It creates a multi-index
with the columns that were used for the GroupBy. 
So, for example, if we were to use this UDF for PySpark, we would 
waste processing time resetting the index. But that's Pandas. 

## NumPy 

How would we do this in NumPy. There is no GroupBy in NumPy. 
There's a very old [NEP](https://numpy.org/neps/nep-0008-groupby_additions.html)
that proposed this, but obviously it was not implemented. 
So, how would we do this. 
Essentially what we need to do is group indices for category and year first. 
NumPy has a nice way of doing this with `lexsort`.  

```
sort_indices = np.lexsort((x_values, years, categories))
```

This will first sort by `categories`, then `years`, then `x_values`. 
We also sort by `x_values` since we need this for the next step. 
Then what we do is `reshape` the 1D array to a 2D array.
So basically, for each `category` and `year` we have a column of `y_values`. 
And then we use `apply_along_axis`, since we don't want to use a Pandas apply. 
A Pandas apply is essentially a Python for loop which is slow! 
So, we use the NumPy vectorized version. 

```
def _interpolate_wrapper(fp: np.ndarray, xp: np.ndarray, x: float) -> float:
    return float(np.interp(x=x, xp=xp, fp=fp))

def numpy_groupby(df: pd.DataFrame) -> pd.DataFrame:
      ....
      ....
      y_values = y_values.reshape([-1, num_x_unique_values])
      interpolated_y_values = np.apply_along_axis(
          _interpolate_wrapper,
          axis=1,
          arr=y_values,
          x=_INTERPOLATE_AT,
          xp=x_unique_values,
      )
```

Why did we have to create a new function `_interpolate_wrapper`?
Well, that is because `apply_along_axis` wants to use the first
argument of the function being passed, even though we are specializing that
in the function arguments. So, we had to create a wrapper to make
`y_values` be the first argument.
We can of course use different functions if that is what we wanted to do.
So that's it. We have implemented the same functionality.
But why do this? That takes us to.... benchmarking.

## Benchmarking

We use `timeit` to compare the times of the 2 different ways of doing
our interpolation.  

```
if __name__ == "__main__":
    numpy_times = timeit.repeat(
        "numpy_groupby(df)",
        "from __main__ import create_dataframe, numpy_groupby;df = create_dataframe();",
        number=100,
    )
    print(f"Numpy times: {numpy_times}")
    pandas_times = timeit.repeat(
        "pandas_groupby(df)",
        "from __main__ import create_dataframe, pandas_groupby;df = create_dataframe()",
        number=100,
    )
    print(f"Pandas times: {pandas_times}")
```

This will run the 2 functions a 100 times, and repeat it 5 times which
is the default value for `repeat`. The output will be then
a list of 5 numbers for each of the 2 function calls.
Each of the 5 numbers represent the time for one of the 5 runs.
I am running this on a 2019 Macbook with an i9 Intel processor.  
And here are the results. 

```
Numpy times: [0.039644957000000036, 0.03817060300000008, 0.037790082, 0.037306608000000074, 0.03735358100000008]
Pandas times: [0.36932151, 0.36356516000000005, 0.358974868, 0.3752171339999999, 0.36828465099999974]
```

Well, clearly we can see almost an order of magnitude(10X) improvement in performance.
That is A LOT. 
And as our data becomes bigger and bigger in size, 
this can be the difference between having a $500 vs a $5000 job. 
Or $5000 vs $50000. Or.... you get the point.

## Code

The code is available [here](https://github.com/vikramsg/blog_code/tree/main/numpy_groupby). 





