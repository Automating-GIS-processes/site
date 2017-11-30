Advanced plotting with Bokeh
----------------------------

In this part we see how it is possible to visualize any kind of geometries (normal geometries + Multi-geometries)
in Bokeh and add a legend into the map which is one of the key elements of a good map.

- Let's import the modules and functions that we need

.. ipython:: python

    from bokeh.palettes import YlOrRd as palette  #Spectral6 as palette
    from bokeh.plotting import figure, save
    from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper
    from bokeh.palettes import RdYlGn10 as palette
    import geopandas as gpd
    import pysal as ps
    import numpy as np

- Let's use three different layers to produce the map. One of the files (``road.shp``) is containing MultiLineString
objects. Here we learn how to deal with such geometric objects when plotting bokeh maps.

.. code:: python

    # Filepaths
    fp = r"/home/geo/data/TravelTimes_to_5975375_RailwayStation.shp"
    roads_fp = r"/home/geo/data/roads.shp"
    metro_fp = r"/home/geo/data/metro.shp"

.. ipython:: python
   :suppress:

    roads_fp = os.path.join(os.path.abspath('data'), "roads.shp")
    fp = os.path.join(os.path.abspath('data'), "TravelTimes_to_5975375_RailwayStation.shp")
    metro_fp = os.path.abspath('data'), "metro.shp")

- Read the data with Geopandas.

.. ipython:: python

    data = gpd.read_file(fp)
    roads = gpd.read_file(roads_fp)
    metro = gpd.read_file(metro_fp)

- Ensure that the CRS is the same than in the all layers

.. ipython:: python

    data['geometry'] = data['geometry'].to_crs(epsg=3067)
    roads['geometry'] = roads['geometry'].to_crs(epsg=3067)
    metro['geometry'] = metro['geometry'].to_crs(epsg=3067)

Next, let's create a set of functions that are used for getting the x and y coordinates of the geometries.
Shapefiles etc. can often have Multi-geometries (MultiLineStrings etc.), thus we need to handle those as well which makes things slightly more complicated.

- It is always a good practice to slice your functions into small pieces which is what we have done here:

.. code:: python

    def getXYCoords(geometry, coord_type):
        """ Returns either x or y coordinates from  geometry coordinate sequence. Used with LineString and Polygon geometries."""
        if coord_type == 'x':
            return geometry.coords.xy[0]
        elif coord_type == 'y':
            return geometry.coords.xy[1]

    def getPolyCoords(geometry, coord_type):
        """ Returns Coordinates of Polygon using the Exterior of the Polygon."""
        ext = geometry.exterior
        return getXYCoords(ext, coord_type)

    def getLineCoords(geometry, coord_type):
        """ Returns Coordinates of Linestring object."""
        return getXYCoords(geometry, coord_type)

    def getPointCoords(geometry, coord_type):
        """ Returns Coordinates of Point object."""
        if coord_type == 'x':
            return geometry.x
        elif coord_type == 'y':
            return geometry.y

    def multiGeomHandler(multi_geometry, coord_type, geom_type):
        """
        Function for handling multi-geometries. Can be MultiPoint, MultiLineString or MultiPolygon.
        Returns a list of coordinates where all parts of Multi-geometries are merged into a single list.
        Individual geometries are separated with np.nan which is how Bokeh wants them.
        # Bokeh documentation regarding the Multi-geometry issues can be found here (it is an open issue)
        # https://github.com/bokeh/bokeh/issues/2321
        """

        for i, part in enumerate(multi_geometry):
            # On the first part of the Multi-geometry initialize the coord_array (np.array)
            if i == 0:
                if geom_type == "MultiPoint":
                    coord_arrays = np.append(getPointCoords(part, coord_type), np.nan)
                elif geom_type == "MultiLineString":
                    coord_arrays = np.append(getLineCoords(part, coord_type), np.nan)
                elif geom_type == "MultiPolygon":
                    coord_arrays = np.append(getPolyCoords(part, coord_type), np.nan)
            else:
                if geom_type == "MultiPoint":
                    coord_arrays = np.concatenate([coord_arrays, np.append(getPointCoords(part, coord_type), np.nan)])
                elif geom_type == "MultiLineString":
                    coord_arrays = np.concatenate([coord_arrays, np.append(getLineCoords(part, coord_type), np.nan)])
                elif geom_type == "MultiPolygon":
                    coord_arrays = np.concatenate([coord_arrays, np.append(getPolyCoords(part, coord_type), np.nan)])

        # Return the coordinates
        return coord_arrays


    def getCoords(row, geom_col, coord_type):
        """
        Returns coordinates ('x' or 'y') of a geometry (Point, LineString or Polygon) as a list (if geometry is LineString or Polygon).
        Can handle also MultiGeometries.
        """
        # Get geometry
        geom = row[geom_col]

        # Check the geometry type
        gtype = geom.geom_type

        # "Normal" geometries
        # -------------------

        if gtype == "Point":
            return getPointCoords(geom, coord_type)
        elif gtype == "LineString":
            return list( getLineCoords(geom, coord_type) )
        elif gtype == "Polygon":
            return list( getPolyCoords(geom, coord_type) )

        # Multi geometries
        # ----------------

        else:
            return list( multiGeomHandler(geom, coord_type, gtype) )

.. ipython:: python
   :suppress:

    def getXYCoords(geometry, coord_type):
        if coord_type == 'x':
            return geometry.coords.xy[0]
        elif coord_type == 'y':
            return geometry.coords.xy[1]

.. ipython:: python
   :suppress:

    def getPolyCoords(geometry, coord_type):
        ext = geometry.exterior
        return getXYCoords(ext, coord_type)

.. ipython:: python
   :suppress:

    def getLineCoords(geometry, coord_type):
        return getXYCoords(geometry, coord_type)

.. ipython:: python
   :suppress:

    def getPointCoords(geometry, coord_type):
        if coord_type == 'x':
            return geometry.x
        elif coord_type == 'y':
            return geometry.y

.. ipython:: python
   :suppress:

    def multiGeomHandler(multi_geometry, coord_type, geom_type):
        for i, part in enumerate(multi_geometry):
            if i == 0:
                if geom_type == "MultiPoint":
                    coord_arrays = np.append(getPointCoords(part, coord_type), np.nan)
                elif geom_type == "MultiLineString":
                    coord_arrays = np.append(getLineCoords(part, coord_type), np.nan)
                elif geom_type == "MultiPolygon":
                    coord_arrays = np.append(getPolyCoords(part, coord_type), np.nan)
            else:
                if geom_type == "MultiPoint":
                    coord_arrays = np.concatenate([coord_arrays, np.append(getPointCoords(part, coord_type), np.nan)])
                elif geom_type == "MultiLineString":
                    coord_arrays = np.concatenate([coord_arrays, np.append(getLineCoords(part, coord_type), np.nan)])
                elif geom_type == "MultiPolygon":
                    coord_arrays = np.concatenate([coord_arrays, np.append(getPolyCoords(part, coord_type), np.nan)])
        return coord_arrays

.. ipython:: python
   :suppress:

    def getCoords(row, geom_col, coord_type):
        geom = row[geom_col]
        gtype = geom.geom_type
        if gtype == "Point":
            return getPointCoords(geom, coord_type)
        elif gtype == "LineString":
            return list( getLineCoords(geom, coord_type) )
        elif gtype == "Polygon":
            return list( getPolyCoords(geom, coord_type) )
        else:
            return list( multiGeomHandler(geom, coord_type, gtype) )

Now we can apply our functions and calculate the x and y coordinates of any kind of geometry by using the same function, i.e. getCoords().

- Calculate the x and y coordinates of the grid.

.. ipython:: python

    data['x'] = data.apply(getCoords, geom_col="geometry", coord_type="x", axis=1)
    data['y'] = data.apply(getCoords, geom_col="geometry", coord_type="y", axis=1)

- Calculate the x and y coordinates of the roads (these contain MultiLineStrings).

.. ipython:: python

    roads['x'] = roads.apply(getCoords, geom_col="geometry", coord_type="x", axis=1)
    roads['y'] = roads.apply(getCoords, geom_col="geometry", coord_type="y", axis=1)

- Calculate the x and y coordinates of metro.

.. ipython:: python

    metro['x'] = metro.apply(getCoords, geom_col="geometry", coord_type="x", axis=1)
    metro['y'] = metro.apply(getCoords, geom_col="geometry", coord_type="y", axis=1)

Next, we need to classify the travel time values into 5 minute intervals using Pysal's user defined classifier. We also create legend labels for the classes.

- First, we need to replace No Data values (-1) with large number (999) so that those values end up in the last class.

.. ipython:: python

    data = data.replace(-1, 999)

Next, we want to classify the travel times with 5 minute intervals until 200 minutes.

- Let's create a list of values where minumum value is 5, maximum value is 200 and step is 5.

.. ipython:: python

    breaks = [x for x in range(5, 200, 5)]

- Now we can create a pysal ``User_Defined`` classifier and classify our travel time values.

.. ipython:: python

    classifier = ps.User_Defined.make(bins=breaks)
    pt_classif = data[['pt_r_tt']].apply(classifier)
    car_classif = data[['car_r_t']].apply(classifier)

- Rename the columns of our classified columns.

.. ipython:: python

    pt_classif.columns = ['pt_r_tt_ud']
    car_classif.columns = ['car_r_t_ud']

- Join the classes back to the main data.

.. ipython:: python

    data = data.join(pt_classif)
    data = data.join(car_classif)

- Create names for the legend (until 60 minutes). The following will produce: ``["0-5", "5-10", "10-15", ... , "60 <"]``.

.. ipython:: python

    upper_limit = 60
    step = 5
    names = ["%s-%s " % (x-5, x) for x in range(step, upper_limit, step)]

- Add legend label for over 60.

.. ipython:: python

    names.append("%s <" % upper_limit)

- Assign legend names for the classes.

.. ipython:: python

    data['label_pt'] = None
    data['label_car'] = None

- Update rows with the class-names.

.. ipython:: python

    for i in range(len(names)):
        data.loc[data['pt_r_tt_ud'] == i, 'label_pt'] = names[i]
        data.loc[data['car_r_t_ud'] == i, 'label_car'] = names[i]

- Update all cells that didn't get any value with ``"60 <"``

.. ipython:: python

    data['label_pt'] = data['label_pt'].fillna("%s <" % upper_limit)
    data['label_car'] = data['label_car'].fillna("%s <" % upper_limit)

- Finally, we can visualize our layers with Bokeh, add a legend for travel times and add HoverTools for Destination Point and the grid values (travel times).

.. code:: python

   # Select only necessary columns for our plotting to keep the amount of data minumum
   df = data[['x', 'y', 'pt_r_tt_ud', 'pt_r_tt', 'car_r_t', 'from_id', 'label_pt']]
   dfsource = ColumnDataSource(data=df)

   # Include only coordinates from roads (exclude 'geometry' column)
   rdf = roads[['x', 'y']]
   rdfsource = ColumnDataSource(data=rdf)

   # Include only coordinates from metro (exclude 'geometry' column)
   mdf = metro[['x','y']]
   mdfsource = ColumnDataSource(data=mdf)

   # Specify the tools that we want to use
   TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

   # Flip the colors in color palette
   palette.reverse()
   color_mapper = LogColorMapper(palette=palette)

   p = figure(title="Travel times to Helsinki city center by public transportation", tools=TOOLS,
              plot_width=650, plot_height=500, active_scroll = "wheel_zoom" )

   # Do not add grid line
   p.grid.grid_line_color = None

   # Add polygon grid and a legend for it
   grid = p.patches('x', 'y', source=dfsource, name="grid",
            fill_color={'field': 'pt_r_tt_ud', 'transform': color_mapper},
            fill_alpha=1.0, line_color="black", line_width=0.03, legend="label_pt")

   # Add roads
   r = p.multi_line('x', 'y', source=rdfsource, color="grey")

   # Add metro
   m = p.multi_line('x', 'y', source=mdfsource, color="red")

   # Modify legend location
   p.legend.location = "top_right"
   p.legend.orientation = "vertical"

   # Insert a circle on top of the Central Railway Station (coords in EurefFIN-TM35FIN)
   station_x = 385752.214
   station_y =  6672143.803
   circle = p.circle(x=[station_x], y=[station_y], name="point", size=6, color="yellow")

   # Add two separate hover tools for the data
   phover = HoverTool(renderers=[circle])
   phover.tooltips=[("Destination", "Railway Station")]

   ghover = HoverTool(renderers=[grid])
   ghover.tooltips=[("YKR-ID", "@from_id"),
                   ("PT time", "@pt_r_tt"),
                   ("Car time", "@car_r_t"),
                  ]

   p.add_tools(ghover)
   p.add_tools(phover)

   # Output filepath to HTML
   output_file = r"/home/geo/accessibility_map_Helsinki.html"

   # Save the map
   save(p, output_file);

