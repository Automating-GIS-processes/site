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

# Reclassifying data

Reclassifying data based on specific criteria is a common task when doing GIS
analysis. The purpose of this lesson is to see how we can reclassify values
based on some criteria. We could, for example, classify information based on
travel times and housing prices using these criteria:


1. if travel time to my work is less than 30 minutes, **AND**
2. the rent of the apartment is less than 1000 € per month

If both criteria are met: I go to see the appartment and try to rent it
If not: I continue to look for something else


In this tutorial, we will:

1. Use classification schemes from the PySAL [mapclassify
   library](https://pysal.org/mapclassify/) to classify travel times into
   multiple classes.

2. Create a custom classifier to classify travel times and distances in order
   to find out good locations to buy an apartment with these conditions:
   - good public transport accessibility to city center
   - bit further away from city center where the prices are presumably lower


## Input data

We will use [Travel Time Matrix data from
Helsinki](https://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix/)
that contains travel time and distance information for routes between all 250 m
x 250 m grid cell centroids (n = 13231) in the Capital Region of Helsinki by
walking, cycling, public transportation and car.

```{code-cell}
import pathlib 
NOTEBOOK_PATH = pathlib.Path().resolve()
DATA_DIRECTORY = NOTEBOOK_PATH / "data"
```

```{code-cell}
import geopandas
accessibility_grid = geopandas.read_file(
    DATA_DIRECTORY
    / "helsinki_region_travel_times_to_railway_station"
    / "helsinki_region_travel_times_to_railway_station.gpkg"
)
accessibility_grid.head()
```


## Common classifiers

### Classification schemes for thematic maps

[PySAL](https://pysal.org/) -module is an extensive Python library for spatial
analysis. It also includes all of the most common data classifiers that are
used commonly e.g. when visualizing data. Available map classifiers in [pysal's
mapclassify -module](https://github.com/pysal/mapclassify):

- Box Plot
- Equal Interval
- Fisher Jenks
- Fisher Jenks Sampled
- HeadTail Breaks
- Jenks Caspall
- Jenks Caspall Forced
- Jenks Caspall Sampled
- Max P Classifier
- Maximum Breaks
- Natural Breaks
- Quantiles
- Percentiles
- Std Mean
- User Defined


There are plenty of different variables in the accessibility data set (see
[from here the
description](http://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2015)
for all attributes) but what we are interested in are columns called `pt_r_tt`
which is telling the time in minutes that it takes to reach city center from
different parts of the city, and `walk_d` that tells the network distance by
roads to reach city center from different parts of the city (almost equal to
Euclidian distance).

**The NoData values are presented with value -1**. 
Thus we need to remove the No Data values first.

```{code-cell}
# Include only data that is above or equal to 0
accessibility_grid = accessibility_grid.loc[accessibility_grid['pt_r_tt'] >=0]
```

Let's plot the data and see how it looks like
- `cmap` parameter defines the color map. Read more about [choosing colormaps in matplotlib](https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html)
- `scheme` option scales the colors according to a classification scheme (requires `mapclassify` module to be installed):

```{code-cell}
# Plot using 9 classes and classify the values using "Natural Breaks" classification
accessibility_grid.plot(column="pt_r_tt", scheme="Natural_Breaks", k=9, cmap="RdYlBu", linewidth=0, legend=True)
```

As we can see from this map, the travel times are lower in the south where the
city center is located but there are some areas of "good" accessibility also in
some other areas (where the color is red).

Let's also make a plot about walking distances:

```{code-cell}
# Plot walking distance
accessibility_grid.plot(column="walk_d", scheme="Natural_Breaks", k=9, cmap="RdYlBu", linewidth=0, legend=True)
```

Okay, from here we can see that the walking distances (along road network)
reminds more or less Euclidian distances. 

### Applying classifiers to data

As mentioned, the `scheme` option defines the classification scheme using
`pysal/mapclassify`. Let's have a closer look at how these classifiers work.

```{code-cell}
import mapclassify
```

#### Natural Breaks

```{code-cell}
mapclassify.NaturalBreaks(y=accessibility_grid['pt_r_tt'], k=9)
```

#### Quantiles (default is 5 classes):

```{code-cell}
mapclassify.Quantiles(y=accessibility_grid['pt_r_tt'])
```

#### Extract threshold values

It's possible to extract the threshold values into an array:

```{code-cell}
classifier = mapclassify.NaturalBreaks(y=accessibility_grid['pt_r_tt'], k=9)
classifier.bins
```

Let's apply one of the `Pysal` classifiers into our data and classify the
travel times by public transport into 9 classes
The classifier needs to be initialized first with `make()` function that takes
the number of desired classes as input parameter

```{code-cell}
# Create a Natural Breaks classifier
classifier = mapclassify.NaturalBreaks.make(k=9)
```

- Now we can apply that classifier into our data by using `apply` -function

```{code-cell}
# Classify the data
classifications = accessibility_grid[['pt_r_tt']].apply(classifier)

# Let's see what we have
classifications.head()
```

```{code-cell}
type(classifications)
```

Okay, so now we have a DataFrame where our input column was classified into 9
different classes (numbers 1-9) based on [Natural Breaks
classification](http://wiki-1-1930356585.us-east-1.elb.amazonaws.com/wiki/index.php/Jenks_Natural_Breaks_Classification).

We can also add the classification values directly into a new column in our dataframe:

```{code-cell}
# Rename the column so that we know that it was classified with natural breaks
accessibility_grid['nb_pt_r_tt'] = accessibility_grid[['pt_r_tt']].apply(classifier)

# Check the original values and classification
accessibility_grid[['pt_r_tt', 'nb_pt_r_tt']].head()
```

Great, now we have those values in our accessibility GeoDataFrame. Let's
visualize the results and see how they look.

```{code-cell}
# Plot
accessibility_grid.plot(column="nb_pt_r_tt", linewidth=0, legend=True)
```

And here we go, now we have a map where we have used one of the common
classifiers to classify our data into 9 classes.


## Plotting a histogram

A histogram is a graphic representation of the distribution of the data. When
classifying the data, it's always good to consider how the data is distributed,
and how the classification shceme divides values into different ranges. 

- plot the histogram using [pandas.DataFrame.plot.hist](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.hist.html)
- Number of histogram bins (groups of data) can be controlled using the parameter `bins`:

```{code-cell}
# Histogram for public transport rush hour travel time
accessibility_grid['pt_r_tt'].plot.hist(bins=50)
```

Let's also add threshold values on thop of the histogram as vertical lines.

- Natural Breaks:

```{code-cell}
import matplotlib.pyplot as plt

# Define classifier
classifier = mapclassify.NaturalBreaks(y=accessibility_grid['pt_r_tt'], k=9)

# Plot histogram for public transport rush hour travel time
accessibility_grid['pt_r_tt'].plot.hist(bins=50)

# Add vertical lines for class breaks
for value in classifier.bins:
    plt.axvline(value, color='k', linestyle='dashed', linewidth=1)
```

- Quantiles:

```{code-cell}
# Define classifier
classifier = mapclassify.Quantiles(y=accessibility_grid['pt_r_tt'])

# Plot histogram for public transport rush hour travel time
accessibility_grid['pt_r_tt'].plot.hist(bins=50)

for value in classifier.bins:
    plt.axvline(value, color='k', linestyle='dashed', linewidth=1)
```

:::{admonition} Check your understanding
:class: tip

Select another column from the data (for example, travel times by car:
`car_r_t`). Do the following visualizations using one of the classification
schemes available from
[pysal/mapclassify](https://github.com/pysal/mapclassify):
    
- histogram with vertical lines showing the classification bins
- thematic map using the classification scheme
:::


## Creating a custom classifier

### Multicriteria data classification**

Let's create a function where we classify the geometries into two classes based
on a given `threshold` -parameter. If the area of a polygon is lower than the
threshold value (average size of the lake), the output column will get a value
0, if it is larger, it will get a value 1. This kind of classification is often
called a [binary
classification](https://en.wikipedia.org/wiki/Binary_classification).

First we need to create a function for our classification task. This function
takes a single row of the GeoDataFrame as input, plus few other parameters that
we can use.

It also possible to do classifiers with multiple criteria easily in
Pandas/Geopandas by extending the example that we started earlier. Now we will
modify our binaryClassifier function a bit so that it classifies the data based
on two columns.

- Let's call it `custom_classifier` that does the binary classification based on two treshold values:

```{code-cell}
def custom_classifier(row, src_col1, src_col2, threshold1, threshold2, output_col):
    """Custom classirifer that can be applied on each row of a pandas dataframe (axis=1).
    
    This function classifies data based on values in two source columns and
    stores the output value in the output column.  Output values is 1 if the value
    in src_col1 is LOWER than the threshold1 value AND the value in src_col2 is
    HIGHER than the threshold2 value.  In all other cases, output value is 0.
    
    Args:
        row: one row of data
        src_col1: source column name associated with threshold1
        src_col2: source column name associated with threshold2
        threshold1: upper threshold value for src_col1
        threshold2: lower threshold value for src_col2
        output_col: output column name

    Returns:
        updated row of data.
    """

    # If condition is true, assign 1 into output column
    if row[src_col1] < threshold1 and row[src_col2] > threshold2:
        row[output_col] = 1
    
    # Else, assign 1 into output column
    else:
        row[output_col] = 0

    # Return the updated row
    return row
```

Now we have defined the function, and we can start using it.

- Let's do our classification based on two criteria and find out grid cells
  where the **travel time is lower or equal to 20 minutes** but they are
  further away **than 4 km (4000 meters) from city center**.

- Let's create an empty column for our classification results called
  `"suitable_area"`.

```{code-cell}
# Create column for the classification results
accessibility_grid["suitable_area"] = None

# Use the function
accessibility_grid = accessibility_grid.apply(custom_classifier, 
    src_col1='pt_r_tt', 
    src_col2='walk_d', 
    threshold1=20, 
    threshold2=4000, 
    output_col="suitable_area", 
    axis=1
)

# See the first rows
accessibility_grid.head()
```

Okey we have new values in `suitable_area` -column.

- How many Polygons are suitable for us? Let's find out by using a Pandas
  function called `value_counts()` that return the count of different values in
  our column.

```{code-cell}
# Get value counts
accessibility_grid['suitable_area'].value_counts()
```

Okay, so there seems to be nine suitable locations for us where we can try to
find an appartment to buy.

- Let's see where they are located:

```{code-cell}
# Plot
accessibility_grid.plot(column="suitable_area", linewidth=0)
```

A-haa, okay so we can see that suitable places for us with our criteria seem to
be located in the eastern part from the city center. Actually, those locations
are along the metro line which makes them good locations in terms of travel
time to city center since metro is really fast travel mode.
