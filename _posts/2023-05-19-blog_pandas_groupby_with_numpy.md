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






