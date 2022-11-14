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

## Intersect
 
Similar to the spatial relationships `within` and `contains` covered in the [previous section](point-in-polygon-queries), another common geospatial query asks whether two geometries intersect or touch.

 [point-in-polygon]Another typical geospatial operation is to see if a geometry intersects
% or touches another one. Again, there are binary operations in Shapely for checking these spatial relationships:
% 
% - [intersects():](https://shapely.readthedocs.io/en/stable/manual.html#object.intersects) Two objects intersect if the boundary or interior of one object intersect in any way with the boundary or interior of the other object.
% 
% - [touches():](https://shapely.readthedocs.io/en/stable/manual.html#object.touches) Two objects touch if the objects have at least one point in common and their interiors do not intersect with any part of the other object.
%    
% 
% Let's try these out.
% 
% Let's create two LineStrings:
% 
% ```{code-cell} ipython3
% :deletable: true
% :editable: true
% 
% from shapely.geometry import LineString, MultiLineString
% 
% # Create two lines
% line_a = LineString([(0, 0), (1, 1)])
% line_b = LineString([(1, 1), (0, 2)])
% ```
% 
% +++ {"deletable": true, "editable": true}
% 
% Let's see if they intersect
% 
% ```{code-cell} ipython3
% ---
% deletable: true
% editable: true
% jupyter:
%   outputs_hidden: false
% ---
% line_a.intersects(line_b)
% ```
% 
% +++ {"deletable": true, "editable": true}
% 
% Do they also touch?
% 
% ```{code-cell} ipython3
% ---
% deletable: true
% editable: true
% jupyter:
%   outputs_hidden: false
% ---
% line_a.touches(line_b)
% ```
% 
% +++ {"deletable": true, "editable": true}
% 
% Indeed, they do and we can see this by plotting the features together
% 
% ```{code-cell} ipython3
% ---
% deletable: true
% editable: true
% jupyter:
%   outputs_hidden: false
% ---
% # Create a MultiLineString from line_a and line_b
% multi_line = MultiLineString([line_a, line_b])
% multi_line
% ```
% 
% +++ {"deletable": true, "editable": true}
% 
% Thus, the ``line_b`` continues from the same node ( (1,1) ) where ``line_a`` ends.
% 
% However, if the lines overlap fully, they don't touch due to the spatial relationship rule, as we can see:
% 
% Check if `line_a` touches itself:
% 
% ```{code-cell} ipython3
% ---
% deletable: true
% editable: true
% jupyter:
%   outputs_hidden: false
% ---
% # Does the line touch with itself?
% line_a.touches(line_a)
% ```
% 
% +++ {"deletable": true, "editable": true}
% 
% It does not. However, it does intersect:
% 
% ```{code-cell} ipython3
% ---
% deletable: true
% editable: true
% jupyter:
%   outputs_hidden: false
% ---
% # Does the line intersect with itself?
% line_a.intersects(line_a)
% ```
% 
% ## Point in Polygon using Geopandas
% 
% Next we will do a practical example where we check which of the addresses from [the geocoding tutorial](geocoding_in_geopandas.ipynb) are located in Southern district of Helsinki. Let's start by reading a KML-file ``PKS_suuralue.kml`` that has the Polygons for districts of Helsinki Region (data openly available from [Helsinki Region Infoshare](http://www.hri.fi/fi/dataset/paakaupunkiseudun-aluejakokartat).
% 
% Let's start by reading the addresses from the Shapefile that we saved earlier.
% 
% ```{code-cell} ipython3
% :deletable: true
% :editable: true
% 
% import geopandas as gpd
% 
% fp = "data/addresses.shp"
% data = gpd.read_file(fp)
% 
% data.head()
% ```
% 
% +++ {"deletable": true, "editable": true}
% 
% 
% ### Reading KML-files in Geopandas
% 
% It is possible to read the data from KML-files with GeoPandas in a similar manner as Shapefiles. However, we need to first, enable the KML-driver which is not enabled by default (because KML-files can contain unsupported data structures, nested folders etc., hence be careful when reading KML-files). Supported drivers are managed with [`fiona.supported_drivers`](https://github.com/Toblerity/Fiona/blob/master/fiona/drvsupport.py), which is integrated in geopandas. Let's first check which formats are currently supported:
% 
% ```{code-cell} ipython3
% import geopandas as gpd
% gpd.io.file.fiona.drvsupport.supported_drivers
% ```
% 
% - Let's enable the read and write functionalities for KML-driver by passing ``'rw'`` to whitelist of fiona's supported drivers:
% 
% ```{code-cell} ipython3
% :deletable: true
% :editable: true
% 
% gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
% ```
% 
% Let's check again the supported drivers:
% 
% ```{code-cell} ipython3
% gpd.io.file.fiona.drvsupport.supported_drivers
% ```
% 
% +++ {"deletable": true, "editable": true}
% 
% Now we should be able to read a KML file using the geopandas [read_file()](http://geopandas.org/reference/geopandas.read_file.html#geopandas.read_file) function.
% 
% - Let's read district polygons from a KML -file that is located in the data-folder:
% 
% ```{code-cell} ipython3
% :deletable: true
% :editable: true
% 
% # Filepath to KML file
% fp = "data/PKS_suuralue.kml"
% polys = gpd.read_file(fp, driver='KML')
% ```
% 
% ```{code-cell} ipython3
% #Check the data
% print(f"Number of rows: {len(polys)}")
% polys.head(11)
% ```
% 
% Nice, now we can see that we have 23 districts in our area. 
% Let's quickly plot the geometries to see how the layer looks like: 
% 
% ```{code-cell} ipython3
% polys.plot()
% ```
% 
% +++ {"deletable": true, "editable": true}
% 
% We are interested in an area that is called ``Eteläinen`` (*'Southern'* in English).
% 
% Let's select the ``Eteläinen`` district and see where it is located on a map:
% 
% ```{code-cell} ipython3
% # Select data 
% southern = polys.loc[polys['Name']=='Eteläinen']
% ```
% 
% ```{code-cell} ipython3
% # Reset index for the selection
% southern.reset_index(drop=True, inplace=True)
% ```
% 
% ```{code-cell} ipython3
% # Check the selction
% southern.head()
% ```
% 
% - Let's create a map which shows the location of the selected district, and let's also plot the geocoded address points on top of the map:
% 
% ```{code-cell} ipython3
% :deletable: true
% :editable: true
% 
% import matplotlib.pyplot as plt
% 
% # Create a figure with one subplot
% fig, ax = plt.subplots()
% 
% # Plot polygons
% polys.plot(ax=ax, facecolor='gray')
% southern.plot(ax=ax, facecolor='red')
% 
% # Plot points
% data.plot(ax=ax, color='blue', markersize=5)
% 
% plt.tight_layout()
% ```
% 
% +++ {"deletable": true, "editable": true}
% 
% Okey, so we can see that, indeed, certain points are within the selected red Polygon.
% 
% Let's find out which one of them are located within the Polygon. Hence, we are conducting a **Point in Polygon query**.
% 
% First, let's check that we have  `shapely.speedups` enabled. This module makes some of the spatial queries running faster (starting from Shapely version 1.6.0 Shapely speedups are enabled by default):
% 
% ```{code-cell} ipython3
% :deletable: true
% :editable: true
% 
% #import shapely.speedups
% from shapely import speedups
% speedups.enabled
% 
% # If false, run this line:
% #shapely.speedups.enable()
% ```
% 
% +++ {"deletable": true, "editable": true}
% 
% - Let's check which Points are within the ``southern`` Polygon. Notice, that here we check if the Points are ``within`` the **geometry**
%   of the ``southern`` GeoDataFrame. 
% - We use the ``.at[0, 'geometry']`` to parse the actual Polygon geometry object from the GeoDataFrame.
% 
% ```{code-cell} ipython3
% :deletable: true
% :editable: true
% 
% pip_mask = data.within(southern.at[0, 'geometry'])
% print(pip_mask)
% ```
% 
% +++ {"deletable": true, "editable": true}
% 
% As we can see, we now have an array of boolean values for each row, where the result is ``True``
% if Point was inside the Polygon, and ``False`` if it was not.
% 
% We can now use this mask array to select the Points that are inside the Polygon. Selecting data with this kind of mask array (of boolean values) is easy by passing the array inside the ``loc`` indexer:
% 
% ```{code-cell} ipython3
% :deletable: true
% :editable: true
% 
% pip_data = data.loc[pip_mask]
% pip_data
% ```
% 
% +++ {"deletable": true, "editable": true}
% 
% Let's finally confirm that our Point in Polygon query worked as it should by plotting the points that are within the southern district:
% 
% ```{code-cell} ipython3
% :deletable: true
% :editable: true
% 
% # Create a figure with one subplot
% fig, ax = plt.subplots()
% 
% # Plot polygons
% polys.plot(ax=ax, facecolor='gray')
% southern.plot(ax=ax, facecolor='red')
% 
% # Plot points
% pip_data.plot(ax=ax, color='gold', markersize=2)
% 
% plt.tight_layout()
% ```
% 
% +++ {"deletable": true, "editable": true}
% 
% Perfect! Now we only have the (golden) points that, indeed, are inside the red Polygon which is exactly what we wanted!
