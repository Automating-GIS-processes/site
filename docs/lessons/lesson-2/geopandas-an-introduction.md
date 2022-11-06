---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Introduction to geopandas

In this section, we will cover the basics of *geopandas*, a Python library to
interact with geospatial vector data.

[Geopandas](https://geopandas.org/) provides an easy-to-use interface to vector data sets. It combines the capabilities of *pandas*, the data analysis package we got to know in the [Geo-Python course](https://geo-python-site.readthedocs.io/en/latest/lessons/L5/pandas-overview.html), with the geometry handling functionality of [shapely](../lesson-1/geometry-objects), the [geo-spatial file format support of fiona](vector-data-io) and the [map projection libraries of pyproj](map-projections).



```{code-cell}
:tags: ["remove-input"]

import pathlib
import geopandas
import numpy
import pandas

DATA_DIRECTORY = pathlib.Path().resolve() / "data"

HIGHLIGHT_STYLE = "background: #f66161;"

# so the following block is a bit of bad magic to make the table output look
# nice (this cell is hidden, we are only interested in a short table listing
# in which the geometry column is highlighted).
#
# For this, we
#    1. convert the geopandas back into a ‘normal’ pandas.DataFrame with a shortened
#       WKT string in the geometry column
#    1b. while doing so, get rid of most of the columns (rename the remaining ones), and
#    1c. shorten the table to just 5 rows.
#    2. apply the style to all cells in the column "geometry", and to the axis-1-index "geometry"

# Why did I got via a ‘plain’ `pandas.DataFrame`?
# `pandas.set_option("display.max_colwidth", 40)` was ignored, so this seemed like the cleanest way

df = geopandas.read_file(DATA_DIRECTORY / "finland_topographic_database" / "m_L4132R_p.shp")

df["geom"] = df.geometry.to_wkt().apply(lambda wkt: wkt[:40] + " ...")

df = df[["RYHMA", "LUOKKA", "geom"]].loc[:4]
df = df.rename(columns={"RYHMA": "GROUP", "LUOKKA": "CLASS", "geom": "geometry"})

(
    df.style
        .applymap(lambda x: HIGHLIGHT_STYLE, subset=["geometry"])
        .apply_index(lambda x: numpy.where(x.isin(["geometry"]), HIGHLIGHT_STYLE, ""), axis=1)
)
```


% In this lesson, we will cover basics steps needed for interacting with spatial data in Python using geopandas:

% - Managing filepaths
% - Reading spatial data from file 
% - Geometry calculations 
% - Writing spatial data to file
% - Grouping and splitting spatial data into multiple layers


% Geopandas (http://geopandas.org/) makes it possible to work with geospatial data in Python in a relatively easy way. Geopandas combines the capabilities of the data analysis library [pandas](https://pandas.pydata.org/pandas-docs/stable/) with other packages like [shapely](https://shapely.readthedocs.io/en/stable/manual.html) and [fiona](https://fiona.readthedocs.io/en/latest/manual.html) for managing spatial data. 

% The main data structures in geopandas are `GeoSeries` and `GeoDataFrame` which extend the capabilities of `Series` and `DataFrames` from pandas. This means that we can use all our pandas skills also when working with geopandas!  If you need to refresh your memory about pandas, check out week 5 and 6 lesson materials from the [Geo-Python website](geo-python.github.io). 

% The main difference between geodataframes and pandas dataframes is that a [geodataframe](http://geopandas.org/data_structures.html#geodataframe) should contain one column for geometries. By default, the name of this column is `'geometry'`. The geometry column is a [geoseries](http://geopandas.org/data_structures.html#geoseries) which contains the geometries (points, lines, polygons, multipolygons etc.) as shapely objects. 

% ![geodataframe.png](img/geodataframe.png)

% As we learned in the Geo-Python course, it is conventional to import pandas as `pd`. Similarly,we will import geopandas as `gpd`:

% ```{code-cell} ipython3
% import geopandas as gpd
% ```

% ## Input data: Finnish topographic database 

% In this lesson we will work with the [National Land Survey of Finland (NLS) topographic database (from 2018)](https://www.maanmittauslaitos.fi/en/maps-and-spatial-data/expert-users/product-descriptions/topographic-database). 
% - The data set is licensed under the NLS' [open data licence](https://www.maanmittauslaitos.fi/en/opendata-licence-cc40) (CC BY 4.0).
% - Structure of the data is described in a separate Excel file ([download link](http://www.maanmittauslaitos.fi/sites/maanmittauslaitos.fi/files/attachments/2018/10/maastotietokanta_kohdemalli_eng.xlsx)).
% - Further information about file naming is available at [fairdata.fi](https://etsin.fairdata.fi/dataset/5023ecc7-914a-4494-9e32-d0a39d3b56ae).

% For this lesson, we have acquired a subset of the topographic database as shapefiles from the Helsinki Region in Finland via the [CSC open data portal](https://avaa.tdata.fi/web/paituli/latauspalvelu):

% ![Paituli data download](img/Paituli_maastotietokanta_download.png)


% In this lesson, we will focus on **terrain objects** (Feature group: "Terrain/1" in the topographic database). The Terrain/1 feature group contains several feature classes. **Our aim in this lesson is to save all the Terrain/1 feature classes into separate files**.

% *Terrain/1 features in the Topographic Database:*

% |  feature class | Name of feature                                            | Feature group |
% |----------------|------------------------------------------------------------|---------------|
% | 32421          | Motor traffic area                                         | Terrain/1     |
% | 32200          | Cemetery                                                   | Terrain/1     |
% | 34300          | Sand                                                       | Terrain/1     |
% | 34100          | Rock - area                                                | Terrain/1     |
% | 34700          | Rocky area                                                 | Terrain/1     |
% | 32500          | Quarry                                                     | Terrain/1     |
% | 32112          | Mineral resources extraction area, fine-grained material   | Terrain/1     |
% | 32111          | Mineral resources extraction area, coarse-grained material | Terrain/1     |
% | 32611          | Field                                                      | Terrain/1     |
% | 32612          | Garden                                                     | Terrain/1     |
% | 32800          | Meadow                                                     | Terrain/1     |
% | 32900          | Park                                                       | Terrain/1     |
% | 35300          | Paludified land                                            | Terrain/1     |
% | 35412          | Bog, easy to traverse forested                             | Terrain/1     |
% | 35411          | Open bog, easy to traverse treeless                        | Terrain/1     |
% | 35421          | Open fen, difficult to traverse treeless                   | Terrain/1     |
% | 33000          | Earth fill                                                 | Terrain/1     |
% | 33100          | Sports and recreation area                                 | Terrain/1     |
% | 36200          | Lake water                                                 | Terrain/1     |
% | 36313          | Watercourse area                                           | Terrain/1     |


% According to the [naming convention](https://etsin.fairdata.fi/dataset/5023ecc7-914a-4494-9e32-d0a39d3b56ae), all files that start with a letter `m` and end with `p` contain the objects we are interested in (Terrain/1 polygons). 

% +++

% ## Downloading data

% You can use `wget` program (available in Binder and CSC Notebooks) to download the data from the command line from this download link: https://github.com/AutoGIS/data/raw/master/L2_data.zip. Let's download the data into the same folder with the lesson 2 notebooks (`.../notebooks/L2`):

% 1. Open up a new terminal window
% 2. Navigate to the correct folder in the terminal:

% ```
% # Navigate to lesson 2 notebooks directory:
% cd autogis/notebooks/L2
%     
% ```
% 3. Use `wget` to dowload the data from the dowload link:
%     
% ```
% wget https://github.com/AutoGIS/data/raw/master/L2_data.zip
%     
% ```
% <div class="alert alert-info">

% **Copy-paste**
%     
% You can paste copied text in JupyterLab Terminal by pressing `SHIFT` + `RIGHT-CLICK` on your mouse and choosing `Paste`.

% </div>

% Once you have downloaded the `L2_data.zip` file into your (cloud) computer, you can unzip the file using `unzip` command in the Terminal (or e.g. 7zip on Windows if working with own computer). Run the following commands in the `.../notebooks/L2` -directory:

% ``` 
% $ unzip L2_data.zip
% $ ls L2_data

% ```
% You can also check the contents of the downloaded and unzipped file in the file browser window. 

% The L2_data folder contains several subfolders according to the file strucutre in the topographic database shapefile distribution. After unzipping the downloaded file, you can find the data for this tutorial under: `L2_data/NLS/2018/L4/L41/L4132R.shp`. Notice that Shapefile -fileformat contains many separate files such as `.dbf` that contains the attribute information, and `.prj` -file that contains information about coordinate reference system.

% +++

% ## Managing filepaths

% Built-in module `os` provides many useful functions for interacting with the operating system. One of the most useful submodules in the os package is the [os.path-module](https://docs.python.org/2/library/os.path.html) for manipulating file paths. This week, we have data in different sub-folders and we can practice how to use `os` path tools when defining filepaths.

% Let's import `os` and see how we can construct a filepath by joining a folder path and file name:

% ```{code-cell} ipython3
% import os

% # Define path to folder
% input_folder = r"L2_data/NLS/2018/L4/L41/L4132R.shp"

% # Join folder path and filename 
% fp = os.path.join(input_folder, "m_L4132R_p.shp")

% # Print out the full file path
% print(fp)
% ```

% ## Reading a Shapefile

% Esri Shapefile is the default file format when reading in data usign geopandas, so we only need to pass the file path in order to read in our data:

% ```{code-cell} ipython3
% import geopandas as gpd

% # Read file using gpd.read_file()
% data = gpd.read_file(fp)
% ```

% Let's check the data type:

% ```{code-cell} ipython3
% ---
% jupyter:
%   outputs_hidden: false
% ---
% type(data)
% ```

% Here we see that our `data` -variable is a `GeoDataFrame`. GeoDataFrame extends the functionalities of
% `pandas.DataFrame` in a way that it is possible to handle spatial data using similar approaches and datastructures as in pandas (hence the name geopandas). 

% Let's check the first rows of data: 

% ```{code-cell} ipython3
% ---
% jupyter:
%   outputs_hidden: false
% ---
% data.head()
% ```

% - Check all column names:

% ```{code-cell} ipython3
% data.columns.values
% ```

% As you might guess, the column names are in Finnish.
% Let's select only the useful columns and rename them into English:

% ```{code-cell} ipython3
% data = data[['RYHMA', 'LUOKKA',  'geometry']]
% ```

% Define new column names in a dictionary:

% ```{code-cell} ipython3
% colnames = {'RYHMA':'GROUP', 'LUOKKA':'CLASS'}
% ```

% Rename:

% ```{code-cell} ipython3
% data.rename(columns=colnames, inplace=True)
% ```

% Check the output:

% ```{code-cell} ipython3
% data.head()
% ```

% #### Check your understanding

% +++

% <div class="alert alert-info">
%     
% Figure out the following information from our input data using your pandas skills:
%     
% - Number of rows?
% - Number of classes?
% - Number of groups?
% </div>

% ```{code-cell} ipython3
% print("Number of rows", len(data['CLASS']))
% print("Number of classes", data['CLASS'].nunique())
% print("Number of groups", data['GROUP'].nunique())
% ```

% It is always a good idea to explore your data also on a map. Creating a simple map from a `GeoDataFrame` is really easy: you can use ``.plot()`` -function from geopandas that **creates a map based on the geometries of the data**. Geopandas actually uses matplotlib for plotting which we introduced in [Lesson 7 of the Geo-Python course](https://geo-python.github.io/site/notebooks/L7/matplotlib.html).

% Let's try it out, and plot our GeoDataFrame:

% ```{code-cell} ipython3
% ---
% jupyter:
%   outputs_hidden: false
% ---
% data.plot()
% ```

% Voilá! As we can see, it is really easy to produce a map out of your Shapefile with geopandas. Geopandas automatically positions your map in a way that it covers the whole extent of your data.

% *If you are living in the Helsinki region, you might recognize the shapes plotted on the map!*

% +++

% ## Geometries in Geopandas

% Geopandas takes advantage of Shapely's geometric objects. Geometries are stored in a column called *geometry* that is a default column name for
% storing geometric information in geopandas.

% +++

% Let's print the first 5 rows of the column 'geometry':

% ```{code-cell} ipython3
% ---
% jupyter:
%   outputs_hidden: false
% ---
% data['geometry'].head()
% ```

% As we can see the `geometry` column contains familiar looking values, namely Shapely `Polygon` -objects. Since the spatial data is stored as Shapely objects, **it is possible to use Shapely methods** when dealing with geometries in geopandas.

% Let's have a closer look at the polygons and try to apply some of the Shapely methods we are already familiar with.

% Let's start by checking the area of the first polygon in the data:

% ```{code-cell} ipython3
% # Access the geometry on the first row of data
% data.at[0, "geometry"]
% ```

% ```{code-cell} ipython3
% # Print information about the area 
% print("Area:", round(data.at[0, "geometry"].area, 0), "square meters")
% ```


% Let's do the same for the first five rows in the data; 

% - Iterate over the GeoDataFrame rows using the `iterrows()` -function that we learned [during the Lesson 6 of the Geo-Python course](https://geo-python.github.io/site/notebooks/L6/pandas/advanced-data-processing-with-pandas.html#Iterating-rows-and-using-self-made-functions-in-Pandas).
% - For each row, print the area of the polygon (here, we'll limit the for-loop to a selection of the first five rows):

% ```{code-cell} ipython3
% ---
% jupyter:
%   outputs_hidden: false
% ---
% # Iterate over rows and print the area of a Polygon
% for index, row in data[0:5].iterrows():
%     
%     # Get the area from the shapely-object stored in the geometry-column
%     poly_area = row['geometry'].area
%     
%     # Print info
%     print("Polygon area at index {index} is: {area:.0f} square meters".format(index=index, area=poly_area))
% ```

% As you see from here, all **pandas** methods, such as the `iterrows()` function, are directly available in Geopandas without the need to call pandas separately because Geopandas is an **extension** for pandas. 

% In practice, it is not necessary to use the iterrows()-approach to calculate the area for all features. Geodataframes and geoseries have an attribute `area` which we can use for accessing the area for each feature at once: 

% ```{code-cell} ipython3
% data.area
% ```

% Let's next create a new column into our GeoDataFrame where we calculate and store the areas of individual polygons:

% ```{code-cell} ipython3
% ---
% jupyter:
%   outputs_hidden: false
% ---
% # Create a new column called 'area' 
% data['area'] = data.area
% ```

% Check the output:

% ```{code-cell} ipython3
% data['area']
% ```

% These values correspond to the ones we saw in previous step when iterating rows.

% Let's check what is the `min`, `max` and `mean` of those areas using familiar functions from our previous Pandas lessions.

% ```{code-cell} ipython3
% # Maximum area
% round(data['area'].max(), 2)
% ```

% ```{code-cell} ipython3
% # Minimum area
% round(data['area'].min(), 2)
% ```

% ```{code-cell} ipython3
% # Average area
% round(data['area'].mean(), 2)
% ```

% ## Writing data into a shapefile

% It is possible to export GeoDataFrames into various data formats using the [to_file()](http://geopandas.org/io.html#writing-spatial-data) method. In our case, we want to export subsets of the data into Shapefiles (one file for each feature class).

% Let's first select one class (class number `36200`, "Lake water") from the data as a new GeoDataFrame:

% ```{code-cell} ipython3
% # Select a class
% selection = data.loc[data["CLASS"]==36200]
% ```

% Check the selection:

% ```{code-cell} ipython3
% selection.plot()
% ```

% - write this layer into a new Shapefile using the `gpd.to_file()` -function:

% ```{code-cell} ipython3
% # Create a output path for the data
% output_folder = r"L2_data/"
% output_fp = os.path.join(output_folder, "Class_36200.shp")
% ```

% ```{code-cell} ipython3
% # Write those rows into a new file (the default output file format is Shapefile)
% selection.to_file(output_fp)
% ```

% #### Check your understanding

% +++

% <div class="alert alert-info">

% Read the output Shapefile in a new geodataframe, and check that the data looks ok.
% </div>

% ```{code-cell} ipython3
% temp = gpd.read_file(output_fp)
% ```

% ```{code-cell} ipython3
% # Check first rows
% temp.head()
% ```

% ```{code-cell} ipython3
% # You can also plot the data for a visual check
% temp.plot()
% ```

% ## Grouping the Geodataframe

% One really useful function that can be used in Pandas/Geopandas is [groupby()](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.groupby.html) which groups data based on values on selected column(s). We saw and used this function already in Lesson 6 of the Geo-Python course. 

% Next we will automate the file export task; we will group the data based on column `CLASS` and export a shapefile for each class.

% Let's continue with the same input file we already read previously into the variable `data`. We also selected and renamed a subset of the columns.

% Check again the first rows of our input data:

% ```{code-cell} ipython3
% data.head()
% ```

% The `CLASS` column in the data contains information about different land use types. With `.unique()` -function we can quickly see all different values in that column:

% ```{code-cell} ipython3
% ---
% jupyter:
%   outputs_hidden: false
% ---
% # Print all unique values in the column
% data['CLASS'].unique()
% ```

% - Now we can use that information to group our data and save all land use types into different layers:

% ```{code-cell} ipython3
% ---
% jupyter:
%   outputs_hidden: false
% ---
% # Group the data by class
% grouped = data.groupby('CLASS')

% # Let's see what we have
% grouped
% ```

% As we can see, `groupby` -function gives us an object called `DataFrameGroupBy` which is similar to list of keys and values (in a dictionary) that we can iterate over.

% Check group keys:

% ```{code-cell} ipython3
% grouped.groups.keys()
% ```

% The group keys are unique values from the column by which we grouped the dataframe.

% Check how many rows of data each group has:

% ```{code-cell} ipython3
% ---
% jupyter:
%   outputs_hidden: false
% ---
% # Iterate over the grouped object
% for key, group in grouped:

%     # Let's check how many rows each group has:
%     print('Terrain class:', key)
%     print('Number of rows:', len(group), "\n")
% ```

% There are, for example, 56 lake polygons in the input data.

% +++

% We can also check how the _last_ group looks like (we have the variables in memory from the last iteration of the for-loop):

% ```{code-cell} ipython3
% group.head()
% ```

% Notice that the index numbers refer to the row numbers in the original data -GeoDataFrame.

% +++

% Check also the data type of the group:

% ```{code-cell} ipython3
% type(group)
% ```

% As we can see, each set of data are now grouped into separate GeoDataFrames, and we can save them into separate files.

% +++

% ### Saving multiple output files

% Let's **export each class into a separate Shapefile**. While doing this, we also want to **create unique filenames for each class**.

% When looping over the grouped object, information about the class is stored in the variable `key`, and we can use this information for creating new variable names inside the for-loop. For example, we want to name the shapefile containing lake polygons as "terrain_36200.shp".


% <div class="alert alert-info">

% **String formatting**
%     
% There are different approaches for formatting strings in Python. Here are a couple of different ways for putting together file-path names using two variables:

% ```
% basename = "terrain"
% key = 36200

% # OPTION 1. Concatenating using the `+` operator:
% out_fp = basename + "_" + str(key) + ".shp"

% # OPTION 2. Positional formatting using `%` operator
% out_fp = "%s_%s.shp" %(basename, key)
%     
% # OPTION 3. Positional formatting using `.format()`
% out_fp = "{}_{}.shp".format(basename, key)
% ```
%     
% Read more from here: https://pyformat.info/
% </div>


% Let's now export terrain classes into separate Shapefiles.

% - First, create a new folder for the outputs:

% ```{code-cell} ipython3
% # Determine output directory
% output_folder = r"L2_data/"

% # Create a new folder called 'Results' 
% result_folder = os.path.join(output_folder, 'Results')

% # Check if the folder exists already
% if not os.path.exists(result_folder):
%     
%     print("Creating a folder for the results..")
%     # If it does not exist, create one
%     os.makedirs(result_folder)
%     
% else:
%     print("Results folder exists already.")
% ```

% At this point, you can go to the file browser and check that the new folder was created successfully.

% - Iterate over groups, create a file name, and save group to file:

% ```{code-cell} ipython3
% ---
% jupyter:
%   outputs_hidden: false
% ---
% # Iterate over the groups
% for key, group in grouped:
%     # Format the filename 
%     output_name = "terrain_{}.shp".format(key)

%     # Print information about the process
%     print("Saving file", os.path.basename(output_name))

%     # Create an output path
%     outpath = os.path.join(result_folder, output_name)

%     # Export the data
%     group.to_file(outpath)
% ```

% Excellent! Now we have saved those individual classes into separate Shapefiles and named the file according to the class name. These kind of grouping operations can be really handy when dealing with layers of spatial data. Doing similar process manually would be really laborious and error-prone.

% +++

% ### Extra: save data to csv

% +++

% We can also extract basic statistics from our geodataframe, and save this information as a text file. 

% Let's summarize the total area of each group:

% ```{code-cell} ipython3
% area_info = grouped.area.sum().round()
% ```

% ```{code-cell} ipython3
% area_info
% ```

% - save area info to csv using pandas:

% ```{code-cell} ipython3
% # Create an output path
% area_info.to_csv(os.path.join(result_folder, "terrain_class_areas.csv"), header=True)
% ```

% ## Summary

% In this tutorial we introduced the first steps of using geopandas. More specifically you should know how to:

% 1. Read data from Shapefile using geopandas

% 2. Access geometry information in a geodataframe

% 4. Write GeoDataFrame data from Shapefile using geopandas

% 5. Automate a task to save specific rows from data into Shapefile based on specific key using `groupby()` -function

% 6. Extra: saving attribute information to a csv file.

