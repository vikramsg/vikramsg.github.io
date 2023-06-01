---
layout: single
title:  "Using arguments in a Pandas UDF for PySpark"
date:   2023-06-01
---

In our last [couple](../blog_pandas_groupby_with_numpy/) of [posts](../blog_numba_slower_than_pandas/) 
we looked at how we could optimize pandas functions. 
This post will be different. We still want to address issues that we face in the PySpark world,
but today we will not look at performance at all. 

## Parameters in a Pandas UDF 

In PySpark, when we want to use a Pandas UDF, we actually have 2 options. 
We can use the regular Pandas UDF, or we can use the [Pandas Function API](https://docs.databricks.com/pandas/pandas-function-apis.html). 
While both of them address the UDF question, the actual function implemented still operates on a Pandas DataFrame,
so that simplifies what we want to address in this post. 

Suppose, just as before, we create a Pandas DataFrame for 3 categories, and have a column represent sales
over a year. 

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

We can easily convert this to a Spark dataframe using `spark.createDataFrame`. 
Next, we want to get sales after a particular fraction of the year. 
Previously, we did the groupBy inside the Pandas function, but let's do it using PySpark now. 

```
_INTERPOLATE_AT = 0.3

def numpy_interpolate_global_args(indices: Tuple[int, int], df: pd.DataFrame) -> pd.DataFrame:
    interpolated_value = np.interp(_INTERPOLATE_AT, df["x"], df["y"])

    return pd.DataFrame(
        data={
            "category": indices[0],
            "year": indices[1],
            "interpolated_value": interpolated_value,
        },
        index=[indices[0]],
    )

interpolated_df_global_args = spark_df.groupBy(F.col("category"), F.col("year")).applyInPandas(
        numpy_interpolate_global_args, schema=interpolated_schema
    )
```

Notice that the Pandas Function `numpy_groupby_global_args` has a specific signature.
We can omit the first argument, and it will still work, but that's about the extent of the flexibility.
This is the required signature. So, to decide at what fraction of the year we want to interpolate at, 
we have used the global variable `_INTERPOLATE_AT`. This is... ugly, but it gets the job done. For now. 

However, what if we got the argument from a file, or CLI args. In theory, we could still use global arguments, 
but it gets messy really quickly. And testing becomes hard as well. So what do we do? 

## Use partial for arguments 

Let's use `partial` from `functools`. We can use this to specialize the UDF for a particular input value
and then use the new function as the argument for PySpark. Here's what it looks like.  

```
def numpy_interpolate_local_args(indices: Tuple[int, int], df: pd.DataFrame, interpolate_at: float) -> pd.DataFrame:
    interpolated_value = np.interp(interpolate_at, df["x"], df["y"])

    return pd.DataFrame(
        data={
            "category": indices[0],
            "year": indices[1],
            "interpolated_value": interpolated_value,
        },
        index=[indices[0]],
    )

numpy_groupby_interpolate_at = partial(numpy_interpolate_local_args, interpolate_at=_INTERPOLATE_AT)
interpolated_df = spark_df.groupBy(F.col("category"), F.col("year")).applyInPandas(
        numpy_groupby_interpolate_at, schema=interpolated_schema
    )
```

Neat, right? I like this pattern, but having `partial` can sometimes feel jarring as well as hacky. 


## Final thoughts

So what are your thoughts. Do you think this is a nice pattern to pass arguments to a Pandas UDF. 
If you have a better pattern, I would be interested to know. 
  
## Code

The code is available 
[here](https://github.com/vikramsg/blog_code/blob/main/spark_arguments/spark_args.py). 

