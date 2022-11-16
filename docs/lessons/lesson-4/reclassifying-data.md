---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Data reclassification

Reclassifying data based on specific criteria is a common task when doing GIS analysis. The purpose of this lesson is to see how we can reclassify values based on some criteria. We could, for example, classify information based on travel times and housing prices using these criteria:

```
1. if travel time to my work is less than 30 minutes

    AND

    2. the rent of the apartment is less than 1000 € per month

    ------------------------------------------------------

    IF TRUE: ==> I go to view it and try to rent the apartment
    IF NOT TRUE: ==> I continue looking for something else
```

In this tutorial, we will:

1. Use classification schemes from the PySAL [mapclassify library](https://pysal.org/mapclassify/) to classify travel times into multiple classes.

2. Create a custom classifier to classify travel times and distances in order to find out good locations to buy an apartment with these conditions:
   - good public transport accessibility to city center
   - bit further away from city center where the prices are presumably lower

## Input data

We will use [Travel Time Matrix data from Helsinki](https://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix/) that contains travel time and distance information for 
routes between all 250 m x 250 m grid cell centroids (n = 13231) in the Capital Region of Helsinki by walking, cycling, public transportation and car.

In this tutorial, we will use the geojson file generated in the previous section:
`"data/TravelTimes_to_5975375_RailwayStation_Helsinki.geojson"`

Alternatively, you can re-download [L4 data](https://github.com/AutoGIS/data/raw/master/L4_data.zip) and use `"data/Travel_times_to_5975375_RailwayStation.shp"` as input file in here.



## Common classifiers

### Classification schemes for thematic maps


[PySAL](https://pysal.org/) -module is an extensive Python library for spatial analysis. It also includes all of the most common data classifiers that are used commonly e.g. when visualizing data. Available map classifiers in [pysal's mapclassify -module](https://github.com/pysal/mapclassify):

 - Box_Plot
 - Equal_Interval
 - Fisher_Jenks
 - Fisher_Jenks_Sampled
 - HeadTail_Breaks
 - Jenks_Caspall
 - Jenks_Caspall_Forced
 - Jenks_Caspall_Sampled
 - Max_P_Classifier
 - Maximum_Breaks
 - Natural_Breaks
 - Quantiles
 - Percentiles
 - Std_Mean
 - User_Defined

- First, we need to read our Travel Time data from Helsinki:

```{code-cell} ipython3
import geopandas as gpd

fp = "data/TravelTimes_to_5975375_RailwayStation_Helsinki.geojson"

# Read the GeoJSON file similarly as Shapefile
acc = gpd.read_file(fp)

# Let's see what we have
acc.head()
```

As we can see, there are plenty of different variables (see [from here the description](http://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2015) for all attributes) but what we are interested in are columns called `pt_r_tt` which is telling the time in minutes that it takes to reach city center from different parts of the city, and `walk_d` that tells the network distance by roads to reach city center from different parts of the city (almost equal to Euclidian distance).

**The NoData values are presented with value -1**. 

- Thus we need to remove the No Data values first.

```{code-cell} ipython3
# Include only data that is above or equal to 0
acc = acc.loc[acc['pt_r_tt'] >=0]
```

- Let's plot the data and see how it looks like
- `cmap` parameter defines the color map. Read more about [choosing colormaps in matplotlib](https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html)
- `scheme` option scales the colors according to a classification scheme (requires `mapclassify` module to be installed):

```{code-cell} ipython3
import matplotlib.pyplot as plt

# Plot using 9 classes and classify the values using "Natural Breaks" classification
acc.plot(column="pt_r_tt", scheme="Natural_Breaks", k=9, cmap="RdYlBu", linewidth=0, legend=True)

# Use tight layout
plt.tight_layout()
```

As we can see from this map, the travel times are lower in the south where the city center is located but there are some areas of "good" accessibility also in some other areas (where the color is red).

- Let's also make a plot about walking distances:

```{code-cell} ipython3
# Plot walking distance
acc.plot(column="walk_d", scheme="Natural_Breaks", k=9, cmap="RdYlBu", linewidth=0, legend=True)

# Use tight layour
plt.tight_layout()
```

Okay, from here we can see that the walking distances (along road network) reminds more or less Euclidian distances. 

### Applying classifiers to data

As mentioned, the `scheme` option defines the classification scheme using `pysal/mapclassify`. Let's have a closer look at how these classifiers work.

```{code-cell} ipython3
import mapclassify
```

- Natural Breaks

```{code-cell} ipython3
mapclassify.NaturalBreaks(y=acc['pt_r_tt'], k=9)
```

- Quantiles (default is 5 classes):

```{code-cell} ipython3
mapclassify.Quantiles(y=acc['pt_r_tt'])
```

- It's possible to extract the threshold values into an array:

```{code-cell} ipython3
classifier = mapclassify.NaturalBreaks(y=acc['pt_r_tt'], k=9)
classifier.bins
```

- Let's apply one of the `Pysal` classifiers into our data and classify the travel times by public transport into 9 classes
- The classifier needs to be initialized first with `make()` function that takes the number of desired classes as input parameter

```{code-cell} ipython3
# Create a Natural Breaks classifier
classifier = mapclassify.NaturalBreaks.make(k=9)
```

- Now we can apply that classifier into our data by using `apply` -function

```{code-cell} ipython3
# Classify the data
classifications = acc[['pt_r_tt']].apply(classifier)

# Let's see what we have
classifications.head()
```

```{code-cell} ipython3
type(classifications)
```

Okay, so now we have a DataFrame where our input column was classified into 9 different classes (numbers 1-9) based on [Natural Breaks classification](http://wiki-1-1930356585.us-east-1.elb.amazonaws.com/wiki/index.php/Jenks_Natural_Breaks_Classification).

- We can also add the classification values directly into a new column in our dataframe:

```{code-cell} ipython3
# Rename the column so that we know that it was classified with natural breaks
acc['nb_pt_r_tt'] = acc[['pt_r_tt']].apply(classifier)

# Check the original values and classification
acc[['pt_r_tt', 'nb_pt_r_tt']].head()
```

Great, now we have those values in our accessibility GeoDataFrame. Let's visualize the results and see how they look.

```{code-cell} ipython3
# Plot
acc.plot(column="nb_pt_r_tt", linewidth=0, legend=True)

# Use tight layout
plt.tight_layout()
```

And here we go, now we have a map where we have used one of the common classifiers to classify our data into 9 classes.

+++

## Plotting a histogram

A histogram is a graphic representation of the distribution of the data. When classifying the data, it's always good to consider how the data is distributed, and how the classification shceme divides values into different ranges. 

- plot the histogram using [pandas.DataFrame.plot.hist](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.hist.html)
- Number of histogram bins (groups of data) can be controlled using the parameter `bins`:

```{code-cell} ipython3
# Histogram for public transport rush hour travel time
acc['pt_r_tt'].plot.hist(bins=50)
```

Let's also add threshold values on thop of the histogram as vertical lines.

- Natural Breaks:

```{code-cell} ipython3
# Define classifier
classifier = mapclassify.NaturalBreaks(y=acc['pt_r_tt'], k=9)

# Plot histogram for public transport rush hour travel time
acc['pt_r_tt'].plot.hist(bins=50)

# Add vertical lines for class breaks
for value in classifier.bins:
    plt.axvline(value, color='k', linestyle='dashed', linewidth=1)
```

- Quantiles:

```{code-cell} ipython3
# Define classifier
classifier = mapclassify.Quantiles(y=acc['pt_r_tt'])

# Plot histogram for public transport rush hour travel time
acc['pt_r_tt'].plot.hist(bins=50)

for value in classifier.bins:
    plt.axvline(value, color='k', linestyle='dashed', linewidth=1)
```


<div class="alert alert-info">

**Check your understanding**

Select another column from the data (for example, travel times by car: `car_r_t`). Do the following visualizations using one of the classification schemes available from [pysal/mapclassify](https://github.com/pysal/mapclassify):
    
- histogram with vertical lines showing the classification bins
- thematic map using the classification scheme


</div>

```{code-cell} ipython3

```

## Creating a custom classifier

**Multicriteria data classification**

Let's create a function where we classify the geometries into two classes based on a given `threshold` -parameter. If the area of a polygon is lower than the threshold value (average size of the lake), the output column will get a value 0, if it is larger, it will get a value 1. This kind of classification is often called a [binary classification](https://en.wikipedia.org/wiki/Binary_classification).

First we need to create a function for our classification task. This function takes a single row of the GeoDataFrame as input, plus few other parameters that we can use.

It also possible to do classifiers with multiple criteria easily in Pandas/Geopandas by extending the example that we started earlier. Now we will modify our binaryClassifier function a bit so that it classifies the data based on two columns.

- Let's call it `custom_classifier` that does the binary classification based on two treshold values:

```{code-cell} ipython3
def custom_classifier(row, src_col1, src_col2, threshold1, threshold2, output_col):
    """Custom classirifer that can be applied on each row of a pandas dataframe (axis=1).
    
    This function classifies data based on values in two source columns and stores the output value in the output column.
    Output values is 1 if the value in src_col1 is LOWER than the threshold1 value AND the value in src_col2 is HIGHER than the threshold2 value. 
    In all other cases, output value is 0.
    
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

- Let's do our classification based on two criteria and find out grid cells where the **travel time is lower or equal to 20 minutes** but they are further away **than 4 km (4000 meters) from city center**.

- Let's create an empty column for our classification results called `"suitable_area"`.

```{code-cell} ipython3
# Create column for the classification results
acc["suitable_area"] = None

# Use the function
acc = acc.apply(custom_classifier, 
                src_col1='pt_r_tt', 
                src_col2='walk_d', 
                threshold1=20, 
                threshold2=4000, 
                output_col="suitable_area", 
                axis=1)

# See the first rows
acc.head()
```

Okey we have new values in `suitable_area` -column.

- How many Polygons are suitable for us? Let's find out by using a Pandas function called `value_counts()` that return the count of different values in our column.

```{code-cell} ipython3
# Get value counts
acc['suitable_area'].value_counts()
```

Okay, so there seems to be nine suitable locations for us where we can try to find an appartment to buy.

- Let's see where they are located:

```{code-cell} ipython3
# Plot
acc.plot(column="suitable_area", linewidth=0)

# Use tight layour
plt.tight_layout()
```

A-haa, okay so we can see that suitable places for us with our criteria seem to be located in the
eastern part from the city center. Actually, those locations are along the metro line which makes them good locations in terms of travel time to city center since metro is really fast travel mode.

**Other examples**

Older course materials contain an example of applying a [custom binary classifier on the Corine land cover data](https://automating-gis-processes.github.io/2017/lessons/L4/reclassify.html#classifying-data>).
---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Case: hospital districts

+++

In this tutorial, we will create boundaries of Finnish hospital districts (*sairaanhoitopiiri* in Finnish) by dissolving municipality boundaries into larger entities. Main processing steps include a table join and dissolving the municipality geometries into larger entities.

We will combine information from [municipality polygons](https://www.stat.fi/org/avoindata/paikkatietoaineistot/vaesto_tilastointialueittain.html) from Statistics Finland and a [list of health care districts](https://www.kuntaliitto.fi/sosiaali-ja-terveysasiat/sairaanhoitopiirien-jasenkunnat) by the Finnish Municipality authority Kuntaliitto.

+++

Importing required python packages:

```{code-cell} ipython3
import json
import numpy as np
import pandas as pd
import geopandas as gpd
from pyproj import CRS
import matplotlib.pyplot as plt
```

## Read in data
- **Municipality polygons** from Statistics Finland web feature service: https://www.stat.fi/org/avoindata/paikkatietoaineistot/kuntapohjaiset_tilastointialueet.html
    - wfs: http://geo.stat.fi/geoserver/tilastointialueet/wfs?
    - feature: `tilastointialueet:kunta1000k` (most recent information about municipality polygons)




```{code-cell} ipython3
# For available features, see http://geo.stat.fi/geoserver/tilastointialueet/wfs?request=GetCapabilities
url = "http://geo.stat.fi/geoserver/tilastointialueet/wfs?request=GetFeature&typename=tilastointialueet:kunta1000k&outputformat=JSON"
geodata = gpd.read_file(url)
```

```{code-cell} ipython3
geodata.head()
```

```{code-cell} ipython3
# Check length (there are 310 municipalities in Finland in 2020)
len(geodata)
```

```{code-cell} ipython3
#Select and rename columns
geodata.rename(columns={'kunta':'code'}, inplace=True)
geodata = geodata[['code','name', 'geometry']]
geodata.head()
```

```{code-cell} ipython3
geodata.plot()
```

```{code-cell} ipython3
geodata.dtypes
```

- **Finnish municipalities with hospital district information** as an Excel spreadsheet 
    - Downloaded from: https://www.kuntaliitto.fi/sosiaali-ja-terveysasiat/sairaanhoitopiirien-jasenkunnat in March 2020. 
    - File `Shp_jäsenkunnat_2020.xls`, sheet `kunnat_shp_2020_ aakkosjärj.` This is the original unaltered file.
    - In this file, "shp" stands for "sairaanhoitopiiri" (hospital district in Finnish)
    
*Note: this data set does not include Åland (Ahvenanmaa). Åland municipalities are added in the later step.*
*Note: "hospital districts" is a more proper translation to sairaanhoitopiirit, but in this lesson I use "health care districts" to refer to these entities*

Excel files often come with additional formatting such as metadata on the first lines of the data array. This is why it is a good idea to download the file on your own computer and have a look at the data structure before reading in the file using Python.
It is also often a good idea to save the file as a csv file before reading in the data. However, it is also possible to read in data directly from Excel. For this, you need to have the xlrd module installed:

```
conda install -c conda-forge xlrd
```

Now we are ready to read in the data using pandas.

In the case of this health districts excel the header is located on the 4th row (index 3) of the excel spreadsheet. 

```{code-cell} ipython3
# Read in the excel spreadsheet
data = pd.read_excel(r"data/Shp_jäsenkunnat_2020.xls", sheet_name="kunnat_shp_2020_ aakkosjärj.", header=3)
```

```{code-cell} ipython3
data.head()
```

In addition, the first row after the header is empty. We can get rid of it using the dropna() -function:

```{code-cell} ipython3
data.dropna(inplace=True)
```

Check number of rows (16 Åland municipalities are missing)

```{code-cell} ipython3
len(data)
```

The data needs some fixing and cleaning after reading the excel sheet

```{code-cell} ipython3
# Rename columns from Finnish to English 
data.rename(columns={"kunta-\nkoodi":"code", 'sairaanhoitopiiri':'healthCareDistrict'}, inplace=True)

# Select only useful columns
data = data[['code','healthCareDistrict']]
```

```{code-cell} ipython3
data
```

Looks better! Now we need to prepare the data for table join. We will use the municipality code as the common key.

```{code-cell} ipython3
data.dtypes
```

The code column is currently a floating point number. We need to modify these codes so that they match the ones in the spatial data:

```{code-cell} ipython3
# Example using one code
number = data.at[1, "code"]
number
```

```{code-cell} ipython3
# Conver this number to character string 020
print("20".zfill(3))
```

Let's apply this process on all rows at once, and take into account different number of digits:

```{code-cell} ipython3
# Convert to character string
data["code"] = data["code"].astype(int).astype('str')

# Add missing zeros to municipality codes
data["code"] = data["code"].str.zfill(3)
```

```{code-cell} ipython3
data.head()
```

## Join Health district info to the municipality polygons

```{code-cell} ipython3
# Merge health district info to geodata using "code" as the common key
geodata = geodata.merge(data, on="code", how="left")
```

```{code-cell} ipython3
geodata
```

Looks good! However, Municipalities in the Åland island did not have a matching health care district in the data. Let's have a closer look: 

```{code-cell} ipython3
# List all municipalities that lack health district info:
geodata[geodata["healthCareDistrict"].isnull()].name
```

```{code-cell} ipython3
# Update "Ahvenanmaa" as the health care district for Åland municipalities (16 municipalities in total)
geodata.loc[geodata["healthCareDistrict"].isnull(), "healthCareDistrict"] = "Ahvenanmaa"
```

Check the count of municipalities per health care disctrict

```{code-cell} ipython3
geodata["healthCareDistrict"].value_counts()
```

## Create polygons for health care districts 

```{code-cell} ipython3
# Dissolve (=combine) municipality polygon geometries for each health care district
districts = geodata.dissolve(by='healthCareDistrict')
```

```{code-cell} ipython3
districts.reset_index(inplace=True)
```

```{code-cell} ipython3
# Select useful columns
districts = districts[["healthCareDistrict", "geometry"]]
```

```{code-cell} ipython3
districts
```

```{code-cell} ipython3
districts.plot(column='healthCareDistrict', cmap='tab20', k=20)
plt.axis('off')
```

```{code-cell} ipython3
# Write GeoJSON in original projection
districts.to_file("healthDistrictsEPSG3067.geojson", driver='GeoJSON', encoding='utf-8')
```

```{code-cell} ipython3
# Re-project to WGS84 and save again
wgs84 = CRS.from_epsg(4326)
districts.to_crs(wgs84).to_file("healthDistrictsEPSG4326.geojson", driver='GeoJSON', encoding='utf-8')
```

That's it! You can elaborate this workflow by joining additional data. For example, if you join population info per municipality you can sum it up for each health care district using the `aggfunc=sum` argument to get population count per health care district.
