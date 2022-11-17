---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Simplifying geometries


Sometimes it might be useful to be able to simplify geometries. This could be
something to consider for example when you have very detailed spatial features
that cover the whole world. If you make a map that covers the whole world, it
is unnecessary to have really detailed geometries because it is simply
impossible to see those small details from your map. Furthermore, it takes a
long time to actually render a large quantity of features into a map. Here, we
will see how it is possible to simplify geometric features in Python.

As an example we will use data representing the Amazon river in South America,
and simplify it's geometries.

Let's first read the data and see how the river looks like:

```{code-cell}
import pathlib 
NOTEBOOK_PATH = pathlib.Path().resolve()
DATA_DIRECTORY = NOTEBOOK_PATH / "data"
```


```{code-cell}
import geopandas

amazon = geopandas.read_file(DATA_DIRECTORY / "amazon_river" / "amazon_river.gpkg")

amazon.head()
```

```{code-cell}
amazon.crs
```

```{code-cell}
amazon.plot()
```

The LineString that is presented here is quite detailed, so let's see how we
can generalize them a bit. As we can see from the coordinate reference system,
the data is projected in a system using [Mercator projection based on
SIRGAS datum](http://spatialreference.org/ref/sr-org/7868/), and metres as a unit. 

Generalization can be done easily by using a Shapely function called
`.simplify()`. The `tolerance` parameter can be used to adjusts how much
geometries should be generalized. **The tolerance value is tied to the
coordinate system of the geometries**. Hence, the value we pass here is 20 000
**meters** (20 kilometers).


```{code-cell}
# Generalize geometry
amazon['simplegeom'] = amazon.simplify(tolerance=20000)

# Set geometry to be our new simlified geometry
amazon = amazon.set_geometry('simplegeom')

# Plot 
amazon.plot()
```

Nice! As a result, now we have simplified our LineString quite significantly as we can see from the map.
