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

# Spatial join

% [Spatial join](http://wiki.gis.com/wiki/index.php/Spatial_Join) is
% yet another classic GIS problem. Getting attributes from one layer and
% transferring them into another layer based on their spatial relationship
% is something you most likely need to do on a regular basis.
% 
% In the previous section we learned how to perform **a Point in Polygon query**.
% We can now use the same logic to conduct **a spatial join** between two layers based on their
% spatial relationship. We could, for example, join the attributes of a polygon layer into a point layer where each point would get the
% attributes of a polygon that ``contains`` the point.
% 
% Luckily, [spatial join is already implemented in Geopandas](http://geopandas.org/mergingdata.html#spatial-joins), thus we do not need to create our own function for doing it. There are three possible types of
% join that can be applied in spatial join that are determined with ``op`` -parameter in the ``gpd.sjoin()`` -function:
% 
% -  ``"intersects"``
% -  ``"within"``
% -  ``"contains"``
% 
% Sounds familiar? Yep, all of those spatial relationships were discussed
% in the [Point in Polygon lesson](point-in-polygon.ipynb), thus you should know how they work. 
% 
% Furthermore, pay attention to the different options for the type of join via the `how` parameter; "left", "right" and "inner". You can read more about these options in the [geopandas sjoin documentation](http://geopandas.org/mergingdata.html#sjoin-arguments) and pandas guide for [merge, join and concatenate](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html)
% 
% Let's perform a spatial join between these two layers:
% - **Addresses:** the geocoded address-point (we created this Shapefile in the geocoding tutorial)
% - **Population grid:** 250m x 250m grid polygon layer that contains population information from the Helsinki Region.
%     - The population grid a dataset is produced by the **Helsinki Region Environmental
% Services Authority (HSY)** (see [this page](https://www.hsy.fi/fi/asiantuntijalle/avoindata/Sivut/AvoinData.aspx?dataID=7) to access data from different years).
%     - You can download the data from [from this link](https://www.hsy.fi/sites/AvoinData/AvoinData/SYT/Tietoyhteistyoyksikko/Shape%20(Esri)/V%C3%A4est%C3%B6tietoruudukko/Vaestotietoruudukko_2018_SHP.zip) in the  [Helsinki Region Infroshare
% (HRI) open data portal](https://hri.fi/en_gb/).
% 
% 
% 
% - Here, we will access the data directly from the HSY wfs:
% 
% 
% ```{code-cell} ipython3
% import geopandas as gpd
% from pyproj import CRS
% import requests
% import geojson
% 
% # Specify the url for web feature service
% url = 'https://kartta.hsy.fi/geoserver/wfs'
% 
% # Specify parameters (read data in json format). 
% # Available feature types in this particular data source: http://geo.stat.fi/geoserver/vaestoruutu/wfs?service=wfs&version=2.0.0&request=describeFeatureType
% params = dict(service='WFS', 
%               version='2.0.0', 
%               request='GetFeature', 
%               typeName='asuminen_ja_maankaytto:Vaestotietoruudukko_2018', 
%               outputFormat='json')
% 
% # Fetch data from WFS using requests
% r = requests.get(url, params=params)
% 
% # Create GeoDataFrame from geojson
% pop = gpd.GeoDataFrame.from_features(geojson.loads(r.content))
% ```
% 
% Check the result: 
% 
% ```{code-cell} ipython3
% pop.head()
% ```
% 
% Okey so we have multiple columns in the dataset but the most important
% one here is the column `asukkaita` ("population" in Finnish) that
% tells the amount of inhabitants living under that polygon.
% 
% -  Let's change the name of that column into `pop18` so that it is
%    more intuitive. As you might remember, we can easily rename (Geo)DataFrame column names using the ``rename()`` function where we pass a dictionary of new column names like this: ``columns={'oldname': 'newname'}``.
% 
% ```{code-cell} ipython3
% # Change the name of a column
% pop = pop.rename(columns={'asukkaita': 'pop18'})
% 
% # Check the column names
% pop.columns
% ```
% 
% Let's also get rid of all unnecessary columns by selecting only columns that we need i.e. ``pop18`` and ``geometry``
% 
% ```{code-cell} ipython3
% # Subset columns
% pop = pop[["pop18", "geometry"]]
% ```
% 
% ```{code-cell} ipython3
% pop.head()
% ```
% 
% Now we have cleaned the data and have only those columns that we need
% for our analysis.
% 
% +++
% 
% ## Join the layers
% 
% Now we are ready to perform the spatial join between the two layers that
% we have. The aim here is to get information about **how many people live
% in a polygon that contains an individual address-point** . Thus, we want
% to join attributes from the population layer we just modified into the
% addresses point layer ``addresses.shp`` that we created trough gecoding in the previous section.
% 
% -  Read the addresses layer into memory:
% 
% ```{code-cell} ipython3
% # Addresses filpath
% addr_fp = r"data/addresses.shp"
% 
% # Read data
% addresses = gpd.read_file(addr_fp)
% ```
% 
% ```{code-cell} ipython3
% # Check the head of the file
% addresses.head()
% ```
% 
% In order to do a spatial join, the layers need to be in the same projection
% 
% - Check the crs of input layers:
% 
% ```{code-cell} ipython3
% addresses.crs
% ```
% 
% ```{code-cell} ipython3
% pop.crs
% ```
% 
% If the crs information is missing from the population grid, we can **define the coordinate reference system** as **ETRS GK-25 (EPSG:3879)** because we know what it is based on the [population grid metadata](https://hri.fi/data/dataset/vaestotietoruudukko). 
% 
% ```{code-cell} ipython3
% # Define crs
% pop.crs = CRS.from_epsg(3879).to_wkt()
% ```
% 
% ```{code-cell} ipython3
% pop.crs
% ```
% 
% ```{code-cell} ipython3
% # Are the layers in the same projection?
% addresses.crs == pop.crs
% ```
% 
% Let's re-project addresses to the projection of the population layer:
% 
% ```{code-cell} ipython3
% addresses = addresses.to_crs(pop.crs)
% ```
% 
% -  Let's make sure that the coordinate reference system of the layers
% are identical
% 
% ```{code-cell} ipython3
% # Check the crs of address points
% print(addresses.crs)
% 
% # Check the crs of population layer
% print(pop.crs)
% 
% # Do they match now?
% addresses.crs == pop.crs
% ```
% 
% Now they should be identical. Thus, we can be sure that when doing spatial
% queries between layers the locations match and we get the right results
% e.g. from the spatial join that we are conducting here.
% 
% -  Let's now join the attributes from ``pop`` GeoDataFrame into
%    ``addresses`` GeoDataFrame by using ``gpd.sjoin()`` -function:
% 
% ```{code-cell} ipython3
% # Make a spatial join
% join = gpd.sjoin(addresses, pop, how="inner", op="within")
% ```
% 
% ```{code-cell} ipython3
% join.head()
% ```
% 
% Awesome! Now we have performed a successful spatial join where we got
% two new columns into our ``join`` GeoDataFrame, i.e. ``index_right``
% that tells the index of the matching polygon in the population grid and
% ``pop18`` which is the population in the cell where the address-point is
% located.
% 
% - Let's still check how many rows of data we have now:
% 
% ```{code-cell} ipython3
% len(join)
% ```
% 
% Did we lose some data here? 
% 
% - Check how many addresses we had originally:
% 
% ```{code-cell} ipython3
% len(addresses)
% ```
% 
% If we plot the layers on top of each other, we can observe that some of the points are located outside the populated grid squares (increase figure size if you can't see this properly!)
% 
% ```{code-cell} ipython3
% import matplotlib.pyplot as plt
% 
% # Create a figure with one subplot
% fig, ax = plt.subplots(figsize=(15,8))
% 
% # Plot population grid
% pop.plot(ax=ax)
% 
% # Plot points
% addresses.plot(ax=ax, color='red', markersize=5)
% ```
% 
% Let's also visualize the joined output:
% 
% +++
% 
% Plot the points and use the ``pop18`` column to indicate the color.
%    ``cmap`` -parameter tells to use a sequential colormap for the
%    values, ``markersize`` adjusts the size of a point, ``scheme`` parameter can be used to adjust the classification method based on [pysal](http://pysal.readthedocs.io/en/latest/library/esda/mapclassify.html), and ``legend`` tells that we want to have a legend:
% 
% ```{code-cell} ipython3
% # Create a figure with one subplot
% fig, ax = plt.subplots(figsize=(10,6))
% 
% # Plot the points with population info
% join.plot(ax=ax, column='pop18', cmap="Reds", markersize=15, scheme='quantiles', legend=True);
% 
% # Add title
% plt.title("Amount of inhabitants living close the the point");
% 
% # Remove white space around the figure
% plt.tight_layout()
% ```
% 
% In a similar way, we can plot the original population grid and check the overall population distribution in Helsinki:
% 
% ```{code-cell} ipython3
% # Create a figure with one subplot
% fig, ax = plt.subplots(figsize=(10,6))
% 
% # Plot the grid with population info
% pop.plot(ax=ax, column='pop18', cmap="Reds", scheme='quantiles', legend=True);
% 
% # Add title
% plt.title("Population 2018 in 250 x 250 m grid squares");
% 
% # Remove white space around the figure
% plt.tight_layout()
% ```
% 
% Finally, let's save the result point layer into a file:
% 
% ```{code-cell} ipython3
% # Output path
% outfp = r"data/addresses_population.shp"
% 
% # Save to disk
% join.to_file(outfp)
% ```
