Static maps
===========

Over the course of the last weeks, we have already become familiar with
plotting basic static maps using
```geopandas.GeoDataFrame.plot()`` <http://geopandas.org/mapping.html>`__,
for instance in lessons `2 <../lesson-2/geopandas-an-introduction>`__,
`3 <../lesson-3/spatial-join>`__, and
`4 <../lesson-4/reclassifying-data>`__. We also learned that
``geopandas.GeoDataFrame.plot()`` uses the ``matplotlib.pyplot``
library, and that `most of its arguments and options are accepted by
geopandas <https://matplotlib.org/stable/api/pyplot_summary.html>`__.

To refresh our memory about the basics of plotting maps, let’s create a
static accessibility map of the Helsinki metropolitan area, that also
shows roads and metro lines (three layers, overlaid onto each other).
Remember that the input data sets need to be in the same coordinate
system!

Data
----

We will use three different data sets: - the travel time to the Helsinki
railway station we used in `lesson
4 <../lesson-4/reclassifying-data>`__, which is in
``DATA_DIRECTORY / "helsinki_region_travel_times_to_railway_station"``,
- the Helsinki Metro network, available via WFS from the city’s map
services, and - a simplified network of the most important roads in the
metropolitan region, also available via WFS from the same endpoint.

.. code:: ipython3

    import pathlib
    NOTEBOOK_PATH = pathlib.Path().resolve()
    DATA_DIRECTORY = NOTEBOOK_PATH / "data"

.. code:: ipython3

    import geopandas
    import numpy
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    
    accessibility_grid = geopandas.read_file(
        DATA_DIRECTORY
        / "helsinki_region_travel_times_to_railway_station"
        / "helsinki_region_travel_times_to_railway_station.gpkg"
    )
    accessibility_grid["pt_r_t"] = accessibility_grid["pt_r_t"].replace(-1, numpy.nan)
    
    WFS_BASE_URL = (
        "https://kartta.hel.fi/ws/geoserver/avoindata/wfs"
        "?service=wfs"
        "&version=2.0.0"
        "&request=GetFeature"
        "&srsName=EPSG:3879"
        "&typeName={layer:s}"
    )
    
    metro = (
        geopandas.read_file(
            WFS_BASE_URL.format(layer="avoindata:Seutukartta_liikenne_metro_rata")
        )
        .set_crs("EPSG:3879")
    )
    roads = (
        geopandas.read_file(
            WFS_BASE_URL.format(layer="avoindata:Seutukartta_liikenne_paatiet")
        )
        .set_crs("EPSG:3879")
    )

   **Attention: Coordinate Reference Systems**

   Remember that different geo-data frames need to be in the same
   coordinate system before plotting them in the same map.
   ``geopandas.GeoDataFrame.plot()`` does not reproject data
   automatically.

   You can always check it with a simple ``assert`` statement.

.. code:: ipython3

    assert accessibility_grid.crs == metro.crs == roads.crs, "Input data sets’ CRS differs"


::


    ---------------------------------------------------------------------------

    AssertionError                            Traceback (most recent call last)

    Cell In[3], line 1
    ----> 1 assert accessibility_grid.crs == metro.crs == roads.crs, "Input data sets’ CRS differs"


    AssertionError: Input data sets’ CRS differs


If multiple data sets do not share a common CRS, first, figure out which
CRS they have assigned (if any!), then transform the data into a common
reference system:

.. code:: ipython3

    print(accessibility_grid.crs)


.. parsed-literal::

    EPSG:3067


.. code:: ipython3

    print(metro.crs)


.. parsed-literal::

    EPSG:3879


.. code:: ipython3

    print(roads.crs)


.. parsed-literal::

    EPSG:3879


.. code:: ipython3

    roads = roads.to_crs(accessibility_grid.crs)
    metro = metro.to_crs(accessibility_grid.crs)

.. code:: ipython3

    assert accessibility_grid.crs == metro.crs == roads.crs, "Input data sets’ CRS differs"

Plotting a multi-layer map
--------------------------

   **Hint: Check Your Understanding**

   Complete the next steps at your own pace (clear out the code cells
   first). Make sure to revisit previous lessons if you feel unsure how
   to complete a task.

   -  Visualize a multi-layer map using the
      ``geopandas.GeoDataFrame.plot()`` method;
   -  First, plot the accessibility grid using a ‘quantiles’
      classification scheme;
   -  Then, add roads network and metro lines in the same plot (remember
      the ``ax`` parameter).

Remember the following options that can be passed to ``plot()``: - style
the polygon layer: - define a classification scheme using the ``scheme``
parameter - `change the colour map using
``cmap`` <https://matplotlib.org/stable/tutorials/colors/colormaps.html>`__
- control the layer’s transparency the ``alpha`` parameter (``0`` is
fully transparent, ``1`` fully opaque) - style the line layers: - adjust
`the line colour <https://matplotlib.org/stable/api/colors_api.html>`__
using the ``color`` parameter - change the ``linewidth``, as needed

The layers have different extents (``roads`` covers a much larger area).
You can use the axes’ (``ax``) methods ``set_xlim()`` and ``set_ylim()``
to set the horizontal and vertical extents of the map (e.g., to a
geo-data frame’s ``total_bounds``).

.. code:: ipython3

    import matplotlib.pyplot as plt
    ax = accessibility_grid.plot(
        figsize=(12, 8),
    
        column="pt_r_t",
        scheme="quantiles",
        cmap="Spectral",
        linewidth=0,
        alpha=0.8
    )
    
    metro.plot(
        ax=ax,
        color="orange",
        linewidth=2.5
    )
    
    roads.plot(
        ax=ax,
        color="grey",
        linewidth=0.8
    )
    
    minx, miny, maxx, maxy = accessibility_grid.total_bounds
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    
    plt.savefig('maps/accessibility_plot.png')  # Save the figure as an image file
    plt.close()  # Close the plot to free up memory



Adding a legend
---------------

To plot a legend for a map, add the ``legend=True`` parameter.

For figures without a classification ``scheme``, the legend consists of
a colour gradient bar. The legend is an instance of
```matplotlib.pyplot.colorbar.Colorbar`` <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.colorbar.html>`__,
and all arguments defined in ``legend_kwds`` are passed through to it.
See below how to use the ``label`` property to set the *legend title*:

.. code:: ipython3

    ax = accessibility_grid.plot(
        figsize=(12, 8),
    
        column="pt_r_t",
        cmap="Spectral",
        linewidth=0,
        alpha=0.8,
    
        legend=True,
        legend_kwds={"label": "Travel time (min)"}
    )
    plt.savefig('maps/accessibility_plot_leg.png')  # Save the figure as an image file
    plt.close()  # Close the plot to free up memory



   **Hint: Set Other ``Colorbar`` Parameters**

   Check out ```matplotlib.pyplot.colorbar.Colorbar``\ ’s
   documentation <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.colorbar.html>`__
   and experiment with other parameters! Anything you add to the
   ``legend_kwds`` dictionary will be passed to the color bar.

--------------

For figures that use a classification ``scheme``, on the other hand,
``plot()`` creates a
```matplotlib.legend.Legend`` <https://matplotlib.org/stable/api/legend_api.html#matplotlib.legend.Legend>`__.
Again, ``legend_kwds`` are passed through, but the parameters are
slightly different: for instance, use ``title`` instead of ``label`` to
set the legend title:

.. code:: ipython3

    accessibility_grid.plot(
        figsize=(12, 8),
    
        column="pt_r_t",
        scheme="quantiles",
        cmap="Spectral",
        linewidth=0,
        alpha=0.8,
    
        legend=True,
        legend_kwds={"title": "Travel time (min)"}
    )
    plt.savefig('maps/accessibility_plot_leg2.png')  # Save the figure as an image file
    plt.close()  # Close the plot to free up memory

   **Hint: Set Other ``Legend`` Parameters**

   Check out ```matplotlib.pyplot.legend.Legend``\ ’s
   documentation <https://matplotlib.org/stable/api/legend_api.html#matplotlib.legend.Legend>`__,
   and experiment with other parameters! Anything you add to the
   ``legend_kwds`` dictionary will be passed to the legend.

   What ``legend_kwds`` keyword would spread the legend onto two
   columns?

Adding a base map
-----------------

For better orientation, it is often helpful to add a base map to a map
plot. A base map, for instance, from map providers such as
`OpenStreetMap <https://osm.org/>`__ or
`Stamen <https://maps.stamen.com/>`__, adds streets, place names, and
other contextual information.

The Python package `contextily <https://contextily.readthedocs.io/>`__
takes care of downloading the necessary map tiles and rendering them in
a geopandas plot.

   **Caution: Web Mercator**

   Map tiles from online map providers are typically in `Web Mercator
   projection
   (EPSG:3857) <http://spatialreference.org/ref/sr-org/epsg3857-wgs84-web-mercator-auxiliary-sphere/>`__.
   It is generally advisable to transform all other layers to
   ``EPSG:3857``, too.

.. code:: ipython3

    accessibility_grid = accessibility_grid.to_crs("EPSG:3857")
    metro = metro.to_crs("EPSG:3857")
    roads = roads.to_crs("EPSG:3857")

To add a base map to an existing plot, use the
```contextily.add_basemap()`` <https://contextily.readthedocs.io/en/latest/intro_guide.html>`__
function, and supply the plot’s ``ax`` object obtained in an earlier
step.

.. code:: ipython3

    import contextily
    
    ax = accessibility_grid.plot(
        figsize=(12, 8),
    
        column="pt_r_t",
        scheme="quantiles",
        cmap="Spectral",
        linewidth=0,
        alpha=0.8,
    
        legend=True,
        legend_kwds={"title": "Travel time (min)"}
    )
    contextily.add_basemap(ax, source=contextily.providers.OpenStreetMap.Mapnik)



.. image:: static-maps-2_files/static-maps-2_22_0.png


`There are many other online maps to choose
from <https://contextily.readthedocs.io/en/latest/intro_guide.html#Providers>`__.
Any of the other ``contextily.providers`` (see link above) can be passed
as a ``source`` to ``add_basemap()``. You can get a list of available
providers:

.. code:: ipython3

    contextily.providers




.. raw:: html

    
            <div>
            <style>
    /* CSS stylesheet for displaying xyzservices objects in Jupyter.*/
    .xyz-wrap {
        --xyz-border-color: var(--jp-border-color2, #ddd);
        --xyz-font-color2: var(--jp-content-font-color2, rgba(128, 128, 128, 1));
        --xyz-background-color-white: var(--jp-layout-color1, white);
        --xyz-background-color: var(--jp-layout-color2, rgba(128, 128, 128, 0.1));
    }
    
    html[theme=dark] .xyz-wrap,
    body.vscode-dark .xyz-wrap,
    body.vscode-high-contrast .xyz-wrap {
        --xyz-border-color: #222;
        --xyz-font-color2: rgba(255, 255, 255, 0.54);
        --xyz-background-color-white: rgba(255, 255, 255, 1);
        --xyz-background-color: rgba(255, 255, 255, 0.05);
    
    }
    
    .xyz-header {
        padding-top: 6px;
        padding-bottom: 6px;
        margin-bottom: 4px;
        border-bottom: solid 1px var(--xyz-border-color);
    }
    
    .xyz-header>div {
        display: inline;
        margin-top: 0;
        margin-bottom: 0;
    }
    
    .xyz-obj,
    .xyz-name {
        margin-left: 2px;
        margin-right: 10px;
    }
    
    .xyz-obj {
        color: var(--xyz-font-color2);
    }
    
    .xyz-attrs {
        grid-column: 1 / -1;
    }
    
    dl.xyz-attrs {
        padding: 0 5px 0 5px;
        margin: 0;
        display: grid;
        grid-template-columns: 135px auto;
        background-color: var(--xyz-background-color);
    }
    
    .xyz-attrs dt,
    dd {
        padding: 0;
        margin: 0;
        float: left;
        padding-right: 10px;
        width: auto;
    }
    
    .xyz-attrs dt {
        font-weight: normal;
        grid-column: 1;
    }
    
    .xyz-attrs dd {
        grid-column: 2;
        white-space: pre-wrap;
        word-break: break-all;
    }
    
    .xyz-details ul>li>label>span {
        color: var(--xyz-font-color2);
        padding-left: 10px;
    }
    
    .xyz-inside {
        display: none;
    }
    
    .xyz-checkbox:checked~.xyz-inside {
        display: contents;
    }
    
    .xyz-collapsible li>input {
        display: none;
    }
    
    .xyz-collapsible>li>label {
        cursor: pointer;
    }
    
    .xyz-collapsible>li>label:hover {
        color: var(--xyz-font-color2);
    }
    
    ul.xyz-collapsible {
        list-style: none!important;
        padding-left: 20px!important;
    }
    
    .xyz-checkbox+label:before {
        content: '►';
        font-size: 11px;
    }
    
    .xyz-checkbox:checked+label:before {
        content: '▼';
    }
    
    .xyz-wrap {
        margin-bottom: 10px;
    }
    </style>
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">39 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="5fb8dfbb-573c-40a2-90b2-f9e9f084972b" class="xyz-checkbox"/>
                    <label for="5fb8dfbb-573c-40a2-90b2-f9e9f084972b">OpenStreetMap <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">7 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="e5fe9ee0-7b18-4e65-b09f-acaf015f9bf6" class="xyz-checkbox"/>
                    <label for="e5fe9ee0-7b18-4e65-b09f-acaf015f9bf6">Mapnik <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenStreetMap.Mapnik</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tile.openstreetmap.org/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="980b624f-79ed-492d-a808-d9b72157e3f8" class="xyz-checkbox"/>
                    <label for="980b624f-79ed-492d-a808-d9b72157e3f8">DE <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenStreetMap.DE</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tile.openstreetmap.de/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="14b17fb9-9596-4fb4-a6f8-75247a14c4d4" class="xyz-checkbox"/>
                    <label for="14b17fb9-9596-4fb4-a6f8-75247a14c4d4">CH <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenStreetMap.CH</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tile.osm.ch/switzerland/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors</dd><dt><span>bounds</span></dt><dd>[[45, 5], [48, 11]]</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2ea7389e-fdad-41fd-b392-27066a9dccad" class="xyz-checkbox"/>
                    <label for="2ea7389e-fdad-41fd-b392-27066a9dccad">France <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenStreetMap.France</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>&copy; OpenStreetMap France | &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap France | (C) OpenStreetMap contributors</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="56009e22-dc5a-4bd8-9d3d-61ae285cf8be" class="xyz-checkbox"/>
                    <label for="56009e22-dc5a-4bd8-9d3d-61ae285cf8be">HOT <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenStreetMap.HOT</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a></dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors, Tiles style by Humanitarian OpenStreetMap Team hosted by OpenStreetMap France</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="d9fd3932-405a-412a-be5e-bb64a582113a" class="xyz-checkbox"/>
                    <label for="d9fd3932-405a-412a-be5e-bb64a582113a">BZH <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenStreetMap.BZH</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tile.openstreetmap.bzh/br/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles courtesy of <a href="http://www.openstreetmap.bzh/" target="_blank">Breton OpenStreetMap Team</a></dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors, Tiles courtesy of Breton OpenStreetMap Team</dd><dt><span>bounds</span></dt><dd>[[46.2, -5.5], [50, 0.7]]</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3c5a3a32-db6c-44bd-84ed-4e72ac3cb5e3" class="xyz-checkbox"/>
                    <label for="3c5a3a32-db6c-44bd-84ed-4e72ac3cb5e3">BlackAndWhite <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenStreetMap.BlackAndWhite</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b19d7c31-d510-4c7c-bf73-8f548746db09" class="xyz-checkbox"/>
                    <label for="b19d7c31-d510-4c7c-bf73-8f548746db09">MapTilesAPI <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">3 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="34c9a44b-bd0d-4300-b6d2-792158a3c5a2" class="xyz-checkbox"/>
                    <label for="34c9a44b-bd0d-4300-b6d2-792158a3c5a2">OSMEnglish <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTilesAPI.OSMEnglish</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://maptiles.p.rapidapi.com/{variant}/{z}/{x}/{y}.png?rapidapi-key={apikey}</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="http://www.maptilesapi.com/">MapTiles API</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) MapTiles API, (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>en/map/v1</dd><dt><span>apikey</span></dt><dd><insert your api key here></dd><dt><span>max_zoom</span></dt><dd>19</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8311074d-f1ec-44a2-86f9-35b365a26ac2" class="xyz-checkbox"/>
                    <label for="8311074d-f1ec-44a2-86f9-35b365a26ac2">OSMFrancais <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTilesAPI.OSMFrancais</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://maptiles.p.rapidapi.com/{variant}/{z}/{x}/{y}.png?rapidapi-key={apikey}</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="http://www.maptilesapi.com/">MapTiles API</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) MapTiles API, (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>fr/map/v1</dd><dt><span>apikey</span></dt><dd><insert your api key here></dd><dt><span>max_zoom</span></dt><dd>19</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f8f94f88-cdcb-45ee-9ad8-48dc1634dc9b" class="xyz-checkbox"/>
                    <label for="f8f94f88-cdcb-45ee-9ad8-48dc1634dc9b">OSMEspagnol <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTilesAPI.OSMEspagnol</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://maptiles.p.rapidapi.com/{variant}/{z}/{x}/{y}.png?rapidapi-key={apikey}</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="http://www.maptilesapi.com/">MapTiles API</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) MapTiles API, (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>es/map/v1</dd><dt><span>apikey</span></dt><dd><insert your api key here></dd><dt><span>max_zoom</span></dt><dd>19</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="34229f0e-f08c-47e5-9a4c-fd0c386ba441" class="xyz-checkbox"/>
                    <label for="34229f0e-f08c-47e5-9a4c-fd0c386ba441">OpenSeaMap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenSeaMap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png</dd><dt><span>html_attribution</span></dt><dd>Map data: &copy; <a href="http://www.openseamap.org">OpenSeaMap</a> contributors</dd><dt><span>attribution</span></dt><dd>Map data: (C) OpenSeaMap contributors</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="acffc180-1535-4b9e-b6ae-0538bb8bd813" class="xyz-checkbox"/>
                    <label for="acffc180-1535-4b9e-b6ae-0538bb8bd813">OPNVKarte <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OPNVKarte</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tileserver.memomaps.de/tilegen/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>html_attribution</span></dt><dd>Map <a href="https://memomaps.de/">memomaps.de</a> <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>Map memomaps.de CC-BY-SA, map data (C) OpenStreetMap contributors</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="458066b5-b31d-4019-8028-908eccb0928c" class="xyz-checkbox"/>
                    <label for="458066b5-b31d-4019-8028-908eccb0928c">OpenTopoMap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenTopoMap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>html_attribution</span></dt><dd>Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)</dd><dt><span>attribution</span></dt><dd>Map data: (C) OpenStreetMap contributors, SRTM | Map style: (C) OpenTopoMap (CC-BY-SA)</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="44fe9afa-fcfe-4bb8-8874-2e4899590e2b" class="xyz-checkbox"/>
                    <label for="44fe9afa-fcfe-4bb8-8874-2e4899590e2b">OpenRailwayMap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenRailwayMap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Map style: &copy; <a href="https://www.OpenRailwayMap.org">OpenRailwayMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)</dd><dt><span>attribution</span></dt><dd>Map data: (C) OpenStreetMap contributors | Map style: (C) OpenRailwayMap (CC-BY-SA)</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="1020c176-3034-41fc-8cae-9b78ebed2826" class="xyz-checkbox"/>
                    <label for="1020c176-3034-41fc-8cae-9b78ebed2826">OpenFireMap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenFireMap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://openfiremap.org/hytiles/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Map style: &copy; <a href="http://www.openfiremap.org">OpenFireMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)</dd><dt><span>attribution</span></dt><dd>Map data: (C) OpenStreetMap contributors | Map style: (C) OpenFireMap (CC-BY-SA)</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0c0ef933-601a-4344-8c22-6a1de0640bef" class="xyz-checkbox"/>
                    <label for="0c0ef933-601a-4344-8c22-6a1de0640bef">SafeCast <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">SafeCast</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://s3.amazonaws.com/te512.safecast.org/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>html_attribution</span></dt><dd>Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Map style: &copy; <a href="https://blog.safecast.org/about/">SafeCast</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)</dd><dt><span>attribution</span></dt><dd>Map data: (C) OpenStreetMap contributors | Map style: (C) SafeCast (CC-BY-SA)</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="080f6db0-45b7-4c98-a132-cc24cf3f5f8c" class="xyz-checkbox"/>
                    <label for="080f6db0-45b7-4c98-a132-cc24cf3f5f8c">Stadia <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">14 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="e6ad118e-84dd-4c07-997a-4468491f2885" class="xyz-checkbox"/>
                    <label for="e6ad118e-84dd-4c07-997a-4468491f2885">AlidadeSmooth <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Stadia.AlidadeSmooth</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.stadiamaps.com/tiles/{variant}/{z}/{x}/{y}{r}.{ext}</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Stadia Maps (C) OpenMapTiles (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>alidade_smooth</dd><dt><span>ext</span></dt><dd>png</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9170d4cd-1b5e-40e9-946b-55c145ffefe8" class="xyz-checkbox"/>
                    <label for="9170d4cd-1b5e-40e9-946b-55c145ffefe8">AlidadeSmoothDark <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Stadia.AlidadeSmoothDark</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.stadiamaps.com/tiles/{variant}/{z}/{x}/{y}{r}.{ext}</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Stadia Maps (C) OpenMapTiles (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>alidade_smooth_dark</dd><dt><span>ext</span></dt><dd>png</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="41547829-9cab-43d5-8e71-53a6c201e179" class="xyz-checkbox"/>
                    <label for="41547829-9cab-43d5-8e71-53a6c201e179">OSMBright <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Stadia.OSMBright</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.stadiamaps.com/tiles/{variant}/{z}/{x}/{y}{r}.{ext}</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Stadia Maps (C) OpenMapTiles (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>osm_bright</dd><dt><span>ext</span></dt><dd>png</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b74eab92-e4e1-4e84-bbd2-8598f5342577" class="xyz-checkbox"/>
                    <label for="b74eab92-e4e1-4e84-bbd2-8598f5342577">Outdoors <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Stadia.Outdoors</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.stadiamaps.com/tiles/{variant}/{z}/{x}/{y}{r}.{ext}</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Stadia Maps (C) OpenMapTiles (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>outdoors</dd><dt><span>ext</span></dt><dd>png</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5e757d23-f4a9-49cd-a40a-425df85ae6d8" class="xyz-checkbox"/>
                    <label for="5e757d23-f4a9-49cd-a40a-425df85ae6d8">StamenToner <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Stadia.StamenToner</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.stadiamaps.com/tiles/{variant}/{z}/{x}/{y}{r}.{ext}</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Stadia Maps (C) Stamen Design (C) OpenMapTiles (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>stamen_toner</dd><dt><span>ext</span></dt><dd>png</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ee7ef962-b2f8-4987-bb52-4e408e8655df" class="xyz-checkbox"/>
                    <label for="ee7ef962-b2f8-4987-bb52-4e408e8655df">StamenTonerBackground <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Stadia.StamenTonerBackground</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.stadiamaps.com/tiles/{variant}/{z}/{x}/{y}{r}.{ext}</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Stadia Maps (C) Stamen Design (C) OpenMapTiles (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>stamen_toner_background</dd><dt><span>ext</span></dt><dd>png</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0fadaa86-56c1-4ede-ac95-a0e4ec886f43" class="xyz-checkbox"/>
                    <label for="0fadaa86-56c1-4ede-ac95-a0e4ec886f43">StamenTonerLines <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Stadia.StamenTonerLines</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.stadiamaps.com/tiles/{variant}/{z}/{x}/{y}{r}.{ext}</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Stadia Maps (C) Stamen Design (C) OpenMapTiles (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>stamen_toner_lines</dd><dt><span>ext</span></dt><dd>png</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="35a2607f-9ee4-4875-8994-408ea7dd8652" class="xyz-checkbox"/>
                    <label for="35a2607f-9ee4-4875-8994-408ea7dd8652">StamenTonerLabels <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Stadia.StamenTonerLabels</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.stadiamaps.com/tiles/{variant}/{z}/{x}/{y}{r}.{ext}</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Stadia Maps (C) Stamen Design (C) OpenMapTiles (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>stamen_toner_labels</dd><dt><span>ext</span></dt><dd>png</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="39846769-aed3-411e-a528-9b3d8f4910b5" class="xyz-checkbox"/>
                    <label for="39846769-aed3-411e-a528-9b3d8f4910b5">StamenTonerLite <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Stadia.StamenTonerLite</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.stadiamaps.com/tiles/{variant}/{z}/{x}/{y}{r}.{ext}</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Stadia Maps (C) Stamen Design (C) OpenMapTiles (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>stamen_toner_lite</dd><dt><span>ext</span></dt><dd>png</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="23f277c4-9043-4f66-9235-ce148f7a1f31" class="xyz-checkbox"/>
                    <label for="23f277c4-9043-4f66-9235-ce148f7a1f31">StamenWatercolor <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Stadia.StamenWatercolor</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.stadiamaps.com/tiles/{variant}/{z}/{x}/{y}.{ext}</dd><dt><span>min_zoom</span></dt><dd>1</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Stadia Maps (C) Stamen Design (C) OpenMapTiles (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>stamen_watercolor</dd><dt><span>ext</span></dt><dd>jpg</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="866e5405-8fa7-42e9-aca7-854cbbbc6fab" class="xyz-checkbox"/>
                    <label for="866e5405-8fa7-42e9-aca7-854cbbbc6fab">StamenTerrain <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Stadia.StamenTerrain</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.stadiamaps.com/tiles/{variant}/{z}/{x}/{y}{r}.{ext}</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Stadia Maps (C) Stamen Design (C) OpenMapTiles (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>stamen_terrain</dd><dt><span>ext</span></dt><dd>png</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2a3050e2-53a4-4f41-8671-8e14b825a7e5" class="xyz-checkbox"/>
                    <label for="2a3050e2-53a4-4f41-8671-8e14b825a7e5">StamenTerrainBackground <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Stadia.StamenTerrainBackground</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.stadiamaps.com/tiles/{variant}/{z}/{x}/{y}{r}.{ext}</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Stadia Maps (C) Stamen Design (C) OpenMapTiles (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>stamen_terrain_background</dd><dt><span>ext</span></dt><dd>png</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3ce78977-354d-4db8-9506-002742f264ef" class="xyz-checkbox"/>
                    <label for="3ce78977-354d-4db8-9506-002742f264ef">StamenTerrainLabels <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Stadia.StamenTerrainLabels</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.stadiamaps.com/tiles/{variant}/{z}/{x}/{y}{r}.{ext}</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Stadia Maps (C) Stamen Design (C) OpenMapTiles (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>stamen_terrain_labels</dd><dt><span>ext</span></dt><dd>png</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="7d241d63-d33d-4024-8478-60bd2cff8327" class="xyz-checkbox"/>
                    <label for="7d241d63-d33d-4024-8478-60bd2cff8327">StamenTerrainLines <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Stadia.StamenTerrainLines</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.stadiamaps.com/tiles/{variant}/{z}/{x}/{y}{r}.{ext}</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Stadia Maps (C) Stamen Design (C) OpenMapTiles (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>stamen_terrain_lines</dd><dt><span>ext</span></dt><dd>png</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="95311cc7-f029-4bcd-84a6-aa7049743905" class="xyz-checkbox"/>
                    <label for="95311cc7-f029-4bcd-84a6-aa7049743905">Thunderforest <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">9 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="4e326133-6963-406a-9f3d-2f3c2b7d8504" class="xyz-checkbox"/>
                    <label for="4e326133-6963-406a-9f3d-2f3c2b7d8504">OpenCycleMap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Thunderforest.OpenCycleMap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.thunderforest.com/{variant}/{z}/{x}/{y}.png?apikey={apikey}</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Thunderforest, (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>cycle</dd><dt><span>apikey</span></dt><dd><insert your api key here></dd><dt><span>max_zoom</span></dt><dd>22</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2c05a179-b50a-4aac-a913-8f0c1807c996" class="xyz-checkbox"/>
                    <label for="2c05a179-b50a-4aac-a913-8f0c1807c996">Transport <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Thunderforest.Transport</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.thunderforest.com/{variant}/{z}/{x}/{y}.png?apikey={apikey}</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Thunderforest, (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>transport</dd><dt><span>apikey</span></dt><dd><insert your api key here></dd><dt><span>max_zoom</span></dt><dd>22</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4ff1e8da-d140-444a-8bbc-7077fad83cce" class="xyz-checkbox"/>
                    <label for="4ff1e8da-d140-444a-8bbc-7077fad83cce">TransportDark <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Thunderforest.TransportDark</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.thunderforest.com/{variant}/{z}/{x}/{y}.png?apikey={apikey}</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Thunderforest, (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>transport-dark</dd><dt><span>apikey</span></dt><dd><insert your api key here></dd><dt><span>max_zoom</span></dt><dd>22</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f177d173-375c-4161-a3ff-9ce56e2bcd22" class="xyz-checkbox"/>
                    <label for="f177d173-375c-4161-a3ff-9ce56e2bcd22">SpinalMap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Thunderforest.SpinalMap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.thunderforest.com/{variant}/{z}/{x}/{y}.png?apikey={apikey}</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Thunderforest, (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>spinal-map</dd><dt><span>apikey</span></dt><dd><insert your api key here></dd><dt><span>max_zoom</span></dt><dd>22</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="890296d9-9452-4064-98c2-4a15c7c7927c" class="xyz-checkbox"/>
                    <label for="890296d9-9452-4064-98c2-4a15c7c7927c">Landscape <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Thunderforest.Landscape</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.thunderforest.com/{variant}/{z}/{x}/{y}.png?apikey={apikey}</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Thunderforest, (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>landscape</dd><dt><span>apikey</span></dt><dd><insert your api key here></dd><dt><span>max_zoom</span></dt><dd>22</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="6983b896-0525-4cdb-9799-fe4e8e80ef73" class="xyz-checkbox"/>
                    <label for="6983b896-0525-4cdb-9799-fe4e8e80ef73">Outdoors <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Thunderforest.Outdoors</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.thunderforest.com/{variant}/{z}/{x}/{y}.png?apikey={apikey}</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Thunderforest, (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>outdoors</dd><dt><span>apikey</span></dt><dd><insert your api key here></dd><dt><span>max_zoom</span></dt><dd>22</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2194250c-045c-419d-ad18-c1b1ee30e2a3" class="xyz-checkbox"/>
                    <label for="2194250c-045c-419d-ad18-c1b1ee30e2a3">Pioneer <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Thunderforest.Pioneer</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.thunderforest.com/{variant}/{z}/{x}/{y}.png?apikey={apikey}</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Thunderforest, (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>pioneer</dd><dt><span>apikey</span></dt><dd><insert your api key here></dd><dt><span>max_zoom</span></dt><dd>22</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="051c185b-4953-498f-ba71-75aa634931a8" class="xyz-checkbox"/>
                    <label for="051c185b-4953-498f-ba71-75aa634931a8">MobileAtlas <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Thunderforest.MobileAtlas</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.thunderforest.com/{variant}/{z}/{x}/{y}.png?apikey={apikey}</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Thunderforest, (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>mobile-atlas</dd><dt><span>apikey</span></dt><dd><insert your api key here></dd><dt><span>max_zoom</span></dt><dd>22</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="03614aa4-3954-42d2-8ca8-49e6c3a263e2" class="xyz-checkbox"/>
                    <label for="03614aa4-3954-42d2-8ca8-49e6c3a263e2">Neighbourhood <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Thunderforest.Neighbourhood</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.thunderforest.com/{variant}/{z}/{x}/{y}.png?apikey={apikey}</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) Thunderforest, (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>neighbourhood</dd><dt><span>apikey</span></dt><dd><insert your api key here></dd><dt><span>max_zoom</span></dt><dd>22</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0795736c-bacd-4205-a755-67a289230ffb" class="xyz-checkbox"/>
                    <label for="0795736c-bacd-4205-a755-67a289230ffb">CyclOSM <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">CyclOSM</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd><a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>CyclOSM | Map data: (C) OpenStreetMap contributors</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0361a880-a544-4ed7-ae02-70820af7eefb" class="xyz-checkbox"/>
                    <label for="0361a880-a544-4ed7-ae02-70820af7eefb">Jawg <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">6 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="82b63f21-6de8-475d-9a1f-068d6b300949" class="xyz-checkbox"/>
                    <label for="82b63f21-6de8-475d-9a1f-068d6b300949">Streets <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Jawg.Streets</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.jawg.io/{variant}/{z}/{x}/{y}{r}.png?access-token={accessToken}</dd><dt><span>html_attribution</span></dt><dd><a href="http://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) **Jawg** Maps (C) OpenStreetMap contributors</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>22</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>variant</span></dt><dd>jawg-streets</dd><dt><span>accessToken</span></dt><dd><insert your access token here></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5b316c84-951e-4e69-9d25-78c2684c7271" class="xyz-checkbox"/>
                    <label for="5b316c84-951e-4e69-9d25-78c2684c7271">Terrain <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Jawg.Terrain</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.jawg.io/{variant}/{z}/{x}/{y}{r}.png?access-token={accessToken}</dd><dt><span>html_attribution</span></dt><dd><a href="http://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) **Jawg** Maps (C) OpenStreetMap contributors</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>22</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>variant</span></dt><dd>jawg-terrain</dd><dt><span>accessToken</span></dt><dd><insert your access token here></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9591fb84-65e8-4caf-ba81-408b66ee4701" class="xyz-checkbox"/>
                    <label for="9591fb84-65e8-4caf-ba81-408b66ee4701">Sunny <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Jawg.Sunny</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.jawg.io/{variant}/{z}/{x}/{y}{r}.png?access-token={accessToken}</dd><dt><span>html_attribution</span></dt><dd><a href="http://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) **Jawg** Maps (C) OpenStreetMap contributors</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>22</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>variant</span></dt><dd>jawg-sunny</dd><dt><span>accessToken</span></dt><dd><insert your access token here></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="dfd7f1f1-8b28-4dbb-a13a-212d1b4b5376" class="xyz-checkbox"/>
                    <label for="dfd7f1f1-8b28-4dbb-a13a-212d1b4b5376">Dark <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Jawg.Dark</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.jawg.io/{variant}/{z}/{x}/{y}{r}.png?access-token={accessToken}</dd><dt><span>html_attribution</span></dt><dd><a href="http://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) **Jawg** Maps (C) OpenStreetMap contributors</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>22</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>variant</span></dt><dd>jawg-dark</dd><dt><span>accessToken</span></dt><dd><insert your access token here></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2c726fe3-16f5-4c93-8f1a-6d0a2ca9b2de" class="xyz-checkbox"/>
                    <label for="2c726fe3-16f5-4c93-8f1a-6d0a2ca9b2de">Light <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Jawg.Light</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.jawg.io/{variant}/{z}/{x}/{y}{r}.png?access-token={accessToken}</dd><dt><span>html_attribution</span></dt><dd><a href="http://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) **Jawg** Maps (C) OpenStreetMap contributors</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>22</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>variant</span></dt><dd>jawg-light</dd><dt><span>accessToken</span></dt><dd><insert your access token here></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="c8afab0a-b65d-4578-be59-2be0505b8379" class="xyz-checkbox"/>
                    <label for="c8afab0a-b65d-4578-be59-2be0505b8379">Matrix <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Jawg.Matrix</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.jawg.io/{variant}/{z}/{x}/{y}{r}.png?access-token={accessToken}</dd><dt><span>html_attribution</span></dt><dd><a href="http://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) **Jawg** Maps (C) OpenStreetMap contributors</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>22</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>variant</span></dt><dd>jawg-matrix</dd><dt><span>accessToken</span></dt><dd><insert your access token here></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="76080851-eae8-4c00-b84c-aec4488360a4" class="xyz-checkbox"/>
                    <label for="76080851-eae8-4c00-b84c-aec4488360a4">MapBox <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapBox</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}{r}?access_token={accessToken}</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.mapbox.com/about/maps/" target="_blank">Mapbox</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors <a href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a></dd><dt><span>attribution</span></dt><dd>(C) Mapbox (C) OpenStreetMap contributors Improve this map</dd><dt><span>tileSize</span></dt><dd>512</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>zoomOffset</span></dt><dd>-1</dd><dt><span>id</span></dt><dd>mapbox/streets-v11</dd><dt><span>accessToken</span></dt><dd><insert your access token here></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="83740871-139d-482c-b016-8f913336d8df" class="xyz-checkbox"/>
                    <label for="83740871-139d-482c-b016-8f913336d8df">MapTiler <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">15 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="7bc9b678-b601-414e-a3b2-d74f8f4731c3" class="xyz-checkbox"/>
                    <label for="7bc9b678-b601-414e-a3b2-d74f8f4731c3">Streets <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Streets</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/maps/{variant}/{z}/{x}/{y}{r}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>streets</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>tileSize</span></dt><dd>512</dd><dt><span>zoomOffset</span></dt><dd>-1</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>21</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b8e13419-2d7b-4845-90e8-76e195f4471c" class="xyz-checkbox"/>
                    <label for="b8e13419-2d7b-4845-90e8-76e195f4471c">Basic <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Basic</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/maps/{variant}/{z}/{x}/{y}{r}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>basic</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>tileSize</span></dt><dd>512</dd><dt><span>zoomOffset</span></dt><dd>-1</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>21</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f6873af0-c377-4b0b-b037-ceb8f21bfc3f" class="xyz-checkbox"/>
                    <label for="f6873af0-c377-4b0b-b037-ceb8f21bfc3f">Bright <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Bright</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/maps/{variant}/{z}/{x}/{y}{r}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>bright</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>tileSize</span></dt><dd>512</dd><dt><span>zoomOffset</span></dt><dd>-1</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>21</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="aa1e6425-10f4-4647-ac0b-7246de9d0642" class="xyz-checkbox"/>
                    <label for="aa1e6425-10f4-4647-ac0b-7246de9d0642">Pastel <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Pastel</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/maps/{variant}/{z}/{x}/{y}{r}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>pastel</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>tileSize</span></dt><dd>512</dd><dt><span>zoomOffset</span></dt><dd>-1</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>21</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="dcef8c17-2db8-4413-9ab8-b57eadffda79" class="xyz-checkbox"/>
                    <label for="dcef8c17-2db8-4413-9ab8-b57eadffda79">Positron <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Positron</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/maps/{variant}/{z}/{x}/{y}{r}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>positron</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>tileSize</span></dt><dd>512</dd><dt><span>zoomOffset</span></dt><dd>-1</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>21</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a82da403-0753-4896-a3b5-d617b7a08e9b" class="xyz-checkbox"/>
                    <label for="a82da403-0753-4896-a3b5-d617b7a08e9b">Hybrid <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Hybrid</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/maps/{variant}/{z}/{x}/{y}{r}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>hybrid</dd><dt><span>ext</span></dt><dd>jpg</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>tileSize</span></dt><dd>512</dd><dt><span>zoomOffset</span></dt><dd>-1</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>21</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="23e818cb-e846-4430-99a2-c152ebf4f2e4" class="xyz-checkbox"/>
                    <label for="23e818cb-e846-4430-99a2-c152ebf4f2e4">Toner <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Toner</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/maps/{variant}/{z}/{x}/{y}{r}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>toner</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>tileSize</span></dt><dd>512</dd><dt><span>zoomOffset</span></dt><dd>-1</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>21</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="14c367d6-0c69-457e-9477-1b1902c54b65" class="xyz-checkbox"/>
                    <label for="14c367d6-0c69-457e-9477-1b1902c54b65">Topo <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Topo</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/maps/{variant}/{z}/{x}/{y}{r}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>topo</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>tileSize</span></dt><dd>512</dd><dt><span>zoomOffset</span></dt><dd>-1</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>21</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e49c2eee-42bd-4588-9496-127680ecc954" class="xyz-checkbox"/>
                    <label for="e49c2eee-42bd-4588-9496-127680ecc954">Voyager <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Voyager</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/maps/{variant}/{z}/{x}/{y}{r}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>voyager</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>tileSize</span></dt><dd>512</dd><dt><span>zoomOffset</span></dt><dd>-1</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>21</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="34d0a761-9e01-423b-8693-ad2a088a7f14" class="xyz-checkbox"/>
                    <label for="34d0a761-9e01-423b-8693-ad2a088a7f14">Basic4326 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Basic4326</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/maps/{variant}/{z}/{x}/{y}{r}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>basic-4326</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>tileSize</span></dt><dd>512</dd><dt><span>zoomOffset</span></dt><dd>-1</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>21</dd><dt><span>crs</span></dt><dd>EPSG:4326</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="de5a6057-e6fe-4845-9061-e091c4ccdab8" class="xyz-checkbox"/>
                    <label for="de5a6057-e6fe-4845-9061-e091c4ccdab8">Outdoor <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Outdoor</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/maps/{variant}/{z}/{x}/{y}{r}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>outdoor</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>tileSize</span></dt><dd>512</dd><dt><span>zoomOffset</span></dt><dd>-1</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>21</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cbdcf671-c05b-4c73-84ce-2dd8ff6b8242" class="xyz-checkbox"/>
                    <label for="cbdcf671-c05b-4c73-84ce-2dd8ff6b8242">Topographique <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Topographique</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/maps/{variant}/{z}/{x}/{y}{r}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>topographique</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>tileSize</span></dt><dd>512</dd><dt><span>zoomOffset</span></dt><dd>-1</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>21</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="71f86bb9-5e91-496a-85a0-c90dc0875154" class="xyz-checkbox"/>
                    <label for="71f86bb9-5e91-496a-85a0-c90dc0875154">Winter <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Winter</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/maps/{variant}/{z}/{x}/{y}{r}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>winter</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>tileSize</span></dt><dd>512</dd><dt><span>zoomOffset</span></dt><dd>-1</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>21</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="193e9c4a-d0aa-4326-b447-095c5a1acd76" class="xyz-checkbox"/>
                    <label for="193e9c4a-d0aa-4326-b447-095c5a1acd76">Satellite <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Satellite</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/tiles/{variant}/{z}/{x}/{y}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>satellite-v2</dd><dt><span>ext</span></dt><dd>jpg</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>20</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e3544439-7ccd-4ca7-b781-e8b1a6ee1ce3" class="xyz-checkbox"/>
                    <label for="e3544439-7ccd-4ca7-b781-e8b1a6ee1ce3">Terrain <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MapTiler.Terrain</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.maptiler.com/tiles/{variant}/{z}/{x}/{y}.{ext}?key={key}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a></dd><dt><span>attribution</span></dt><dd>(C) MapTiler (C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>terrain-rgb</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>key</span></dt><dd><insert your MapTiler Cloud API key here></dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>12</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5ba9f658-7768-4bbc-856c-6ed3782e5040" class="xyz-checkbox"/>
                    <label for="5ba9f658-7768-4bbc-856c-6ed3782e5040">TomTom <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">3 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="791d032b-18b8-441c-8a4e-e41795525474" class="xyz-checkbox"/>
                    <label for="791d032b-18b8-441c-8a4e-e41795525474">Basic <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">TomTom.Basic</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.api.tomtom.com/map/1/tile/{variant}/{style}/{z}/{x}/{y}.{ext}?key={apikey}</dd><dt><span>variant</span></dt><dd>basic</dd><dt><span>max_zoom</span></dt><dd>22</dd><dt><span>html_attribution</span></dt><dd><a href="https://tomtom.com" target="_blank">&copy;  1992 - 2023 TomTom.</a> </dd><dt><span>attribution</span></dt><dd>(C) 1992 - 2023 TomTom.</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>style</span></dt><dd>main</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>apikey</span></dt><dd><insert your API key here></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4d37cd2e-0009-4f98-b5f6-41229e721089" class="xyz-checkbox"/>
                    <label for="4d37cd2e-0009-4f98-b5f6-41229e721089">Hybrid <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">TomTom.Hybrid</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.api.tomtom.com/map/1/tile/{variant}/{style}/{z}/{x}/{y}.{ext}?key={apikey}</dd><dt><span>variant</span></dt><dd>hybrid</dd><dt><span>max_zoom</span></dt><dd>22</dd><dt><span>html_attribution</span></dt><dd><a href="https://tomtom.com" target="_blank">&copy;  1992 - 2023 TomTom.</a> </dd><dt><span>attribution</span></dt><dd>(C) 1992 - 2023 TomTom.</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>style</span></dt><dd>main</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>apikey</span></dt><dd><insert your API key here></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="7ff1d2b9-35c0-4ca8-9d32-54bf3d53353c" class="xyz-checkbox"/>
                    <label for="7ff1d2b9-35c0-4ca8-9d32-54bf3d53353c">Labels <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">TomTom.Labels</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.api.tomtom.com/map/1/tile/{variant}/{style}/{z}/{x}/{y}.{ext}?key={apikey}</dd><dt><span>variant</span></dt><dd>labels</dd><dt><span>max_zoom</span></dt><dd>22</dd><dt><span>html_attribution</span></dt><dd><a href="https://tomtom.com" target="_blank">&copy;  1992 - 2023 TomTom.</a> </dd><dt><span>attribution</span></dt><dd>(C) 1992 - 2023 TomTom.</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>style</span></dt><dd>main</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>apikey</span></dt><dd><insert your API key here></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="516ee0f7-f27d-4b32-9c2c-b37e91fe5282" class="xyz-checkbox"/>
                    <label for="516ee0f7-f27d-4b32-9c2c-b37e91fe5282">Esri <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">15 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="4c835027-71cd-460a-92e0-afd3a9d1a64e" class="xyz-checkbox"/>
                    <label for="4c835027-71cd-460a-92e0-afd3a9d1a64e">WorldStreetMap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.WorldStreetMap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://server.arcgisonline.com/ArcGIS/rest/services/{variant}/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>World_Street_Map</dd><dt><span>html_attribution</span></dt><dd>Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012</dd><dt><span>attribution</span></dt><dd>Tiles (C) Esri -- Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="dc859181-7c41-4235-bf1b-9dc9be5a4b4c" class="xyz-checkbox"/>
                    <label for="dc859181-7c41-4235-bf1b-9dc9be5a4b4c">DeLorme <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.DeLorme</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://server.arcgisonline.com/ArcGIS/rest/services/{variant}/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>Specialty/DeLorme_World_Base_Map</dd><dt><span>html_attribution</span></dt><dd>Tiles &copy; Esri &mdash; Copyright: &copy;2012 DeLorme</dd><dt><span>attribution</span></dt><dd>Tiles (C) Esri -- Copyright: (C)2012 DeLorme</dd><dt><span>min_zoom</span></dt><dd>1</dd><dt><span>max_zoom</span></dt><dd>11</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2c474cec-1462-4d7f-b32b-8879e1690197" class="xyz-checkbox"/>
                    <label for="2c474cec-1462-4d7f-b32b-8879e1690197">WorldTopoMap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.WorldTopoMap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://server.arcgisonline.com/ArcGIS/rest/services/{variant}/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>World_Topo_Map</dd><dt><span>html_attribution</span></dt><dd>Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community</dd><dt><span>attribution</span></dt><dd>Tiles (C) Esri -- Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="122ada3b-a9d6-4e3a-b434-0fe42fd67ba3" class="xyz-checkbox"/>
                    <label for="122ada3b-a9d6-4e3a-b434-0fe42fd67ba3">WorldImagery <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.WorldImagery</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://server.arcgisonline.com/ArcGIS/rest/services/{variant}/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>World_Imagery</dd><dt><span>html_attribution</span></dt><dd>Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community</dd><dt><span>attribution</span></dt><dd>Tiles (C) Esri -- Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9feda8cc-5798-4d4a-928c-5faa30090115" class="xyz-checkbox"/>
                    <label for="9feda8cc-5798-4d4a-928c-5faa30090115">WorldTerrain <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.WorldTerrain</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://server.arcgisonline.com/ArcGIS/rest/services/{variant}/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>World_Terrain_Base</dd><dt><span>html_attribution</span></dt><dd>Tiles &copy; Esri &mdash; Source: USGS, Esri, TANA, DeLorme, and NPS</dd><dt><span>attribution</span></dt><dd>Tiles (C) Esri -- Source: USGS, Esri, TANA, DeLorme, and NPS</dd><dt><span>max_zoom</span></dt><dd>13</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="257f6473-16f9-4ded-9515-5b80afbdea11" class="xyz-checkbox"/>
                    <label for="257f6473-16f9-4ded-9515-5b80afbdea11">WorldShadedRelief <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.WorldShadedRelief</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://server.arcgisonline.com/ArcGIS/rest/services/{variant}/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>World_Shaded_Relief</dd><dt><span>html_attribution</span></dt><dd>Tiles &copy; Esri &mdash; Source: Esri</dd><dt><span>attribution</span></dt><dd>Tiles (C) Esri -- Source: Esri</dd><dt><span>max_zoom</span></dt><dd>13</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9d59d3d4-db89-4b36-b662-af37320cc5e8" class="xyz-checkbox"/>
                    <label for="9d59d3d4-db89-4b36-b662-af37320cc5e8">WorldPhysical <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.WorldPhysical</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://server.arcgisonline.com/ArcGIS/rest/services/{variant}/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>World_Physical_Map</dd><dt><span>html_attribution</span></dt><dd>Tiles &copy; Esri &mdash; Source: US National Park Service</dd><dt><span>attribution</span></dt><dd>Tiles (C) Esri -- Source: US National Park Service</dd><dt><span>max_zoom</span></dt><dd>8</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="57e8f65a-12e0-49d0-a11e-c733d7261653" class="xyz-checkbox"/>
                    <label for="57e8f65a-12e0-49d0-a11e-c733d7261653">OceanBasemap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.OceanBasemap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://server.arcgisonline.com/ArcGIS/rest/services/{variant}/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>Ocean/World_Ocean_Base</dd><dt><span>html_attribution</span></dt><dd>Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri</dd><dt><span>attribution</span></dt><dd>Tiles (C) Esri -- Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri</dd><dt><span>max_zoom</span></dt><dd>13</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="94c41e24-640f-48a4-af9e-13f791cbfa1f" class="xyz-checkbox"/>
                    <label for="94c41e24-640f-48a4-af9e-13f791cbfa1f">NatGeoWorldMap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.NatGeoWorldMap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://server.arcgisonline.com/ArcGIS/rest/services/{variant}/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>NatGeo_World_Map</dd><dt><span>html_attribution</span></dt><dd>Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, NAVTEQ, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC</dd><dt><span>attribution</span></dt><dd>Tiles (C) Esri -- National Geographic, Esri, DeLorme, NAVTEQ, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC</dd><dt><span>max_zoom</span></dt><dd>16</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b60fe869-376d-462e-9fa7-4a5778a8a3f5" class="xyz-checkbox"/>
                    <label for="b60fe869-376d-462e-9fa7-4a5778a8a3f5">WorldGrayCanvas <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.WorldGrayCanvas</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://server.arcgisonline.com/ArcGIS/rest/services/{variant}/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>Canvas/World_Light_Gray_Base</dd><dt><span>html_attribution</span></dt><dd>Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ</dd><dt><span>attribution</span></dt><dd>Tiles (C) Esri -- Esri, DeLorme, NAVTEQ</dd><dt><span>max_zoom</span></dt><dd>16</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b8382920-a86e-4287-875f-159ea0f67170" class="xyz-checkbox"/>
                    <label for="b8382920-a86e-4287-875f-159ea0f67170">ArcticImagery <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.ArcticImagery</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://server.arcgisonline.com/ArcGIS/rest/services/Polar/Arctic_Imagery/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>Arctic_Imagery</dd><dt><span>html_attribution</span></dt><dd>Earthstar Geographics</dd><dt><span>attribution</span></dt><dd>Earthstar Geographics</dd><dt><span>max_zoom</span></dt><dd>24</dd><dt><span>crs</span></dt><dd>EPSG:5936</dd><dt><span>bounds</span></dt><dd>[[-2623285.8808999993, -2623285.8808999993], [6623285.8803, 6623285.8803]]</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="36c41bbe-d08f-4ff3-b9b4-e784104c648d" class="xyz-checkbox"/>
                    <label for="36c41bbe-d08f-4ff3-b9b4-e784104c648d">ArcticOceanBase <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.ArcticOceanBase</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://server.arcgisonline.com/ArcGIS/rest/services/Polar/Arctic_Ocean_Base/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>Arctic_Ocean_Base</dd><dt><span>html_attribution</span></dt><dd>Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community</dd><dt><span>attribution</span></dt><dd>Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community</dd><dt><span>max_zoom</span></dt><dd>24</dd><dt><span>crs</span></dt><dd>EPSG:5936</dd><dt><span>bounds</span></dt><dd>[[-2623285.8808999993, -2623285.8808999993], [6623285.8803, 6623285.8803]]</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f43f8278-0f82-4c1c-b73f-904f9330be65" class="xyz-checkbox"/>
                    <label for="f43f8278-0f82-4c1c-b73f-904f9330be65">ArcticOceanReference <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.ArcticOceanReference</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://server.arcgisonline.com/ArcGIS/rest/services/Polar/Arctic_Ocean_Reference/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>Arctic_Ocean_Reference</dd><dt><span>html_attribution</span></dt><dd>Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community</dd><dt><span>attribution</span></dt><dd>Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community</dd><dt><span>max_zoom</span></dt><dd>24</dd><dt><span>crs</span></dt><dd>EPSG:5936</dd><dt><span>bounds</span></dt><dd>[[-2623285.8808999993, -2623285.8808999993], [6623285.8803, 6623285.8803]]</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b7c010cf-658d-4c14-a9c6-a93d8aa98aea" class="xyz-checkbox"/>
                    <label for="b7c010cf-658d-4c14-a9c6-a93d8aa98aea">AntarcticImagery <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.AntarcticImagery</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://server.arcgisonline.com/ArcGIS/rest/services/Polar/Antarctic_Imagery/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>Antarctic_Imagery</dd><dt><span>html_attribution</span></dt><dd>Earthstar Geographics</dd><dt><span>attribution</span></dt><dd>Earthstar Geographics</dd><dt><span>max_zoom</span></dt><dd>24</dd><dt><span>crs</span></dt><dd>EPSG:3031</dd><dt><span>bounds</span></dt><dd>[[-9913957.327914657, -5730886.461772691], [9913957.327914657, 5730886.461773157]]</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="7080b359-c78a-4c4f-92f4-297e6c9b39f9" class="xyz-checkbox"/>
                    <label for="7080b359-c78a-4c4f-92f4-297e6c9b39f9">AntarcticBasemap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Esri.AntarcticBasemap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.arcgis.com/tiles/C8EMgrsFcRFL6LrL/arcgis/rest/services/Antarctic_Basemap/MapServer/tile/{z}/{y}/{x}</dd><dt><span>variant</span></dt><dd>Antarctic_Basemap</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by NOAA National Centers for Environmental Information (NCEI); International Bathymetric Chart of the Southern Ocean (IBCSO); General Bathymetric Chart of the Oceans (GEBCO).</dd><dt><span>attribution</span></dt><dd>Imagery provided by NOAA National Centers for Environmental Information (NCEI); International Bathymetric Chart of the Southern Ocean (IBCSO); General Bathymetric Chart of the Oceans (GEBCO).</dd><dt><span>max_zoom</span></dt><dd>9</dd><dt><span>crs</span></dt><dd>EPSG:3031</dd><dt><span>bounds</span></dt><dd>[[-4524583.19363305, -4524449.487765655], [4524449.4877656475, 4524583.193633042]]</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b2529ed9-3026-4481-8144-5ed90ea17c72" class="xyz-checkbox"/>
                    <label for="b2529ed9-3026-4481-8144-5ed90ea17c72">OpenWeatherMap <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">11 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="2131e88b-ad75-4774-bf5a-b3eff53db46e" class="xyz-checkbox"/>
                    <label for="2131e88b-ad75-4774-bf5a-b3eff53db46e">Clouds <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenWeatherMap.Clouds</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://{s}.tile.openweathermap.org/map/{variant}/{z}/{x}/{y}.png?appid={apiKey}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a></dd><dt><span>attribution</span></dt><dd>Map data (C) OpenWeatherMap</dd><dt><span>apiKey</span></dt><dd><insert your api key here></dd><dt><span>opacity</span></dt><dd>0.5</dd><dt><span>variant</span></dt><dd>clouds</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="08f7494c-1864-49b0-bdcc-c157779ea101" class="xyz-checkbox"/>
                    <label for="08f7494c-1864-49b0-bdcc-c157779ea101">CloudsClassic <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenWeatherMap.CloudsClassic</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://{s}.tile.openweathermap.org/map/{variant}/{z}/{x}/{y}.png?appid={apiKey}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a></dd><dt><span>attribution</span></dt><dd>Map data (C) OpenWeatherMap</dd><dt><span>apiKey</span></dt><dd><insert your api key here></dd><dt><span>opacity</span></dt><dd>0.5</dd><dt><span>variant</span></dt><dd>clouds_cls</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="04cee424-6985-49ee-b2f4-2ad2ea91ab48" class="xyz-checkbox"/>
                    <label for="04cee424-6985-49ee-b2f4-2ad2ea91ab48">Precipitation <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenWeatherMap.Precipitation</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://{s}.tile.openweathermap.org/map/{variant}/{z}/{x}/{y}.png?appid={apiKey}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a></dd><dt><span>attribution</span></dt><dd>Map data (C) OpenWeatherMap</dd><dt><span>apiKey</span></dt><dd><insert your api key here></dd><dt><span>opacity</span></dt><dd>0.5</dd><dt><span>variant</span></dt><dd>precipitation</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b66b521d-3176-45b9-8754-f2c4c4debfc2" class="xyz-checkbox"/>
                    <label for="b66b521d-3176-45b9-8754-f2c4c4debfc2">PrecipitationClassic <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenWeatherMap.PrecipitationClassic</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://{s}.tile.openweathermap.org/map/{variant}/{z}/{x}/{y}.png?appid={apiKey}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a></dd><dt><span>attribution</span></dt><dd>Map data (C) OpenWeatherMap</dd><dt><span>apiKey</span></dt><dd><insert your api key here></dd><dt><span>opacity</span></dt><dd>0.5</dd><dt><span>variant</span></dt><dd>precipitation_cls</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="6dedcefd-e5bb-4941-9a2d-8719bda2a306" class="xyz-checkbox"/>
                    <label for="6dedcefd-e5bb-4941-9a2d-8719bda2a306">Rain <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenWeatherMap.Rain</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://{s}.tile.openweathermap.org/map/{variant}/{z}/{x}/{y}.png?appid={apiKey}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a></dd><dt><span>attribution</span></dt><dd>Map data (C) OpenWeatherMap</dd><dt><span>apiKey</span></dt><dd><insert your api key here></dd><dt><span>opacity</span></dt><dd>0.5</dd><dt><span>variant</span></dt><dd>rain</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="43d8f862-5d32-481a-a210-c105ba642325" class="xyz-checkbox"/>
                    <label for="43d8f862-5d32-481a-a210-c105ba642325">RainClassic <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenWeatherMap.RainClassic</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://{s}.tile.openweathermap.org/map/{variant}/{z}/{x}/{y}.png?appid={apiKey}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a></dd><dt><span>attribution</span></dt><dd>Map data (C) OpenWeatherMap</dd><dt><span>apiKey</span></dt><dd><insert your api key here></dd><dt><span>opacity</span></dt><dd>0.5</dd><dt><span>variant</span></dt><dd>rain_cls</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9a38fb5c-a083-46fd-86f3-54b4dc917230" class="xyz-checkbox"/>
                    <label for="9a38fb5c-a083-46fd-86f3-54b4dc917230">Pressure <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenWeatherMap.Pressure</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://{s}.tile.openweathermap.org/map/{variant}/{z}/{x}/{y}.png?appid={apiKey}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a></dd><dt><span>attribution</span></dt><dd>Map data (C) OpenWeatherMap</dd><dt><span>apiKey</span></dt><dd><insert your api key here></dd><dt><span>opacity</span></dt><dd>0.5</dd><dt><span>variant</span></dt><dd>pressure</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="6da0eddc-85c7-4a71-89b0-89d83a6ae2ef" class="xyz-checkbox"/>
                    <label for="6da0eddc-85c7-4a71-89b0-89d83a6ae2ef">PressureContour <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenWeatherMap.PressureContour</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://{s}.tile.openweathermap.org/map/{variant}/{z}/{x}/{y}.png?appid={apiKey}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a></dd><dt><span>attribution</span></dt><dd>Map data (C) OpenWeatherMap</dd><dt><span>apiKey</span></dt><dd><insert your api key here></dd><dt><span>opacity</span></dt><dd>0.5</dd><dt><span>variant</span></dt><dd>pressure_cntr</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="20a2b340-dde8-428a-b11f-8d0fa221f257" class="xyz-checkbox"/>
                    <label for="20a2b340-dde8-428a-b11f-8d0fa221f257">Wind <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenWeatherMap.Wind</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://{s}.tile.openweathermap.org/map/{variant}/{z}/{x}/{y}.png?appid={apiKey}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a></dd><dt><span>attribution</span></dt><dd>Map data (C) OpenWeatherMap</dd><dt><span>apiKey</span></dt><dd><insert your api key here></dd><dt><span>opacity</span></dt><dd>0.5</dd><dt><span>variant</span></dt><dd>wind</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="32a5ff83-79d5-4f17-a1e8-fb458f11c796" class="xyz-checkbox"/>
                    <label for="32a5ff83-79d5-4f17-a1e8-fb458f11c796">Temperature <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenWeatherMap.Temperature</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://{s}.tile.openweathermap.org/map/{variant}/{z}/{x}/{y}.png?appid={apiKey}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a></dd><dt><span>attribution</span></dt><dd>Map data (C) OpenWeatherMap</dd><dt><span>apiKey</span></dt><dd><insert your api key here></dd><dt><span>opacity</span></dt><dd>0.5</dd><dt><span>variant</span></dt><dd>temp</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="04ee30e3-1edf-4f81-acdb-dc4efd1c2dcb" class="xyz-checkbox"/>
                    <label for="04ee30e3-1edf-4f81-acdb-dc4efd1c2dcb">Snow <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenWeatherMap.Snow</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://{s}.tile.openweathermap.org/map/{variant}/{z}/{x}/{y}.png?appid={apiKey}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a></dd><dt><span>attribution</span></dt><dd>Map data (C) OpenWeatherMap</dd><dt><span>apiKey</span></dt><dd><insert your api key here></dd><dt><span>opacity</span></dt><dd>0.5</dd><dt><span>variant</span></dt><dd>snow</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9c609f15-9c3f-4818-83bc-bef4a5cd10f5" class="xyz-checkbox"/>
                    <label for="9c609f15-9c3f-4818-83bc-bef4a5cd10f5">HERE <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">30 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="107bbc57-0b57-4df2-bd2e-ab621ec77eec" class="xyz-checkbox"/>
                    <label for="107bbc57-0b57-4df2-bd2e-ab621ec77eec">normalDay <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.normalDay</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="79fbb38c-a0ee-44ac-8f51-d754ed2b4ded" class="xyz-checkbox"/>
                    <label for="79fbb38c-a0ee-44ac-8f51-d754ed2b4ded">normalDayCustom <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.normalDayCustom</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day.custom</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8ab3037b-4276-43ba-9f08-cc243db3dbfb" class="xyz-checkbox"/>
                    <label for="8ab3037b-4276-43ba-9f08-cc243db3dbfb">normalDayGrey <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.normalDayGrey</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day.grey</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f860e4a6-4779-469b-a60d-f9d2c9e59b5b" class="xyz-checkbox"/>
                    <label for="f860e4a6-4779-469b-a60d-f9d2c9e59b5b">normalDayMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.normalDayMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="aa87c73a-bb03-477b-b5c6-165c65aee9ac" class="xyz-checkbox"/>
                    <label for="aa87c73a-bb03-477b-b5c6-165c65aee9ac">normalDayGreyMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.normalDayGreyMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day.grey.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b7b35b54-6d24-4866-a5e1-52544a5304b4" class="xyz-checkbox"/>
                    <label for="b7b35b54-6d24-4866-a5e1-52544a5304b4">normalDayTransit <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.normalDayTransit</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day.transit</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="87528468-3f42-4f09-aa37-fd5104aed4c2" class="xyz-checkbox"/>
                    <label for="87528468-3f42-4f09-aa37-fd5104aed4c2">normalDayTransitMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.normalDayTransitMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day.transit.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cd4fedcc-0c6e-4092-9602-c49633216d1b" class="xyz-checkbox"/>
                    <label for="cd4fedcc-0c6e-4092-9602-c49633216d1b">normalDayTraffic <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.normalDayTraffic</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>traffic</dd><dt><span>variant</span></dt><dd>normal.traffic.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>traffictile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5b99c6e4-59d8-45f9-ad93-f25881603f08" class="xyz-checkbox"/>
                    <label for="5b99c6e4-59d8-45f9-ad93-f25881603f08">normalNight <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.normalNight</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.night</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="c83c3cf2-2e9b-44b0-8041-30f0e20f4664" class="xyz-checkbox"/>
                    <label for="c83c3cf2-2e9b-44b0-8041-30f0e20f4664">normalNightMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.normalNightMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.night.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4c92b86b-4e26-4b6b-b5dc-522cf4b5bd12" class="xyz-checkbox"/>
                    <label for="4c92b86b-4e26-4b6b-b5dc-522cf4b5bd12">normalNightGrey <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.normalNightGrey</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.night.grey</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2f8a4e33-ac07-42f0-87d3-37a8dd7f47e6" class="xyz-checkbox"/>
                    <label for="2f8a4e33-ac07-42f0-87d3-37a8dd7f47e6">normalNightGreyMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.normalNightGreyMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.night.grey.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="1521ee0f-fc9d-417c-904b-fc845633e486" class="xyz-checkbox"/>
                    <label for="1521ee0f-fc9d-417c-904b-fc845633e486">normalNightTransit <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.normalNightTransit</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.night.transit</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="60fbd727-08f7-423e-9400-a9eaa83c20a6" class="xyz-checkbox"/>
                    <label for="60fbd727-08f7-423e-9400-a9eaa83c20a6">normalNightTransitMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.normalNightTransitMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.night.transit.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="512e5d41-29de-4113-85aa-6351270957ea" class="xyz-checkbox"/>
                    <label for="512e5d41-29de-4113-85aa-6351270957ea">reducedDay <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.reducedDay</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>reduced.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0a44c724-5681-454b-9e26-0d78392b2ed9" class="xyz-checkbox"/>
                    <label for="0a44c724-5681-454b-9e26-0d78392b2ed9">reducedNight <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.reducedNight</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>reduced.night</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f7f67ce2-83b1-4135-96e9-73535b10b8b0" class="xyz-checkbox"/>
                    <label for="f7f67ce2-83b1-4135-96e9-73535b10b8b0">basicMap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.basicMap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>basetile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="baece710-7a7e-49ed-9ccb-db95a23b8503" class="xyz-checkbox"/>
                    <label for="baece710-7a7e-49ed-9ccb-db95a23b8503">mapLabels <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.mapLabels</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>labeltile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="dedf06b1-5901-415e-9ba5-cc6661db46fa" class="xyz-checkbox"/>
                    <label for="dedf06b1-5901-415e-9ba5-cc6661db46fa">trafficFlow <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.trafficFlow</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>traffic</dd><dt><span>variant</span></dt><dd>normal.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>flowtile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="146feb31-ac53-4f56-a0c6-b4887e0b6aa6" class="xyz-checkbox"/>
                    <label for="146feb31-ac53-4f56-a0c6-b4887e0b6aa6">carnavDayGrey <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.carnavDayGrey</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>carnav.day.grey</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="c4c092bf-1cf9-4d86-a90a-da03781ff4bc" class="xyz-checkbox"/>
                    <label for="c4c092bf-1cf9-4d86-a90a-da03781ff4bc">hybridDay <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.hybridDay</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>aerial</dd><dt><span>variant</span></dt><dd>hybrid.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="aa685bee-71ad-40c7-bfe6-9d1924527c51" class="xyz-checkbox"/>
                    <label for="aa685bee-71ad-40c7-bfe6-9d1924527c51">hybridDayMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.hybridDayMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>aerial</dd><dt><span>variant</span></dt><dd>hybrid.day.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="07bb6b30-d612-4479-ad24-e2d0f7d92710" class="xyz-checkbox"/>
                    <label for="07bb6b30-d612-4479-ad24-e2d0f7d92710">hybridDayTransit <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.hybridDayTransit</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>aerial</dd><dt><span>variant</span></dt><dd>hybrid.day.transit</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="d539b5c9-50f0-4651-823d-c65003e44719" class="xyz-checkbox"/>
                    <label for="d539b5c9-50f0-4651-823d-c65003e44719">hybridDayGrey <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.hybridDayGrey</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>aerial</dd><dt><span>variant</span></dt><dd>hybrid.grey.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="fd0edca1-ef25-4c45-bef0-74f591699bd3" class="xyz-checkbox"/>
                    <label for="fd0edca1-ef25-4c45-bef0-74f591699bd3">hybridDayTraffic <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.hybridDayTraffic</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>traffic</dd><dt><span>variant</span></dt><dd>hybrid.traffic.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>traffictile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="aa3a5a2f-5084-47f1-8b79-b2484e622354" class="xyz-checkbox"/>
                    <label for="aa3a5a2f-5084-47f1-8b79-b2484e622354">pedestrianDay <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.pedestrianDay</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>pedestrian.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="40bc6b0a-212f-42e3-9f7c-808d43c5406d" class="xyz-checkbox"/>
                    <label for="40bc6b0a-212f-42e3-9f7c-808d43c5406d">pedestrianNight <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.pedestrianNight</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>pedestrian.night</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9ab0be02-166a-4e59-9606-c8af57c8c77e" class="xyz-checkbox"/>
                    <label for="9ab0be02-166a-4e59-9606-c8af57c8c77e">satelliteDay <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.satelliteDay</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>aerial</dd><dt><span>variant</span></dt><dd>satellite.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="99590497-52d2-4a4a-8907-e4030ff06b58" class="xyz-checkbox"/>
                    <label for="99590497-52d2-4a4a-8907-e4030ff06b58">terrainDay <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.terrainDay</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>aerial</dd><dt><span>variant</span></dt><dd>terrain.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="042d9555-ee8e-4fc1-bf8c-d4cce81339df" class="xyz-checkbox"/>
                    <label for="042d9555-ee8e-4fc1-bf8c-d4cce81339df">terrainDayMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HERE.terrainDayMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.api.here.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>app_id</span></dt><dd><insert your app_id here></dd><dt><span>app_code</span></dt><dd><insert your app_code here></dd><dt><span>base</span></dt><dd>aerial</dd><dt><span>variant</span></dt><dd>terrain.day.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="1ddaa7f8-9586-4399-848e-7ac2a1b5de9e" class="xyz-checkbox"/>
                    <label for="1ddaa7f8-9586-4399-848e-7ac2a1b5de9e">HEREv3 <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">28 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="a60bf067-e168-4461-848e-07c7ae2bc71a" class="xyz-checkbox"/>
                    <label for="a60bf067-e168-4461-848e-07c7ae2bc71a">normalDay <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.normalDay</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="070291f6-820c-4648-97ef-c427e92e0990" class="xyz-checkbox"/>
                    <label for="070291f6-820c-4648-97ef-c427e92e0990">normalDayCustom <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.normalDayCustom</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day.custom</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="c17a0fb5-2195-430c-9446-eb2a2cc7b617" class="xyz-checkbox"/>
                    <label for="c17a0fb5-2195-430c-9446-eb2a2cc7b617">normalDayGrey <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.normalDayGrey</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day.grey</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ced890ea-ee7f-4c2b-9c80-f3dc56823f4f" class="xyz-checkbox"/>
                    <label for="ced890ea-ee7f-4c2b-9c80-f3dc56823f4f">normalDayMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.normalDayMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3e190f08-a94e-4a42-96ac-9d9201b0d91b" class="xyz-checkbox"/>
                    <label for="3e190f08-a94e-4a42-96ac-9d9201b0d91b">normalDayGreyMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.normalDayGreyMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day.grey.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="bf2cb30a-cd20-443e-bec3-df3bfc5a6af5" class="xyz-checkbox"/>
                    <label for="bf2cb30a-cd20-443e-bec3-df3bfc5a6af5">normalDayTransit <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.normalDayTransit</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day.transit</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="990dcf53-d076-46e5-8eb0-9c08c6b0f65e" class="xyz-checkbox"/>
                    <label for="990dcf53-d076-46e5-8eb0-9c08c6b0f65e">normalDayTransitMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.normalDayTransitMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day.transit.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="7900d691-661e-4485-9528-abb6848c9f87" class="xyz-checkbox"/>
                    <label for="7900d691-661e-4485-9528-abb6848c9f87">normalNight <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.normalNight</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.night</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="88296b95-98ae-4e4d-8184-b35c1a5d4bd3" class="xyz-checkbox"/>
                    <label for="88296b95-98ae-4e4d-8184-b35c1a5d4bd3">normalNightMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.normalNightMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.night.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="56c4ddd4-af9b-486a-8891-53e730a9d8a8" class="xyz-checkbox"/>
                    <label for="56c4ddd4-af9b-486a-8891-53e730a9d8a8">normalNightGrey <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.normalNightGrey</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.night.grey</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3bbdf253-b135-4bbb-9304-89bdfbfda75c" class="xyz-checkbox"/>
                    <label for="3bbdf253-b135-4bbb-9304-89bdfbfda75c">normalNightGreyMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.normalNightGreyMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.night.grey.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cdd8807d-f7c4-417c-8200-0398a0b74f1a" class="xyz-checkbox"/>
                    <label for="cdd8807d-f7c4-417c-8200-0398a0b74f1a">normalNightTransit <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.normalNightTransit</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.night.transit</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="656c923d-9823-4c98-aa0c-3e5b1fe5b502" class="xyz-checkbox"/>
                    <label for="656c923d-9823-4c98-aa0c-3e5b1fe5b502">normalNightTransitMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.normalNightTransitMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.night.transit.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="68628230-49c1-4513-8562-c5bc61dc616f" class="xyz-checkbox"/>
                    <label for="68628230-49c1-4513-8562-c5bc61dc616f">reducedDay <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.reducedDay</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>reduced.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="366ac4e1-ea40-4c92-8e1d-d9b4d22028ba" class="xyz-checkbox"/>
                    <label for="366ac4e1-ea40-4c92-8e1d-d9b4d22028ba">reducedNight <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.reducedNight</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>reduced.night</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="bec0b4ee-39db-4105-9505-3c41c449de9e" class="xyz-checkbox"/>
                    <label for="bec0b4ee-39db-4105-9505-3c41c449de9e">basicMap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.basicMap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>basetile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="55e1badb-9477-40c9-9c72-80204f9ca0da" class="xyz-checkbox"/>
                    <label for="55e1badb-9477-40c9-9c72-80204f9ca0da">mapLabels <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.mapLabels</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>normal.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>labeltile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="93a2941c-7cc4-418e-b09e-3efd54fe0fae" class="xyz-checkbox"/>
                    <label for="93a2941c-7cc4-418e-b09e-3efd54fe0fae">trafficFlow <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.trafficFlow</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>traffic</dd><dt><span>variant</span></dt><dd>normal.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>flowtile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="57398234-397a-48e0-bc9a-4b1725d32796" class="xyz-checkbox"/>
                    <label for="57398234-397a-48e0-bc9a-4b1725d32796">carnavDayGrey <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.carnavDayGrey</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>carnav.day.grey</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="61c01023-d739-48af-ad65-985ef1cad2ff" class="xyz-checkbox"/>
                    <label for="61c01023-d739-48af-ad65-985ef1cad2ff">hybridDay <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.hybridDay</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>aerial</dd><dt><span>variant</span></dt><dd>hybrid.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f43099bc-aa5d-4b0a-b8f8-ef47c50a534c" class="xyz-checkbox"/>
                    <label for="f43099bc-aa5d-4b0a-b8f8-ef47c50a534c">hybridDayMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.hybridDayMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>aerial</dd><dt><span>variant</span></dt><dd>hybrid.day.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3a036267-467c-4f63-a352-8967bf845ca1" class="xyz-checkbox"/>
                    <label for="3a036267-467c-4f63-a352-8967bf845ca1">hybridDayTransit <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.hybridDayTransit</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>aerial</dd><dt><span>variant</span></dt><dd>hybrid.day.transit</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0fb26dec-8dfc-4050-b9a4-75cd8cd07eb8" class="xyz-checkbox"/>
                    <label for="0fb26dec-8dfc-4050-b9a4-75cd8cd07eb8">hybridDayGrey <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.hybridDayGrey</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>aerial</dd><dt><span>variant</span></dt><dd>hybrid.grey.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="587d78a5-c3f7-414a-9d06-88bdd7198852" class="xyz-checkbox"/>
                    <label for="587d78a5-c3f7-414a-9d06-88bdd7198852">pedestrianDay <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.pedestrianDay</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>pedestrian.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f941ede2-5776-4dfc-af8f-5d28f7e7864c" class="xyz-checkbox"/>
                    <label for="f941ede2-5776-4dfc-af8f-5d28f7e7864c">pedestrianNight <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.pedestrianNight</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>base</dd><dt><span>variant</span></dt><dd>pedestrian.night</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="d904180d-2cc7-4384-a5da-82cc18aacf7c" class="xyz-checkbox"/>
                    <label for="d904180d-2cc7-4384-a5da-82cc18aacf7c">satelliteDay <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.satelliteDay</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>aerial</dd><dt><span>variant</span></dt><dd>satellite.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="6fd7e5d0-af44-426e-982f-f5fa45bc2cb1" class="xyz-checkbox"/>
                    <label for="6fd7e5d0-af44-426e-982f-f5fa45bc2cb1">terrainDay <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.terrainDay</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>aerial</dd><dt><span>variant</span></dt><dd>terrain.day</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="21e7c4ef-06d5-454b-96db-8312c96b1235" class="xyz-checkbox"/>
                    <label for="21e7c4ef-06d5-454b-96db-8312c96b1235">terrainDayMobile <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HEREv3.terrainDayMobile</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.{base}.maps.ls.hereapi.com/maptile/2.1/{type}/{mapID}/{variant}/{z}/{x}/{y}/{size}/{format}?apiKey={apiKey}&lg={language}</dd><dt><span>html_attribution</span></dt><dd>Map &copy; 1987-2023 <a href="http://developer.here.com">HERE</a></dd><dt><span>attribution</span></dt><dd>Map (C) 1987-2023 HERE</dd><dt><span>subdomains</span></dt><dd>1234</dd><dt><span>mapID</span></dt><dd>newest</dd><dt><span>apiKey</span></dt><dd><insert your apiKey here></dd><dt><span>base</span></dt><dd>aerial</dd><dt><span>variant</span></dt><dd>terrain.day.mobile</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>type</span></dt><dd>maptile</dd><dt><span>language</span></dt><dd>eng</dd><dt><span>format</span></dt><dd>png8</dd><dt><span>size</span></dt><dd>256</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9ec7225b-e7bd-408e-90b5-8a2dd501c348" class="xyz-checkbox"/>
                    <label for="9ec7225b-e7bd-408e-90b5-8a2dd501c348">FreeMapSK <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">FreeMapSK</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.freemap.sk/T/{z}/{x}/{y}.jpeg</dd><dt><span>min_zoom</span></dt><dd>8</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>bounds</span></dt><dd>[[47.204642, 15.996093], [49.830896, 22.576904]]</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, visualization CC-By-SA 2.0 <a href="http://freemap.sk">Freemap.sk</a></dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors, visualization CC-By-SA 2.0 Freemap.sk</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8ad8dbb5-2912-4d19-a8fe-bbc4549f121d" class="xyz-checkbox"/>
                    <label for="8ad8dbb5-2912-4d19-a8fe-bbc4549f121d">MtbMap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">MtbMap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://tile.mtbmap.cz/mtbmap_tiles/{z}/{x}/{y}.png</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &amp; USGS</dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors & USGS</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2d8dbaa2-e4e7-4e5e-b1a9-979f12fe5f30" class="xyz-checkbox"/>
                    <label for="2d8dbaa2-e4e7-4e5e-b1a9-979f12fe5f30">CartoDB <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">10 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="dd69e7ae-5ed0-4e79-8b65-4731650ca477" class="xyz-checkbox"/>
                    <label for="dd69e7ae-5ed0-4e79-8b65-4731650ca477">Positron <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">CartoDB.Positron</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.basemaps.cartocdn.com/{variant}/{z}/{x}/{y}{r}.png</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a></dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors (C) CARTO</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>variant</span></dt><dd>light_all</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="bd91192d-8308-47fe-a81a-24c519753c2a" class="xyz-checkbox"/>
                    <label for="bd91192d-8308-47fe-a81a-24c519753c2a">PositronNoLabels <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">CartoDB.PositronNoLabels</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.basemaps.cartocdn.com/{variant}/{z}/{x}/{y}{r}.png</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a></dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors (C) CARTO</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>variant</span></dt><dd>light_nolabels</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="90d071b7-05d0-45ab-b537-df40a0f12208" class="xyz-checkbox"/>
                    <label for="90d071b7-05d0-45ab-b537-df40a0f12208">PositronOnlyLabels <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">CartoDB.PositronOnlyLabels</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.basemaps.cartocdn.com/{variant}/{z}/{x}/{y}{r}.png</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a></dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors (C) CARTO</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>variant</span></dt><dd>light_only_labels</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="d3f4cf0f-2834-4209-8cc0-28b1e585d3b2" class="xyz-checkbox"/>
                    <label for="d3f4cf0f-2834-4209-8cc0-28b1e585d3b2">DarkMatter <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">CartoDB.DarkMatter</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.basemaps.cartocdn.com/{variant}/{z}/{x}/{y}{r}.png</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a></dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors (C) CARTO</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>variant</span></dt><dd>dark_all</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="c19de815-f253-4895-94e6-421d5e88a2e5" class="xyz-checkbox"/>
                    <label for="c19de815-f253-4895-94e6-421d5e88a2e5">DarkMatterNoLabels <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">CartoDB.DarkMatterNoLabels</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.basemaps.cartocdn.com/{variant}/{z}/{x}/{y}{r}.png</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a></dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors (C) CARTO</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>variant</span></dt><dd>dark_nolabels</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="14aa32f6-345b-450b-8835-2246f15df35f" class="xyz-checkbox"/>
                    <label for="14aa32f6-345b-450b-8835-2246f15df35f">DarkMatterOnlyLabels <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">CartoDB.DarkMatterOnlyLabels</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.basemaps.cartocdn.com/{variant}/{z}/{x}/{y}{r}.png</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a></dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors (C) CARTO</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>variant</span></dt><dd>dark_only_labels</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ae75711e-06cb-4b5a-a46d-16b4e73ce841" class="xyz-checkbox"/>
                    <label for="ae75711e-06cb-4b5a-a46d-16b4e73ce841">Voyager <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">CartoDB.Voyager</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.basemaps.cartocdn.com/{variant}/{z}/{x}/{y}{r}.png</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a></dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors (C) CARTO</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>variant</span></dt><dd>rastertiles/voyager</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="6a58c2fe-49eb-4943-9ad6-698ab0c954a2" class="xyz-checkbox"/>
                    <label for="6a58c2fe-49eb-4943-9ad6-698ab0c954a2">VoyagerNoLabels <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">CartoDB.VoyagerNoLabels</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.basemaps.cartocdn.com/{variant}/{z}/{x}/{y}{r}.png</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a></dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors (C) CARTO</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>variant</span></dt><dd>rastertiles/voyager_nolabels</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f3d6f120-f1ee-41b5-b84c-14f64ef778a0" class="xyz-checkbox"/>
                    <label for="f3d6f120-f1ee-41b5-b84c-14f64ef778a0">VoyagerOnlyLabels <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">CartoDB.VoyagerOnlyLabels</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.basemaps.cartocdn.com/{variant}/{z}/{x}/{y}{r}.png</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a></dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors (C) CARTO</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>variant</span></dt><dd>rastertiles/voyager_only_labels</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4f8e3b47-1045-401f-b246-a5576fcac52b" class="xyz-checkbox"/>
                    <label for="4f8e3b47-1045-401f-b246-a5576fcac52b">VoyagerLabelsUnder <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">CartoDB.VoyagerLabelsUnder</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.basemaps.cartocdn.com/{variant}/{z}/{x}/{y}{r}.png</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a></dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors (C) CARTO</dd><dt><span>subdomains</span></dt><dd>abcd</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>variant</span></dt><dd>rastertiles/voyager_labels_under</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cd5ef780-2d0c-4aa7-ad17-9e523ade7b13" class="xyz-checkbox"/>
                    <label for="cd5ef780-2d0c-4aa7-ad17-9e523ade7b13">HikeBike <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">2 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="724dfc1c-f2fc-4ab3-8c08-a9dd67c3e66b" class="xyz-checkbox"/>
                    <label for="724dfc1c-f2fc-4ab3-8c08-a9dd67c3e66b">HikeBike <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HikeBike.HikeBike</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.wmflabs.org/{variant}/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>hikebike</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cd482a38-374a-4a4f-904d-732d6a4682fe" class="xyz-checkbox"/>
                    <label for="cd482a38-374a-4a4f-904d-732d6a4682fe">HillShading <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">HikeBike.HillShading</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.wmflabs.org/{variant}/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>15</dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</dd><dt><span>attribution</span></dt><dd>(C) OpenStreetMap contributors</dd><dt><span>variant</span></dt><dd>hillshading</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3cfa904f-9510-4d51-ae31-7b38163a6c39" class="xyz-checkbox"/>
                    <label for="3cfa904f-9510-4d51-ae31-7b38163a6c39">BasemapAT <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">7 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="089ae22d-85e7-4f3b-86cd-294d4498f652" class="xyz-checkbox"/>
                    <label for="089ae22d-85e7-4f3b-86cd-294d4498f652">basemap <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">BasemapAT.basemap</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://mapsneu.wien.gv.at/basemap/{variant}/{type}/google3857/{z}/{y}/{x}.{format}</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>Datenquelle: <a href="https://www.basemap.at">basemap.at</a></dd><dt><span>attribution</span></dt><dd>Datenquelle: basemap.at</dd><dt><span>type</span></dt><dd>normal</dd><dt><span>format</span></dt><dd>png</dd><dt><span>bounds</span></dt><dd>[[46.35877, 8.782379], [49.037872, 17.189532]]</dd><dt><span>variant</span></dt><dd>geolandbasemap</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9231de9f-998c-49c7-8953-b1b6c4f8b175" class="xyz-checkbox"/>
                    <label for="9231de9f-998c-49c7-8953-b1b6c4f8b175">grau <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">BasemapAT.grau</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://mapsneu.wien.gv.at/basemap/{variant}/{type}/google3857/{z}/{y}/{x}.{format}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Datenquelle: <a href="https://www.basemap.at">basemap.at</a></dd><dt><span>attribution</span></dt><dd>Datenquelle: basemap.at</dd><dt><span>type</span></dt><dd>normal</dd><dt><span>format</span></dt><dd>png</dd><dt><span>bounds</span></dt><dd>[[46.35877, 8.782379], [49.037872, 17.189532]]</dd><dt><span>variant</span></dt><dd>bmapgrau</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="57b9d54e-71fd-49ac-9b01-f87c11b3c128" class="xyz-checkbox"/>
                    <label for="57b9d54e-71fd-49ac-9b01-f87c11b3c128">overlay <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">BasemapAT.overlay</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://mapsneu.wien.gv.at/basemap/{variant}/{type}/google3857/{z}/{y}/{x}.{format}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Datenquelle: <a href="https://www.basemap.at">basemap.at</a></dd><dt><span>attribution</span></dt><dd>Datenquelle: basemap.at</dd><dt><span>type</span></dt><dd>normal</dd><dt><span>format</span></dt><dd>png</dd><dt><span>bounds</span></dt><dd>[[46.35877, 8.782379], [49.037872, 17.189532]]</dd><dt><span>variant</span></dt><dd>bmapoverlay</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="bf8adb84-8128-4e94-90ef-726944771dd4" class="xyz-checkbox"/>
                    <label for="bf8adb84-8128-4e94-90ef-726944771dd4">terrain <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">BasemapAT.terrain</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://mapsneu.wien.gv.at/basemap/{variant}/{type}/google3857/{z}/{y}/{x}.{format}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Datenquelle: <a href="https://www.basemap.at">basemap.at</a></dd><dt><span>attribution</span></dt><dd>Datenquelle: basemap.at</dd><dt><span>type</span></dt><dd>grau</dd><dt><span>format</span></dt><dd>jpeg</dd><dt><span>bounds</span></dt><dd>[[46.35877, 8.782379], [49.037872, 17.189532]]</dd><dt><span>variant</span></dt><dd>bmapgelaende</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a6033239-f377-4d2b-b1b8-265b0eddf3a5" class="xyz-checkbox"/>
                    <label for="a6033239-f377-4d2b-b1b8-265b0eddf3a5">surface <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">BasemapAT.surface</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://mapsneu.wien.gv.at/basemap/{variant}/{type}/google3857/{z}/{y}/{x}.{format}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Datenquelle: <a href="https://www.basemap.at">basemap.at</a></dd><dt><span>attribution</span></dt><dd>Datenquelle: basemap.at</dd><dt><span>type</span></dt><dd>grau</dd><dt><span>format</span></dt><dd>jpeg</dd><dt><span>bounds</span></dt><dd>[[46.35877, 8.782379], [49.037872, 17.189532]]</dd><dt><span>variant</span></dt><dd>bmapoberflaeche</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4d72a4f0-e31a-44d4-acc8-6b438652df55" class="xyz-checkbox"/>
                    <label for="4d72a4f0-e31a-44d4-acc8-6b438652df55">highdpi <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">BasemapAT.highdpi</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://mapsneu.wien.gv.at/basemap/{variant}/{type}/google3857/{z}/{y}/{x}.{format}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>html_attribution</span></dt><dd>Datenquelle: <a href="https://www.basemap.at">basemap.at</a></dd><dt><span>attribution</span></dt><dd>Datenquelle: basemap.at</dd><dt><span>type</span></dt><dd>normal</dd><dt><span>format</span></dt><dd>jpeg</dd><dt><span>bounds</span></dt><dd>[[46.35877, 8.782379], [49.037872, 17.189532]]</dd><dt><span>variant</span></dt><dd>bmaphidpi</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2392e09f-18b3-4fce-8508-446a8e8df958" class="xyz-checkbox"/>
                    <label for="2392e09f-18b3-4fce-8508-446a8e8df958">orthofoto <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">BasemapAT.orthofoto</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://mapsneu.wien.gv.at/basemap/{variant}/{type}/google3857/{z}/{y}/{x}.{format}</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>Datenquelle: <a href="https://www.basemap.at">basemap.at</a></dd><dt><span>attribution</span></dt><dd>Datenquelle: basemap.at</dd><dt><span>type</span></dt><dd>normal</dd><dt><span>format</span></dt><dd>jpeg</dd><dt><span>bounds</span></dt><dd>[[46.35877, 8.782379], [49.037872, 17.189532]]</dd><dt><span>variant</span></dt><dd>bmaporthofoto30cm</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="67de5c8e-24b3-43cb-b50c-dae5c0504fb7" class="xyz-checkbox"/>
                    <label for="67de5c8e-24b3-43cb-b50c-dae5c0504fb7">nlmaps <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">5 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="17e24789-5d61-4357-a0e4-d1a1b8e95a6c" class="xyz-checkbox"/>
                    <label for="17e24789-5d61-4357-a0e4-d1a1b8e95a6c">standaard <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">nlmaps.standaard</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0/{variant}/EPSG:3857/{z}/{x}/{y}.png</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>bounds</span></dt><dd>[[50.5, 3.25], [54, 7.6]]</dd><dt><span>html_attribution</span></dt><dd>Kaartgegevens &copy; <a href="https://www.kadaster.nl">Kadaster</a></dd><dt><span>attribution</span></dt><dd>Kaartgegevens (C) Kadaster</dd><dt><span>variant</span></dt><dd>standaard</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="7c221b0b-6082-42ee-9b87-a72c0938c441" class="xyz-checkbox"/>
                    <label for="7c221b0b-6082-42ee-9b87-a72c0938c441">pastel <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">nlmaps.pastel</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0/{variant}/EPSG:3857/{z}/{x}/{y}.png</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>bounds</span></dt><dd>[[50.5, 3.25], [54, 7.6]]</dd><dt><span>html_attribution</span></dt><dd>Kaartgegevens &copy; <a href="https://www.kadaster.nl">Kadaster</a></dd><dt><span>attribution</span></dt><dd>Kaartgegevens (C) Kadaster</dd><dt><span>variant</span></dt><dd>pastel</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5d774447-bbf2-4bed-ada6-a7edf38a6a34" class="xyz-checkbox"/>
                    <label for="5d774447-bbf2-4bed-ada6-a7edf38a6a34">grijs <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">nlmaps.grijs</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0/{variant}/EPSG:3857/{z}/{x}/{y}.png</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>bounds</span></dt><dd>[[50.5, 3.25], [54, 7.6]]</dd><dt><span>html_attribution</span></dt><dd>Kaartgegevens &copy; <a href="https://www.kadaster.nl">Kadaster</a></dd><dt><span>attribution</span></dt><dd>Kaartgegevens (C) Kadaster</dd><dt><span>variant</span></dt><dd>grijs</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8a2eb0be-02cf-4e2a-96f6-572af2462d68" class="xyz-checkbox"/>
                    <label for="8a2eb0be-02cf-4e2a-96f6-572af2462d68">water <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">nlmaps.water</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0/{variant}/EPSG:3857/{z}/{x}/{y}.png</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>bounds</span></dt><dd>[[50.5, 3.25], [54, 7.6]]</dd><dt><span>html_attribution</span></dt><dd>Kaartgegevens &copy; <a href="https://www.kadaster.nl">Kadaster</a></dd><dt><span>attribution</span></dt><dd>Kaartgegevens (C) Kadaster</dd><dt><span>variant</span></dt><dd>water</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ba8b4d07-31b6-4eaa-8842-8a7a3c4ce0fa" class="xyz-checkbox"/>
                    <label for="ba8b4d07-31b6-4eaa-8842-8a7a3c4ce0fa">luchtfoto <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">nlmaps.luchtfoto</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://service.pdok.nl/hwh/luchtfotorgb/wmts/v1_0/Actueel_ortho25/EPSG:3857/{z}/{x}/{y}.jpeg</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>bounds</span></dt><dd>[[50.5, 3.25], [54, 7.6]]</dd><dt><span>html_attribution</span></dt><dd>Kaartgegevens &copy; <a href="https://www.kadaster.nl">Kadaster</a></dd><dt><span>attribution</span></dt><dd>Kaartgegevens (C) Kadaster</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="bcaa5ee6-4c64-4248-8c4e-21ebda81f19d" class="xyz-checkbox"/>
                    <label for="bcaa5ee6-4c64-4248-8c4e-21ebda81f19d">NASAGIBS <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">15 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="a163629c-664f-4864-ad93-7e0d588f247c" class="xyz-checkbox"/>
                    <label for="a163629c-664f-4864-ad93-7e0d588f247c">ModisTerraTrueColorCR <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.ModisTerraTrueColorCR</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://map1.vis.earthdata.nasa.gov/wmts-webmerc/{variant}/default/{time}/{tilematrixset}{max_zoom}/{z}/{y}/{x}.{format}</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>bounds</span></dt><dd>[[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]]</dd><dt><span>min_zoom</span></dt><dd>1</dd><dt><span>max_zoom</span></dt><dd>9</dd><dt><span>format</span></dt><dd>jpg</dd><dt><span>time</span></dt><dd></dd><dt><span>tilematrixset</span></dt><dd>GoogleMapsCompatible_Level</dd><dt><span>variant</span></dt><dd>MODIS_Terra_CorrectedReflectance_TrueColor</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="eddc67fe-b23b-4091-b284-fb563932138d" class="xyz-checkbox"/>
                    <label for="eddc67fe-b23b-4091-b284-fb563932138d">ModisTerraBands367CR <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.ModisTerraBands367CR</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://map1.vis.earthdata.nasa.gov/wmts-webmerc/{variant}/default/{time}/{tilematrixset}{max_zoom}/{z}/{y}/{x}.{format}</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>bounds</span></dt><dd>[[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]]</dd><dt><span>min_zoom</span></dt><dd>1</dd><dt><span>max_zoom</span></dt><dd>9</dd><dt><span>format</span></dt><dd>jpg</dd><dt><span>time</span></dt><dd></dd><dt><span>tilematrixset</span></dt><dd>GoogleMapsCompatible_Level</dd><dt><span>variant</span></dt><dd>MODIS_Terra_CorrectedReflectance_Bands367</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f6c6db3a-9426-4649-8d94-6fa2c1af5cb0" class="xyz-checkbox"/>
                    <label for="f6c6db3a-9426-4649-8d94-6fa2c1af5cb0">ViirsEarthAtNight2012 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.ViirsEarthAtNight2012</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://map1.vis.earthdata.nasa.gov/wmts-webmerc/{variant}/default/{time}/{tilematrixset}{max_zoom}/{z}/{y}/{x}.{format}</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>bounds</span></dt><dd>[[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]]</dd><dt><span>min_zoom</span></dt><dd>1</dd><dt><span>max_zoom</span></dt><dd>8</dd><dt><span>format</span></dt><dd>jpg</dd><dt><span>time</span></dt><dd></dd><dt><span>tilematrixset</span></dt><dd>GoogleMapsCompatible_Level</dd><dt><span>variant</span></dt><dd>VIIRS_CityLights_2012</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="09acdfb0-b7f7-4109-b835-17c255a2997a" class="xyz-checkbox"/>
                    <label for="09acdfb0-b7f7-4109-b835-17c255a2997a">ModisTerraLSTDay <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.ModisTerraLSTDay</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://map1.vis.earthdata.nasa.gov/wmts-webmerc/{variant}/default/{time}/{tilematrixset}{max_zoom}/{z}/{y}/{x}.{format}</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>bounds</span></dt><dd>[[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]]</dd><dt><span>min_zoom</span></dt><dd>1</dd><dt><span>max_zoom</span></dt><dd>7</dd><dt><span>format</span></dt><dd>png</dd><dt><span>time</span></dt><dd></dd><dt><span>tilematrixset</span></dt><dd>GoogleMapsCompatible_Level</dd><dt><span>variant</span></dt><dd>MODIS_Terra_Land_Surface_Temp_Day</dd><dt><span>opacity</span></dt><dd>0.75</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2682eb09-292d-4b29-b7bd-09f3ac920b8d" class="xyz-checkbox"/>
                    <label for="2682eb09-292d-4b29-b7bd-09f3ac920b8d">ModisTerraSnowCover <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.ModisTerraSnowCover</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://map1.vis.earthdata.nasa.gov/wmts-webmerc/{variant}/default/{time}/{tilematrixset}{max_zoom}/{z}/{y}/{x}.{format}</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>bounds</span></dt><dd>[[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]]</dd><dt><span>min_zoom</span></dt><dd>1</dd><dt><span>max_zoom</span></dt><dd>8</dd><dt><span>format</span></dt><dd>png</dd><dt><span>time</span></dt><dd></dd><dt><span>tilematrixset</span></dt><dd>GoogleMapsCompatible_Level</dd><dt><span>variant</span></dt><dd>MODIS_Terra_NDSI_Snow_Cover</dd><dt><span>opacity</span></dt><dd>0.75</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3cc8cd8f-add4-4722-9765-c4e9a9569e92" class="xyz-checkbox"/>
                    <label for="3cc8cd8f-add4-4722-9765-c4e9a9569e92">ModisTerraAOD <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.ModisTerraAOD</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://map1.vis.earthdata.nasa.gov/wmts-webmerc/{variant}/default/{time}/{tilematrixset}{max_zoom}/{z}/{y}/{x}.{format}</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>bounds</span></dt><dd>[[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]]</dd><dt><span>min_zoom</span></dt><dd>1</dd><dt><span>max_zoom</span></dt><dd>6</dd><dt><span>format</span></dt><dd>png</dd><dt><span>time</span></dt><dd></dd><dt><span>tilematrixset</span></dt><dd>GoogleMapsCompatible_Level</dd><dt><span>variant</span></dt><dd>MODIS_Terra_Aerosol</dd><dt><span>opacity</span></dt><dd>0.75</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4f69d488-e4f4-4db4-be26-bdb42c57f010" class="xyz-checkbox"/>
                    <label for="4f69d488-e4f4-4db4-be26-bdb42c57f010">ModisTerraChlorophyll <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.ModisTerraChlorophyll</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://map1.vis.earthdata.nasa.gov/wmts-webmerc/{variant}/default/{time}/{tilematrixset}{max_zoom}/{z}/{y}/{x}.{format}</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>bounds</span></dt><dd>[[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]]</dd><dt><span>min_zoom</span></dt><dd>1</dd><dt><span>max_zoom</span></dt><dd>7</dd><dt><span>format</span></dt><dd>png</dd><dt><span>time</span></dt><dd></dd><dt><span>tilematrixset</span></dt><dd>GoogleMapsCompatible_Level</dd><dt><span>variant</span></dt><dd>MODIS_Terra_Chlorophyll_A</dd><dt><span>opacity</span></dt><dd>0.75</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="734baf8f-c6a8-4918-a75f-c77221e5513f" class="xyz-checkbox"/>
                    <label for="734baf8f-c6a8-4918-a75f-c77221e5513f">ModisTerraBands721CR <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.ModisTerraBands721CR</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MODIS_Terra_CorrectedReflectance_Bands721/default/{time}/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg</dd><dt><span>max_zoom</span></dt><dd>9</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd><dt><span>time</span></dt><dd></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e7a2fd5e-955c-43a1-9354-7f40600c40c9" class="xyz-checkbox"/>
                    <label for="e7a2fd5e-955c-43a1-9354-7f40600c40c9">ModisAquaTrueColorCR <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.ModisAquaTrueColorCR</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MODIS_Aqua_CorrectedReflectance_TrueColor/default/{time}/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg</dd><dt><span>max_zoom</span></dt><dd>9</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd><dt><span>time</span></dt><dd></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9e6a255f-a4d1-4f92-a7ad-2f5321ab4b6f" class="xyz-checkbox"/>
                    <label for="9e6a255f-a4d1-4f92-a7ad-2f5321ab4b6f">ModisAquaBands721CR <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.ModisAquaBands721CR</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MODIS_Aqua_CorrectedReflectance_Bands721/default/{time}/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg</dd><dt><span>max_zoom</span></dt><dd>9</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd><dt><span>time</span></dt><dd></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="121e0435-c15d-452e-9636-9f8cb7fb56b7" class="xyz-checkbox"/>
                    <label for="121e0435-c15d-452e-9636-9f8cb7fb56b7">ViirsTrueColorCR <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.ViirsTrueColorCR</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/VIIRS_SNPP_CorrectedReflectance_TrueColor/default/{time}/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg</dd><dt><span>max_zoom</span></dt><dd>9</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd><dt><span>time</span></dt><dd></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3cf6bf35-7416-4d5f-a685-3a8aa1f1a3a2" class="xyz-checkbox"/>
                    <label for="3cf6bf35-7416-4d5f-a685-3a8aa1f1a3a2">BlueMarble3413 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.BlueMarble3413</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://gibs.earthdata.nasa.gov/wmts/epsg3413/best/BlueMarble_NextGeneration/default/EPSG3413_500m/{z}/{y}/{x}.jpeg</dd><dt><span>max_zoom</span></dt><dd>5</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd><dt><span>crs</span></dt><dd>EPSG:3413</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9d168d19-fdf3-407f-8942-83cee0c5ff04" class="xyz-checkbox"/>
                    <label for="9d168d19-fdf3-407f-8942-83cee0c5ff04">BlueMarble3031 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.BlueMarble3031</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://gibs.earthdata.nasa.gov/wmts/epsg3031/best/BlueMarble_NextGeneration/default/EPSG3031_500m/{z}/{y}/{x}.jpeg</dd><dt><span>max_zoom</span></dt><dd>5</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd><dt><span>crs</span></dt><dd>EPSG:3031</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cd784cf3-0580-4cff-bb09-452bbe56325b" class="xyz-checkbox"/>
                    <label for="cd784cf3-0580-4cff-bb09-452bbe56325b">BlueMarble <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.BlueMarble</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/BlueMarble_NextGeneration/default/EPSG3857_500m/{z}/{y}/{x}.jpeg</dd><dt><span>max_zoom</span></dt><dd>8</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cff4a103-d666-4fa7-9da7-19dd24fa23f8" class="xyz-checkbox"/>
                    <label for="cff4a103-d666-4fa7-9da7-19dd24fa23f8">ASTER_GDEM_Greyscale_Shaded_Relief <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NASAGIBS.ASTER_GDEM_Greyscale_Shaded_Relief</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/ASTER_GDEM_Greyscale_Shaded_Relief/default/GoogleMapsCompatible_Level12/{z}/{y}/{x}.jpg</dd><dt><span>max_zoom</span></dt><dd>12</dd><dt><span>attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (ESDIS) with funding provided by NASA/HQ.</dd><dt><span>html_attribution</span></dt><dd>Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5910217f-a3c5-496c-a6bb-2ec27e134ca5" class="xyz-checkbox"/>
                    <label for="5910217f-a3c5-496c-a6bb-2ec27e134ca5">NLS <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">NLS</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://nls-{s}.tileserver.com/nls/{z}/{x}/{y}.jpg</dd><dt><span>html_attribution</span></dt><dd><a href="http://geo.nls.uk/maps/">National Library of Scotland Historic Maps</a></dd><dt><span>attribution</span></dt><dd>National Library of Scotland Historic Maps</dd><dt><span>bounds</span></dt><dd>[[49.6, -12], [61.7, 3]]</dd><dt><span>min_zoom</span></dt><dd>1</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>subdomains</span></dt><dd>0123</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a49d2212-c8c7-446b-8072-677a334ed770" class="xyz-checkbox"/>
                    <label for="a49d2212-c8c7-446b-8072-677a334ed770">JusticeMap <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">9 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="10e8ce53-dec9-457d-bb19-906477c35ce5" class="xyz-checkbox"/>
                    <label for="10e8ce53-dec9-457d-bb19-906477c35ce5">income <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">JusticeMap.income</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://www.justicemap.org/tile/{size}/{variant}/{z}/{x}/{y}.png</dd><dt><span>html_attribution</span></dt><dd><a href="http://www.justicemap.org/terms.php">Justice Map</a></dd><dt><span>attribution</span></dt><dd>Justice Map</dd><dt><span>size</span></dt><dd>county</dd><dt><span>bounds</span></dt><dd>[[14, -180], [72, -56]]</dd><dt><span>variant</span></dt><dd>income</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="53e8469e-e9a5-4900-af2e-6823e4d92136" class="xyz-checkbox"/>
                    <label for="53e8469e-e9a5-4900-af2e-6823e4d92136">americanIndian <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">JusticeMap.americanIndian</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://www.justicemap.org/tile/{size}/{variant}/{z}/{x}/{y}.png</dd><dt><span>html_attribution</span></dt><dd><a href="http://www.justicemap.org/terms.php">Justice Map</a></dd><dt><span>attribution</span></dt><dd>Justice Map</dd><dt><span>size</span></dt><dd>county</dd><dt><span>bounds</span></dt><dd>[[14, -180], [72, -56]]</dd><dt><span>variant</span></dt><dd>indian</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="20436999-3677-4089-b5c6-b572137837bf" class="xyz-checkbox"/>
                    <label for="20436999-3677-4089-b5c6-b572137837bf">asian <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">JusticeMap.asian</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://www.justicemap.org/tile/{size}/{variant}/{z}/{x}/{y}.png</dd><dt><span>html_attribution</span></dt><dd><a href="http://www.justicemap.org/terms.php">Justice Map</a></dd><dt><span>attribution</span></dt><dd>Justice Map</dd><dt><span>size</span></dt><dd>county</dd><dt><span>bounds</span></dt><dd>[[14, -180], [72, -56]]</dd><dt><span>variant</span></dt><dd>asian</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="065aa45b-e674-4704-9f53-d1f32efe96aa" class="xyz-checkbox"/>
                    <label for="065aa45b-e674-4704-9f53-d1f32efe96aa">black <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">JusticeMap.black</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://www.justicemap.org/tile/{size}/{variant}/{z}/{x}/{y}.png</dd><dt><span>html_attribution</span></dt><dd><a href="http://www.justicemap.org/terms.php">Justice Map</a></dd><dt><span>attribution</span></dt><dd>Justice Map</dd><dt><span>size</span></dt><dd>county</dd><dt><span>bounds</span></dt><dd>[[14, -180], [72, -56]]</dd><dt><span>variant</span></dt><dd>black</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2dfd1134-cf24-4028-b7f4-b4fa371be945" class="xyz-checkbox"/>
                    <label for="2dfd1134-cf24-4028-b7f4-b4fa371be945">hispanic <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">JusticeMap.hispanic</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://www.justicemap.org/tile/{size}/{variant}/{z}/{x}/{y}.png</dd><dt><span>html_attribution</span></dt><dd><a href="http://www.justicemap.org/terms.php">Justice Map</a></dd><dt><span>attribution</span></dt><dd>Justice Map</dd><dt><span>size</span></dt><dd>county</dd><dt><span>bounds</span></dt><dd>[[14, -180], [72, -56]]</dd><dt><span>variant</span></dt><dd>hispanic</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9a4c9781-f767-4007-9cdf-3c46bf0b48d2" class="xyz-checkbox"/>
                    <label for="9a4c9781-f767-4007-9cdf-3c46bf0b48d2">multi <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">JusticeMap.multi</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://www.justicemap.org/tile/{size}/{variant}/{z}/{x}/{y}.png</dd><dt><span>html_attribution</span></dt><dd><a href="http://www.justicemap.org/terms.php">Justice Map</a></dd><dt><span>attribution</span></dt><dd>Justice Map</dd><dt><span>size</span></dt><dd>county</dd><dt><span>bounds</span></dt><dd>[[14, -180], [72, -56]]</dd><dt><span>variant</span></dt><dd>multi</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ebca3751-ed18-45b5-90d1-b79c634a507d" class="xyz-checkbox"/>
                    <label for="ebca3751-ed18-45b5-90d1-b79c634a507d">nonWhite <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">JusticeMap.nonWhite</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://www.justicemap.org/tile/{size}/{variant}/{z}/{x}/{y}.png</dd><dt><span>html_attribution</span></dt><dd><a href="http://www.justicemap.org/terms.php">Justice Map</a></dd><dt><span>attribution</span></dt><dd>Justice Map</dd><dt><span>size</span></dt><dd>county</dd><dt><span>bounds</span></dt><dd>[[14, -180], [72, -56]]</dd><dt><span>variant</span></dt><dd>nonwhite</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ec788292-1e70-4e36-a541-17309b2a05bc" class="xyz-checkbox"/>
                    <label for="ec788292-1e70-4e36-a541-17309b2a05bc">white <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">JusticeMap.white</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://www.justicemap.org/tile/{size}/{variant}/{z}/{x}/{y}.png</dd><dt><span>html_attribution</span></dt><dd><a href="http://www.justicemap.org/terms.php">Justice Map</a></dd><dt><span>attribution</span></dt><dd>Justice Map</dd><dt><span>size</span></dt><dd>county</dd><dt><span>bounds</span></dt><dd>[[14, -180], [72, -56]]</dd><dt><span>variant</span></dt><dd>white</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="28e1228f-d9df-4919-9e6e-9b94905ebcd4" class="xyz-checkbox"/>
                    <label for="28e1228f-d9df-4919-9e6e-9b94905ebcd4">plurality <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">JusticeMap.plurality</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://www.justicemap.org/tile/{size}/{variant}/{z}/{x}/{y}.png</dd><dt><span>html_attribution</span></dt><dd><a href="http://www.justicemap.org/terms.php">Justice Map</a></dd><dt><span>attribution</span></dt><dd>Justice Map</dd><dt><span>size</span></dt><dd>county</dd><dt><span>bounds</span></dt><dd>[[14, -180], [72, -56]]</dd><dt><span>variant</span></dt><dd>plural</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="d963e651-f198-4330-912d-45b7c15e99cc" class="xyz-checkbox"/>
                    <label for="d963e651-f198-4330-912d-45b7c15e99cc">GeoportailFrance <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">271 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="71b8c886-2d5e-4c5f-86fa-514a26a46b17" class="xyz-checkbox"/>
                    <label for="71b8c886-2d5e-4c5f-86fa-514a26a46b17">plan <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.plan</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-85.0, -175.0], [85.0, 175.0]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>essentiels</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8fce3cb5-c861-4411-bc9d-d23c4ef3c9e4" class="xyz-checkbox"/>
                    <label for="8fce3cb5-c861-4411-bc9d-d23c4ef3c9e4">parcels <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.parcels</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>essentiels</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>CADASTRALPARCELS.PARCELLAIRE_EXPRESS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a4abdb3d-6a90-4072-a4da-d7f1a406d443" class="xyz-checkbox"/>
                    <label for="a4abdb3d-6a90-4072-a4da-d7f1a406d443">orthos <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.orthos</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>21</dd><dt><span>apikey</span></dt><dd>ortho</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ee6e6f3b-a32a-4a67-8c88-e083741d067e" class="xyz-checkbox"/>
                    <label for="ee6e6f3b-a32a-4a67-8c88-e083741d067e">Adminexpress_cog_carto_Latest <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Adminexpress_cog_carto_Latest</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>administratif</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ADMINEXPRESS-COG-CARTO.LATEST</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="68ad254b-2c12-456d-aa4a-e23342e4ce69" class="xyz-checkbox"/>
                    <label for="68ad254b-2c12-456d-aa4a-e23342e4ce69">Adminexpress_cog_Latest <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Adminexpress_cog_Latest</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>administratif</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ADMINEXPRESS-COG.LATEST</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b05fef53-5a6b-4cb6-877c-ab2b4a5088e0" class="xyz-checkbox"/>
                    <label for="b05fef53-5a6b-4cb6-877c-ab2b4a5088e0">Limites_administratives_express_Latest <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Limites_administratives_express_Latest</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>administratif</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LIMITES_ADMINISTRATIVES_EXPRESS.LATEST</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="24859ddc-d6c3-4a0e-856e-dd740088a6f8" class="xyz-checkbox"/>
                    <label for="24859ddc-d6c3-4a0e-856e-dd740088a6f8">Geographicalgridsystems_Slopes_Pac <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Geographicalgridsystems_Slopes_Pac</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.5446, -63.1614], [51.0991, 56.0018]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>15</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>GEOGRAPHICALGRIDSYSTEMS.SLOPES.PAC</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5e6c9a70-c670-437e-837f-6c951a40be54" class="xyz-checkbox"/>
                    <label for="5e6c9a70-c670-437e-837f-6c951a40be54">Hydrography_Bcae_Latest <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Hydrography_Bcae_Latest</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>HYDROGRAPHY.BCAE.LATEST</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b7afc9ae-a576-4851-8ffa-6ebadce04c8d" class="xyz-checkbox"/>
                    <label for="b7afc9ae-a576-4851-8ffa-6ebadce04c8d">Landuse_Agriculture_Latest <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture_Latest</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE.LATEST</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a7ec375d-e8e1-4165-ab4b-911c4189d78c" class="xyz-checkbox"/>
                    <label for="a7ec375d-e8e1-4165-ab4b-911c4189d78c">Landuse_Agriculture2007 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2007</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.419, -63.2635], [51.2203, 56.0237]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2007</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="581ff9a2-ce3f-41b5-8279-9a8250b02c11" class="xyz-checkbox"/>
                    <label for="581ff9a2-ce3f-41b5-8279-9a8250b02c11">Landuse_Agriculture2008 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2008</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.419, -63.2635], [51.2203, 56.0237]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2008</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="175feff5-a1de-4e78-9098-c5031b92a0e7" class="xyz-checkbox"/>
                    <label for="175feff5-a1de-4e78-9098-c5031b92a0e7">Landuse_Agriculture2009 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2009</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.419, -63.2635], [51.2203, 56.0237]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2009</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="41262218-69b3-4072-a711-8cf4bd29aa06" class="xyz-checkbox"/>
                    <label for="41262218-69b3-4072-a711-8cf4bd29aa06">Landuse_Agriculture2010 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2010</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2010</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="c32b2aa2-b984-4bea-91cf-ec1cc58fdfaa" class="xyz-checkbox"/>
                    <label for="c32b2aa2-b984-4bea-91cf-ec1cc58fdfaa">Landuse_Agriculture2011 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2011</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2011</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="dafda472-f662-4110-b4eb-087f77a12b5a" class="xyz-checkbox"/>
                    <label for="dafda472-f662-4110-b4eb-087f77a12b5a">Landuse_Agriculture2012 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2012</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2012</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ba9a4779-b265-4d3b-8c30-1b82ce058bc7" class="xyz-checkbox"/>
                    <label for="ba9a4779-b265-4d3b-8c30-1b82ce058bc7">Landuse_Agriculture2013 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2013</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2013</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="73215389-aeab-428d-8043-f6b41407c829" class="xyz-checkbox"/>
                    <label for="73215389-aeab-428d-8043-f6b41407c829">Landuse_Agriculture2014 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2014</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2014</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cb45b303-2e9b-469a-8144-efe5e69efdf1" class="xyz-checkbox"/>
                    <label for="cb45b303-2e9b-469a-8144-efe5e69efdf1">Landuse_Agriculture2015 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2015</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2015</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="1ecb8dc6-cd9e-4d5d-b2c0-70f4b8f25824" class="xyz-checkbox"/>
                    <label for="1ecb8dc6-cd9e-4d5d-b2c0-70f4b8f25824">Landuse_Agriculture2016 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2016</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2016</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f0188c66-5f49-4013-9fd9-1f57a1c478ac" class="xyz-checkbox"/>
                    <label for="f0188c66-5f49-4013-9fd9-1f57a1c478ac">Landuse_Agriculture2017 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2017</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2017</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2bbd2cc1-988c-4933-8ad3-5e25da44e6b4" class="xyz-checkbox"/>
                    <label for="2bbd2cc1-988c-4933-8ad3-5e25da44e6b4">Landuse_Agriculture2018 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2018</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2018</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cc6c70e8-00af-41d2-a8c7-3e830c872421" class="xyz-checkbox"/>
                    <label for="cc6c70e8-00af-41d2-a8c7-3e830c872421">Landuse_Agriculture2019 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2019</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2019</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3c2f857a-fd1d-4e19-8ba9-db39e952b7b1" class="xyz-checkbox"/>
                    <label for="3c2f857a-fd1d-4e19-8ba9-db39e952b7b1">Landuse_Agriculture2020 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2020</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2020</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5d4e6bee-2c59-4668-8f9f-40e37249b4b6" class="xyz-checkbox"/>
                    <label for="5d4e6bee-2c59-4668-8f9f-40e37249b4b6">Landuse_Agriculture2021 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landuse_Agriculture2021</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDUSE.AGRICULTURE2021</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="38426b1e-a2e9-4574-a863-2153e57d8f82" class="xyz-checkbox"/>
                    <label for="38426b1e-a2e9-4574-a863-2153e57d8f82">Prairies_Sensibles_Bcae <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Prairies_Sensibles_Bcae</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>agriculture</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>PRAIRIES.SENSIBLES.BCAE</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="40a0534f-4697-4b41-824c-35145afb8d3c" class="xyz-checkbox"/>
                    <label for="40a0534f-4697-4b41-824c-35145afb8d3c">Elevation_Contour_Line <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Elevation_Contour_Line</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>altimetrie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ELEVATION.CONTOUR.LINE</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="eb0366b1-67b2-4aa6-a67f-63ebb8214ae7" class="xyz-checkbox"/>
                    <label for="eb0366b1-67b2-4aa6-a67f-63ebb8214ae7">Elevation_Elevationgridcoverage_Shadow <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Elevation_Elevationgridcoverage_Shadow</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4069, -63.187], [50.9218, 55.8884]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>15</dd><dt><span>apikey</span></dt><dd>altimetrie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>estompage_grayscale</dd><dt><span>variant</span></dt><dd>ELEVATION.ELEVATIONGRIDCOVERAGE.SHADOW</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="237dfa28-f2e2-431c-b391-72be118eff88" class="xyz-checkbox"/>
                    <label for="237dfa28-f2e2-431c-b391-72be118eff88">Elevation_Elevationgridcoverage_Threshold <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Elevation_Elevationgridcoverage_Threshold</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>3</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>altimetrie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>ELEVATION.ELEVATIONGRIDCOVERAGE.THRESHOLD</dd><dt><span>variant</span></dt><dd>ELEVATION.ELEVATIONGRIDCOVERAGE.THRESHOLD</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="6a719ad7-0c77-48cd-91f2-4c96ff6c95c6" class="xyz-checkbox"/>
                    <label for="6a719ad7-0c77-48cd-91f2-4c96ff6c95c6">Elevation_Level0 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Elevation_Level0</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.51, -63.2529], [51.1388, 55.9472]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>altimetrie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ELEVATION.LEVEL0</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cdb2d824-a934-4a13-b1ec-b5dcf55aded0" class="xyz-checkbox"/>
                    <label for="cdb2d824-a934-4a13-b1ec-b5dcf55aded0">Elevation_Slopes <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Elevation_Slopes</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-22.5952, -178.206], [50.9308, 167.432]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>14</dd><dt><span>apikey</span></dt><dd>altimetrie</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ELEVATION.SLOPES</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="343d160f-fccb-44a1-b2c9-5e6dc5ba34b6" class="xyz-checkbox"/>
                    <label for="343d160f-fccb-44a1-b2c9-5e6dc5ba34b6">Elevationgridcoverage_Highres_Quality <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Elevationgridcoverage_Highres_Quality</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>altimetrie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>Graphe de source du RGE Alti</dd><dt><span>variant</span></dt><dd>ELEVATIONGRIDCOVERAGE.HIGHRES.QUALITY</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="21e6f549-3f20-433b-ae75-9ec15bfe76cf" class="xyz-checkbox"/>
                    <label for="21e6f549-3f20-433b-ae75-9ec15bfe76cf">Geographicalgridsystems_Slopes_Mountain <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Geographicalgridsystems_Slopes_Mountain</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.5446, -63.1614], [51.0991, 56.0018]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>altimetrie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>GEOGRAPHICALGRIDSYSTEMS.SLOPES.MOUNTAIN</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0c52b912-1c37-4bbf-bdde-c147d7f94cf0" class="xyz-checkbox"/>
                    <label for="0c52b912-1c37-4bbf-bdde-c147d7f94cf0">Geographicalgridsystems_1900typemaps <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Geographicalgridsystems_1900typemaps</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[48.4726, 1.62941], [49.1548, 3.0]]</dd><dt><span>min_zoom</span></dt><dd>10</dd><dt><span>max_zoom</span></dt><dd>15</dd><dt><span>apikey</span></dt><dd>cartes</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>GEOGRAPHICALGRIDSYSTEMS.1900TYPEMAPS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9a74bb44-4caf-4266-be34-f62e7a50663b" class="xyz-checkbox"/>
                    <label for="9a74bb44-4caf-4266-be34-f62e7a50663b">Geographicalgridsystems_Bonne <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Geographicalgridsystems_Bonne</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-0.49941, -55.9127], [7.88966, -50.0835]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>10</dd><dt><span>apikey</span></dt><dd>cartes</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>GEOGRAPHICALGRIDSYSTEMS.BONNE</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="919ee1ac-d24b-46f8-87e1-5a4dad73a456" class="xyz-checkbox"/>
                    <label for="919ee1ac-d24b-46f8-87e1-5a4dad73a456">Geographicalgridsystems_Etatmajor10 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Geographicalgridsystems_Etatmajor10</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[48.3847, 1.82682], [49.5142, 2.79738]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>cartes</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>GEOGRAPHICALGRIDSYSTEMS.ETATMAJOR10</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="487b7c32-4edc-4866-8f10-1b0fcafa5828" class="xyz-checkbox"/>
                    <label for="487b7c32-4edc-4866-8f10-1b0fcafa5828">Geographicalgridsystems_Etatmajor40 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Geographicalgridsystems_Etatmajor40</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.1844, -6.08889], [51.2745, 10.961]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>15</dd><dt><span>apikey</span></dt><dd>cartes</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>GEOGRAPHICALGRIDSYSTEMS.ETATMAJOR40</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="643f73cd-03b1-4180-b0ab-7fa8bfab2b10" class="xyz-checkbox"/>
                    <label for="643f73cd-03b1-4180-b0ab-7fa8bfab2b10">Geographicalgridsystems_Maps_Bduni_J1 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Geographicalgridsystems_Maps_Bduni_J1</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>cartes</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>GEOGRAPHICALGRIDSYSTEMS.MAPS.BDUNI.J1</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3f2627a1-b607-4aee-92de-341b24bcfd6e" class="xyz-checkbox"/>
                    <label for="3f2627a1-b607-4aee-92de-341b24bcfd6e">Geographicalgridsystems_Maps_Overview <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Geographicalgridsystems_Maps_Overview</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>1</dd><dt><span>max_zoom</span></dt><dd>8</dd><dt><span>apikey</span></dt><dd>cartes</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>GEOGRAPHICALGRIDSYSTEMS.MAPS.OVERVIEW</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="df172d84-fd91-4f63-a42a-00e2d4150178" class="xyz-checkbox"/>
                    <label for="df172d84-fd91-4f63-a42a-00e2d4150178">Geographicalgridsystems_Maps_Scan50_1950 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Geographicalgridsystems_Maps_Scan50_1950</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>3</dd><dt><span>max_zoom</span></dt><dd>15</dd><dt><span>apikey</span></dt><dd>cartes</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>SCAN50_1950</dd><dt><span>variant</span></dt><dd>GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN50.1950</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="50e993c1-6e22-4dd1-8d5c-9fc6ff898288" class="xyz-checkbox"/>
                    <label for="50e993c1-6e22-4dd1-8d5c-9fc6ff898288">Geographicalgridsystems_Terrier_v1 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Geographicalgridsystems_Terrier_v1</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.2568, 8.36284], [43.1174, 9.75281]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>cartes</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>GEOGRAPHICALGRIDSYSTEMS.TERRIER_V1</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f4265683-cb62-4b10-88f0-6b6a9bf6f813" class="xyz-checkbox"/>
                    <label for="f4265683-cb62-4b10-88f0-6b6a9bf6f813">Geographicalgridsystems_Terrier_v2 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Geographicalgridsystems_Terrier_v2</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.2568, 8.36284], [43.1174, 9.75282]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>cartes</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>GEOGRAPHICALGRIDSYSTEMS.TERRIER_V2</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="acdce3e9-2754-4bff-a44e-fa9ffb1c745d" class="xyz-checkbox"/>
                    <label for="acdce3e9-2754-4bff-a44e-fa9ffb1c745d">Landcover_Cha00_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Cha00_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[40.576, -9.88147], [51.4428, 11.6781]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.CHA00_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="d80da576-434a-4483-8891-324df9c2ae0c" class="xyz-checkbox"/>
                    <label for="d80da576-434a-4483-8891-324df9c2ae0c">Landcover_Cha06_dom <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Cha06_dom</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [47.1747, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - DOM</dd><dt><span>variant</span></dt><dd>LANDCOVER.CHA06_DOM</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="533f61c9-710a-4d48-be5e-7cb263d634d8" class="xyz-checkbox"/>
                    <label for="533f61c9-710a-4d48-be5e-7cb263d634d8">Landcover_Cha06_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Cha06_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[40.576, -9.88147], [51.4428, 11.6781]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.CHA06_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f052f5a6-2632-4510-a203-a51c6036b68f" class="xyz-checkbox"/>
                    <label for="f052f5a6-2632-4510-a203-a51c6036b68f">Landcover_Cha12_dom <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Cha12_dom</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [47.1747, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - DOM</dd><dt><span>variant</span></dt><dd>LANDCOVER.CHA12_DOM</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="eb2fc59d-b1be-4beb-b319-fbe9e6c7d653" class="xyz-checkbox"/>
                    <label for="eb2fc59d-b1be-4beb-b319-fbe9e6c7d653">Landcover_Cha12_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Cha12_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[40.576, -9.88147], [51.4428, 11.6781]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.CHA12_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="833fd8cc-953f-4cc6-a320-92f73c583eca" class="xyz-checkbox"/>
                    <label for="833fd8cc-953f-4cc6-a320-92f73c583eca">Landcover_Cha18 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Cha18</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.4428, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover</dd><dt><span>variant</span></dt><dd>LANDCOVER.CHA18</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="89106d52-8d4c-43d2-af02-534f3b967c89" class="xyz-checkbox"/>
                    <label for="89106d52-8d4c-43d2-af02-534f3b967c89">Landcover_Cha18_dom <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Cha18_dom</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [47.1747, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - DOM</dd><dt><span>variant</span></dt><dd>LANDCOVER.CHA18_DOM</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="df88c9a9-af8d-48e4-994f-4f0d2a0de7ba" class="xyz-checkbox"/>
                    <label for="df88c9a9-af8d-48e4-994f-4f0d2a0de7ba">Landcover_Cha18_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Cha18_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[40.576, -9.88147], [51.4428, 11.6781]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.CHA18_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="bba5b088-a47c-4d9f-857f-c4ed9848cd7f" class="xyz-checkbox"/>
                    <label for="bba5b088-a47c-4d9f-857f-c4ed9848cd7f">Landcover_Clc00r_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc00r_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[40.576, -9.88147], [51.4428, 11.6781]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC00R_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9abea853-ad15-4c1f-97a3-d8131d381d05" class="xyz-checkbox"/>
                    <label for="9abea853-ad15-4c1f-97a3-d8131d381d05">Landcover_Clc00_dom <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc00_dom</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [47.1747, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - DOM</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC00_DOM</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5ff0bfee-ae78-449d-8498-056801153012" class="xyz-checkbox"/>
                    <label for="5ff0bfee-ae78-449d-8498-056801153012">Landcover_Clc00_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc00_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[40.576, -9.88147], [51.4428, 11.6781]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC00_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="993ab266-91f1-452d-b4a4-7326f6be1238" class="xyz-checkbox"/>
                    <label for="993ab266-91f1-452d-b4a4-7326f6be1238">Landcover_Clc06r_dom <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc06r_dom</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [47.1747, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - DOM</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC06R_DOM</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="bb88d8be-7a94-49a3-a3ae-423271960456" class="xyz-checkbox"/>
                    <label for="bb88d8be-7a94-49a3-a3ae-423271960456">Landcover_Clc06r_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc06r_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[40.576, -9.88147], [51.4428, 11.6781]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC06R_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e1516fcc-be28-49d1-bf22-e2b4aa0e9460" class="xyz-checkbox"/>
                    <label for="e1516fcc-be28-49d1-bf22-e2b4aa0e9460">Landcover_Clc06_dom <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc06_dom</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [47.1747, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - DOM</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC06_DOM</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a6d61b18-80c3-493a-ac6d-fbb63b00ca63" class="xyz-checkbox"/>
                    <label for="a6d61b18-80c3-493a-ac6d-fbb63b00ca63">Landcover_Clc06_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc06_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[40.576, -9.88147], [51.4428, 11.6781]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC06_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f3359a21-6185-472f-8f5d-908472ab4025" class="xyz-checkbox"/>
                    <label for="f3359a21-6185-472f-8f5d-908472ab4025">Landcover_Clc12 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc12</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.4428, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - DOM</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC12</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9a230c32-223a-40ec-9c7b-d487070e0e41" class="xyz-checkbox"/>
                    <label for="9a230c32-223a-40ec-9c7b-d487070e0e41">Landcover_Clc12r <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc12r</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.4428, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC12R</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="19a09ef0-bfc8-4c7b-9f5e-5c9aebcfb204" class="xyz-checkbox"/>
                    <label for="19a09ef0-bfc8-4c7b-9f5e-5c9aebcfb204">Landcover_Clc12r_dom <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc12r_dom</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [47.1747, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - DOM</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC12R_DOM</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f48ccf83-11ae-4719-b706-1709e299e6cc" class="xyz-checkbox"/>
                    <label for="f48ccf83-11ae-4719-b706-1709e299e6cc">Landcover_Clc12r_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc12r_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[40.576, -9.88147], [51.4428, 11.6781]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC12R_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e79e02b3-69b1-42ff-ac7e-d3ee5b1b6dfd" class="xyz-checkbox"/>
                    <label for="e79e02b3-69b1-42ff-ac7e-d3ee5b1b6dfd">Landcover_Clc12_dom <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc12_dom</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [47.1747, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - DOM</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC12_DOM</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="38f9ba36-3fd9-4158-b862-1e6ebe46a6fc" class="xyz-checkbox"/>
                    <label for="38f9ba36-3fd9-4158-b862-1e6ebe46a6fc">Landcover_Clc12_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc12_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[40.576, -9.88147], [51.4428, 11.6781]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC12_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="c70c085e-c397-4fd4-b958-00dd4c78cfd8" class="xyz-checkbox"/>
                    <label for="c70c085e-c397-4fd4-b958-00dd4c78cfd8">Landcover_Clc18 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc18</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.4428, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC18</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="c65a7465-d22f-406f-8e0a-6e86b92ce1be" class="xyz-checkbox"/>
                    <label for="c65a7465-d22f-406f-8e0a-6e86b92ce1be">Landcover_Clc18_dom <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc18_dom</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [47.1747, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - DOM</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC18_DOM</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="42ff7452-e9b1-48f9-be35-10a9f37e7928" class="xyz-checkbox"/>
                    <label for="42ff7452-e9b1-48f9-be35-10a9f37e7928">Landcover_Clc18_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc18_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[40.576, -9.88147], [51.4428, 11.6781]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC18_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="67c9ce41-baf7-4e8d-87f3-0d2098777f70" class="xyz-checkbox"/>
                    <label for="67c9ce41-baf7-4e8d-87f3-0d2098777f70">Landcover_Clc90_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Clc90_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[40.576, -9.88147], [51.4428, 11.6781]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.CLC90_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ce1198a7-77a3-4030-a8af-2ff369d2d80f" class="xyz-checkbox"/>
                    <label for="ce1198a7-77a3-4030-a8af-2ff369d2d80f">Landcover_Grid_Clc00 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Grid_Clc00</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4825, -61.9063], [51.1827, 55.9362]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>13</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover</dd><dt><span>variant</span></dt><dd>LANDCOVER.GRID.CLC00</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5c83fba4-f591-4d53-a629-2449f65ea5a7" class="xyz-checkbox"/>
                    <label for="5c83fba4-f591-4d53-a629-2449f65ea5a7">Landcover_Grid_Clc00r_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Grid_Clc00r_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.1779, -5.68494], [51.1827, 10.8556]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>13</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.GRID.CLC00R_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="68fd5584-73e5-411a-968b-35f9b960d190" class="xyz-checkbox"/>
                    <label for="68fd5584-73e5-411a-968b-35f9b960d190">Landcover_Grid_Clc00_dom <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Grid_Clc00_dom</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4825, -61.9063], [16.6077, 55.9362]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>12</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - DOM</dd><dt><span>variant</span></dt><dd>LANDCOVER.GRID.CLC00_DOM</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="c189ee95-c8a7-4856-9bcc-efa86113cfd5" class="xyz-checkbox"/>
                    <label for="c189ee95-c8a7-4856-9bcc-efa86113cfd5">Landcover_Grid_Clc00_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Grid_Clc00_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.1779, -5.68494], [51.1827, 10.8556]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>12</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.GRID.CLC00_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="1ed81660-7acd-4eb6-8dee-36c4a44a65aa" class="xyz-checkbox"/>
                    <label for="1ed81660-7acd-4eb6-8dee-36c4a44a65aa">Landcover_Grid_Clc06 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Grid_Clc06</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4825, -61.9063], [51.1827, 55.9362]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>13</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover</dd><dt><span>variant</span></dt><dd>LANDCOVER.GRID.CLC06</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f67f4f92-38b8-4a7d-ba1b-03ae0ee5b414" class="xyz-checkbox"/>
                    <label for="f67f4f92-38b8-4a7d-ba1b-03ae0ee5b414">Landcover_Grid_Clc06r <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Grid_Clc06r</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4825, -61.9063], [51.2963, 55.9362]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>13</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover</dd><dt><span>variant</span></dt><dd>LANDCOVER.GRID.CLC06R</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3a90cb4d-90ce-49ef-ae00-836fc967dcc5" class="xyz-checkbox"/>
                    <label for="3a90cb4d-90ce-49ef-ae00-836fc967dcc5">Landcover_Grid_Clc06r_dom <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Grid_Clc06r_dom</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4825, -61.9063], [16.6077, 55.9362]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>12</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - DOM</dd><dt><span>variant</span></dt><dd>LANDCOVER.GRID.CLC06R_DOM</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4d36dc59-7d88-4e9b-8337-8eb3aa4da6f0" class="xyz-checkbox"/>
                    <label for="4d36dc59-7d88-4e9b-8337-8eb3aa4da6f0">Landcover_Grid_Clc06r_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Grid_Clc06r_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.0278, -5.91689], [51.2963, 11.0883]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>12</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.GRID.CLC06R_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="20b17971-72a5-426b-ad4b-75e1d3c2d244" class="xyz-checkbox"/>
                    <label for="20b17971-72a5-426b-ad4b-75e1d3c2d244">Landcover_Grid_Clc06_dom <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Grid_Clc06_dom</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4825, -61.9063], [16.6077, 55.9362]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>12</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - DOM</dd><dt><span>variant</span></dt><dd>LANDCOVER.GRID.CLC06_DOM</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4aa7af5e-b283-47cf-ad7e-5d9d669f5d16" class="xyz-checkbox"/>
                    <label for="4aa7af5e-b283-47cf-ad7e-5d9d669f5d16">Landcover_Grid_Clc06_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Grid_Clc06_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.1779, -5.68494], [51.1827, 10.8556]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>12</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.GRID.CLC06_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="d340b510-6e60-4dd6-bc6e-e05390457531" class="xyz-checkbox"/>
                    <label for="d340b510-6e60-4dd6-bc6e-e05390457531">Landcover_Grid_Clc12 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Grid_Clc12</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4825, -61.9063], [51.2963, 55.9362]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>13</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover</dd><dt><span>variant</span></dt><dd>LANDCOVER.GRID.CLC12</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="1bdd8275-8296-467d-9ea1-01f796918970" class="xyz-checkbox"/>
                    <label for="1bdd8275-8296-467d-9ea1-01f796918970">Landcover_Grid_Clc90_fr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Grid_Clc90_fr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.1779, -5.68494], [51.1827, 10.8556]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>13</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - France métropolitaine</dd><dt><span>variant</span></dt><dd>LANDCOVER.GRID.CLC90_FR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="36945ba0-0e4a-4578-8c23-fd5472c2d53a" class="xyz-checkbox"/>
                    <label for="36945ba0-0e4a-4578-8c23-fd5472c2d53a">Landcover_Hr_Dlt_Clc12 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Hr_Dlt_Clc12</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.572, -62.3602], [51.4949, 55.8441]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>13</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - HR - type de forêts</dd><dt><span>variant</span></dt><dd>LANDCOVER.HR.DLT.CLC12</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="d977dff6-7fc7-495c-a4ad-b184739b22de" class="xyz-checkbox"/>
                    <label for="d977dff6-7fc7-495c-a4ad-b184739b22de">Landcover_Hr_Dlt_Clc15 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Hr_Dlt_Clc15</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.572, -62.3602], [51.4949, 55.8441]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>13</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - HR - type de forêts</dd><dt><span>variant</span></dt><dd>LANDCOVER.HR.DLT.CLC15</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="262917e1-ef83-4e9d-aa83-64f8e9fbd95a" class="xyz-checkbox"/>
                    <label for="262917e1-ef83-4e9d-aa83-64f8e9fbd95a">Landcover_Hr_Gra_Clc15 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Hr_Gra_Clc15</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.3925, -61.8133], [51.4949, 55.84]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>13</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - HR - prairies</dd><dt><span>variant</span></dt><dd>LANDCOVER.HR.GRA.CLC15</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3860d50d-d99a-47fe-a345-63d80fa782d8" class="xyz-checkbox"/>
                    <label for="3860d50d-d99a-47fe-a345-63d80fa782d8">Landcover_Hr_Imd_Clc12 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Hr_Imd_Clc12</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.5758, -62.3609], [51.4952, 56.1791]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>13</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - HR - taux d'imperméabilisation des sols</dd><dt><span>variant</span></dt><dd>LANDCOVER.HR.IMD.CLC12</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="fa31467f-5acd-46c0-ad79-b978f51f942d" class="xyz-checkbox"/>
                    <label for="fa31467f-5acd-46c0-ad79-b978f51f942d">Landcover_Hr_Imd_Clc15 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Hr_Imd_Clc15</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.5758, -62.3609], [51.4952, 56.1791]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>13</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - HR - taux d'imperméabilisation des sols</dd><dt><span>variant</span></dt><dd>LANDCOVER.HR.IMD.CLC15</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b9a57fa4-2d42-470c-83ef-daff07d5f224" class="xyz-checkbox"/>
                    <label for="b9a57fa4-2d42-470c-83ef-daff07d5f224">Landcover_Hr_Tcd_Clc12 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Hr_Tcd_Clc12</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.572, -62.3602], [51.4949, 55.8441]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>13</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - HR - taux de couvert arboré</dd><dt><span>variant</span></dt><dd>LANDCOVER.HR.TCD.CLC12</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2c3464a6-9e2f-4cbf-80e9-be2409706f0a" class="xyz-checkbox"/>
                    <label for="2c3464a6-9e2f-4cbf-80e9-be2409706f0a">Landcover_Hr_Tcd_Clc15 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Hr_Tcd_Clc15</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.572, -62.3602], [51.4949, 55.8441]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>13</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - HR - taux de couvert arboré</dd><dt><span>variant</span></dt><dd>LANDCOVER.HR.TCD.CLC15</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="fc0250f0-dff6-479a-9ebe-6225894f9470" class="xyz-checkbox"/>
                    <label for="fc0250f0-dff6-479a-9ebe-6225894f9470">Landcover_Hr_Waw_Clc15 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Hr_Waw_Clc15</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.572, -62.3602], [51.4949, 55.8441]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>13</dd><dt><span>apikey</span></dt><dd>clc</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>CORINE Land Cover - HR - zones humides et surfaces en eaux permanentes</dd><dt><span>variant</span></dt><dd>LANDCOVER.HR.WAW.CLC15</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e506a8d0-4f27-4c1d-8296-6c2e2b567377" class="xyz-checkbox"/>
                    <label for="e506a8d0-4f27-4c1d-8296-6c2e2b567377">Areamanagement_Zfu <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Areamanagement_Zfu</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>AREAMANAGEMENT.ZFU</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ab70d8ae-b947-48bb-aa13-f82967fab4e1" class="xyz-checkbox"/>
                    <label for="ab70d8ae-b947-48bb-aa13-f82967fab4e1">Areamanagement_Zus <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Areamanagement_Zus</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>AREAMANAGEMENT.ZUS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="984f76ca-ae75-40bb-8724-f24afe6b17a9" class="xyz-checkbox"/>
                    <label for="984f76ca-ae75-40bb-8724-f24afe6b17a9">Communes_Prioritydisctrict <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Communes_Prioritydisctrict</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>COMMUNES.PRIORITYDISCTRICT</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="439a4b20-0e2f-4a15-9b93-edd50b8bdbb4" class="xyz-checkbox"/>
                    <label for="439a4b20-0e2f-4a15-9b93-edd50b8bdbb4">Dreal_Zonage_pinel <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Dreal_Zonage_pinel</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[47.2719, -5.15012], [48.9064, -1.00687]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>DREAL.ZONAGE_PINEL</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0e26bb63-39a1-47c6-a3ee-979866d57bcf" class="xyz-checkbox"/>
                    <label for="0e26bb63-39a1-47c6-a3ee-979866d57bcf">Insee_Filosofi_Enfants_0_17_Ans_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Enfants_0_17_Ans_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.ENFANTS.0.17.ANS.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="576d0e68-cc6f-4ea5-a973-1a9bd4f451b7" class="xyz-checkbox"/>
                    <label for="576d0e68-cc6f-4ea5-a973-1a9bd4f451b7">Insee_Filosofi_Logements_Surface_Moyenne_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Logements_Surface_Moyenne_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.LOGEMENTS.SURFACE.MOYENNE.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cd6bb19f-a53f-4087-8749-fe76ec029802" class="xyz-checkbox"/>
                    <label for="cd6bb19f-a53f-4087-8749-fe76ec029802">Insee_Filosofi_Niveau_De_Vie_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Niveau_De_Vie_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.NIVEAU.DE.VIE.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="82efec8b-424c-4e3e-af25-84e4870a2a3c" class="xyz-checkbox"/>
                    <label for="82efec8b-424c-4e3e-af25-84e4870a2a3c">Insee_Filosofi_Part_Familles_Monoparentales_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Familles_Monoparentales_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.FAMILLES.MONOPARENTALES.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a15240cf-078f-4bb7-8b4f-dd8aeb621ee1" class="xyz-checkbox"/>
                    <label for="a15240cf-078f-4bb7-8b4f-dd8aeb621ee1">Insee_Filosofi_Part_Individus_25_39_Ans_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Individus_25_39_Ans_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.INDIVIDUS.25.39.ANS.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e998ed6d-0ddc-4b48-9c7f-56184ac326d7" class="xyz-checkbox"/>
                    <label for="e998ed6d-0ddc-4b48-9c7f-56184ac326d7">Insee_Filosofi_Part_Individus_40_54_Ans_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Individus_40_54_Ans_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.INDIVIDUS.40.54.ANS.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f7e8eddd-3d6a-4d72-a761-0accd59a7d58" class="xyz-checkbox"/>
                    <label for="f7e8eddd-3d6a-4d72-a761-0accd59a7d58">Insee_Filosofi_Part_Individus_55_64_Ans_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Individus_55_64_Ans_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.INDIVIDUS.55.64.ANS.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a6180125-6e2e-44b9-842c-dd643ef10ba4" class="xyz-checkbox"/>
                    <label for="a6180125-6e2e-44b9-842c-dd643ef10ba4">Insee_Filosofi_Part_Logements_Apres_1990_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Logements_Apres_1990_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.LOGEMENTS.APRES.1990.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4e5fb8a7-84b5-4aa7-95f2-8714a3736a20" class="xyz-checkbox"/>
                    <label for="4e5fb8a7-84b5-4aa7-95f2-8714a3736a20">Insee_Filosofi_Part_Logements_Avant_1945_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Logements_Avant_1945_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.LOGEMENTS.AVANT.1945.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a7928e3a-ed1b-49ad-b098-fbd61a3f6d55" class="xyz-checkbox"/>
                    <label for="a7928e3a-ed1b-49ad-b098-fbd61a3f6d55">Insee_Filosofi_Part_Logements_Collectifs_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Logements_Collectifs_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.LOGEMENTS.COLLECTIFS.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="049e6f4d-936e-4cc9-9d34-cdaa7e50996a" class="xyz-checkbox"/>
                    <label for="049e6f4d-936e-4cc9-9d34-cdaa7e50996a">Insee_Filosofi_Part_Logements_Construits_1945_1970_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Logements_Construits_1945_1970_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.LOGEMENTS.CONSTRUITS.1945.1970.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="19b1e2a9-b73e-4ce9-a582-f7adde9119f3" class="xyz-checkbox"/>
                    <label for="19b1e2a9-b73e-4ce9-a582-f7adde9119f3">Insee_Filosofi_Part_Logements_Construits_1970_1990_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Logements_Construits_1970_1990_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.LOGEMENTS.CONSTRUITS.1970.1990.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="7c843adb-25be-4c47-9e13-879bd7df5c4f" class="xyz-checkbox"/>
                    <label for="7c843adb-25be-4c47-9e13-879bd7df5c4f">Insee_Filosofi_Part_Logements_Sociaux_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Logements_Sociaux_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.LOGEMENTS.SOCIAUX.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2b65396f-d2f0-40bd-bbfc-940aa6b4383d" class="xyz-checkbox"/>
                    <label for="2b65396f-d2f0-40bd-bbfc-940aa6b4383d">Insee_Filosofi_Part_Menages_1_Personne_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Menages_1_Personne_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.MENAGES.1.PERSONNE.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="06eb401b-33b4-4c09-9496-01cf6b8313a0" class="xyz-checkbox"/>
                    <label for="06eb401b-33b4-4c09-9496-01cf6b8313a0">Insee_Filosofi_Part_Menages_5_Personnes_Ouplus_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Menages_5_Personnes_Ouplus_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.MENAGES.5.PERSONNES.OUPLUS.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8c49f6d7-ac4b-4552-80b3-ea7e611a8562" class="xyz-checkbox"/>
                    <label for="8c49f6d7-ac4b-4552-80b3-ea7e611a8562">Insee_Filosofi_Part_Menages_Maison_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Menages_Maison_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.MENAGES.MAISON.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="79b96b84-831a-4b3a-83c9-07e296c91ced" class="xyz-checkbox"/>
                    <label for="79b96b84-831a-4b3a-83c9-07e296c91ced">Insee_Filosofi_Part_Menages_Pauvres_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Menages_Pauvres_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.MENAGES.PAUVRES.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="fcce70cd-147a-44b9-bbbe-aa9952565abe" class="xyz-checkbox"/>
                    <label for="fcce70cd-147a-44b9-bbbe-aa9952565abe">Insee_Filosofi_Part_Menages_Proprietaires_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Menages_Proprietaires_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.MENAGES.PROPRIETAIRES.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="1b5ade2a-7716-4ede-8964-d7c8ad1b4d06" class="xyz-checkbox"/>
                    <label for="1b5ade2a-7716-4ede-8964-d7c8ad1b4d06">Insee_Filosofi_Part_Plus_65_Ans_Secret <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Part_Plus_65_Ans_Secret</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.PART.PLUS.65.ANS.SECRET</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="be697232-7d48-40f7-9453-8ebb0741f4b4" class="xyz-checkbox"/>
                    <label for="be697232-7d48-40f7-9453-8ebb0741f4b4">Insee_Filosofi_Population <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Insee_Filosofi_Population</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>economie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>INSEE</dd><dt><span>variant</span></dt><dd>INSEE.FILOSOFI.POPULATION</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="bf0c17a5-fa3c-4faa-80d4-2e44085e189c" class="xyz-checkbox"/>
                    <label for="bf0c17a5-fa3c-4faa-80d4-2e44085e189c">Debroussaillement <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Debroussaillement</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>DEBROUSSAILLEMENT</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0e01f7a1-07f3-42c4-a254-9637d5bb8833" class="xyz-checkbox"/>
                    <label for="0e01f7a1-07f3-42c4-a254-9637d5bb8833">Forets_Publiques <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Forets_Publiques</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>3</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>FORETS PUBLIQUES ONF</dd><dt><span>variant</span></dt><dd>FORETS.PUBLIQUES</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="52a868c3-f3e5-4914-8a0f-005fc364e365" class="xyz-checkbox"/>
                    <label for="52a868c3-f3e5-4914-8a0f-005fc364e365">Geographicalgridsystem_Dfci <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Geographicalgridsystem_Dfci</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>GEOGRAPHICALGRIDSYSTEM.DFCI</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b94352b0-17ba-4060-a196-ea90d4882f76" class="xyz-checkbox"/>
                    <label for="b94352b0-17ba-4060-a196-ea90d4882f76">Landcover_Forestareas <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Forestareas</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDCOVER.FORESTAREAS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2eca3afb-fb29-4300-bcd8-084e40dfd859" class="xyz-checkbox"/>
                    <label for="2eca3afb-fb29-4300-bcd8-084e40dfd859">Landcover_Forestinventory_V1 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Forestinventory_V1</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDCOVER.FORESTINVENTORY.V1</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8b09ad71-f67b-46a7-b41e-ba29afe0210e" class="xyz-checkbox"/>
                    <label for="8b09ad71-f67b-46a7-b41e-ba29afe0210e">Landcover_Forestinventory_V2 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Forestinventory_V2</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDCOVER.FORESTINVENTORY.V2</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8511fdbb-e19e-4e3e-babe-d32fcf44abe0" class="xyz-checkbox"/>
                    <label for="8511fdbb-e19e-4e3e-babe-d32fcf44abe0">Landcover_Sylvoecoregions <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Sylvoecoregions</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDCOVER.SYLVOECOREGIONS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="12e96567-822e-429a-a2c6-ea13fed439e5" class="xyz-checkbox"/>
                    <label for="12e96567-822e-429a-a2c6-ea13fed439e5">Landcover_Sylvoecoregions_Alluvium <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Landcover_Sylvoecoregions_Alluvium</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>LANDCOVER.SYLVOECOREGIONS.ALLUVIUM</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4fee7656-6997-4471-ad69-e002725417b1" class="xyz-checkbox"/>
                    <label for="4fee7656-6997-4471-ad69-e002725417b1">Protectedareas_Apb <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Apb</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.APB</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="85b556f6-c082-4aa7-903a-f94ae0de8bec" class="xyz-checkbox"/>
                    <label for="85b556f6-c082-4aa7-903a-f94ae0de8bec">Protectedareas_Apg <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Apg</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.APG</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f45ceab8-dbaa-41ac-a041-42bdb20492d5" class="xyz-checkbox"/>
                    <label for="f45ceab8-dbaa-41ac-a041-42bdb20492d5">Protectedareas_Aphn <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Aphn</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-53.6279, -63.3725], [51.3121, 82.645]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.APHN</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="518dbfe3-90cf-4a05-8425-fde76a3646df" class="xyz-checkbox"/>
                    <label for="518dbfe3-90cf-4a05-8425-fde76a3646df">Protectedareas_Aplg <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Aplg</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-53.6279, -63.3725], [51.3121, 82.645]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.APLG</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2f7dbb08-fb5c-4264-92b1-576c8adf16e3" class="xyz-checkbox"/>
                    <label for="2f7dbb08-fb5c-4264-92b1-576c8adf16e3">Protectedareas_Bios <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Bios</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.BIOS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="040c25ad-5b3a-47a9-aa81-4b6b5807875f" class="xyz-checkbox"/>
                    <label for="040c25ad-5b3a-47a9-aa81-4b6b5807875f">Protectedareas_Gp <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Gp</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.GP</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f45cca3e-aa33-4b8d-9082-c6e3b032ad3b" class="xyz-checkbox"/>
                    <label for="f45cca3e-aa33-4b8d-9082-c6e3b032ad3b">Protectedareas_Inpg <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Inpg</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-53.6279, -63.3725], [51.3121, 82.645]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.INPG</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="bc66f59d-a40d-49cd-926b-6af97397c037" class="xyz-checkbox"/>
                    <label for="bc66f59d-a40d-49cd-926b-6af97397c037">Protectedareas_Mnhn_Cdl_Parcels <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Mnhn_Cdl_Parcels</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.MNHN.CDL.PARCELS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="30f23917-1e9a-4c83-8be0-4f5658499812" class="xyz-checkbox"/>
                    <label for="30f23917-1e9a-4c83-8be0-4f5658499812">Protectedareas_Mnhn_Cdl_Perimeter <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Mnhn_Cdl_Perimeter</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.MNHN.CDL.PERIMETER</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9ab70bab-27b0-43a1-9dae-ea5f4876a93f" class="xyz-checkbox"/>
                    <label for="9ab70bab-27b0-43a1-9dae-ea5f4876a93f">Protectedareas_Mnhn_Conservatoires <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Mnhn_Conservatoires</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.MNHN.CONSERVATOIRES</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="283b8e99-36dc-4c98-bbea-e1cbb1657071" class="xyz-checkbox"/>
                    <label for="283b8e99-36dc-4c98-bbea-e1cbb1657071">Protectedareas_Mnhn_Rn_Perimeter <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Mnhn_Rn_Perimeter</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-53.6279, -63.3725], [51.3121, 82.645]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.MNHN.RN.PERIMETER</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4fb801f0-92db-470f-96d3-988f115619d0" class="xyz-checkbox"/>
                    <label for="4fb801f0-92db-470f-96d3-988f115619d0">Protectedareas_Pn <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Pn</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.PN</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="56fd48a1-ad21-44be-9238-1e70e49d80b2" class="xyz-checkbox"/>
                    <label for="56fd48a1-ad21-44be-9238-1e70e49d80b2">Protectedareas_Pnm <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Pnm</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.PNM</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b108898e-d89b-49fe-8e10-13f092fdb4ef" class="xyz-checkbox"/>
                    <label for="b108898e-d89b-49fe-8e10-13f092fdb4ef">Protectedareas_Pnr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Pnr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.PNR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="de2cddbd-4fa8-4288-aa2c-dc71f471825f" class="xyz-checkbox"/>
                    <label for="de2cddbd-4fa8-4288-aa2c-dc71f471825f">Protectedareas_Prsf <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Prsf</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>POINT RENCONTRE SECOURS FORET</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.PRSF</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="edc17604-1479-4e0d-8bdb-7b8010ec72dd" class="xyz-checkbox"/>
                    <label for="edc17604-1479-4e0d-8bdb-7b8010ec72dd">Protectedareas_Ramsar <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Ramsar</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.RAMSAR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b6759d41-bef6-44e9-976d-89d8468dc79c" class="xyz-checkbox"/>
                    <label for="b6759d41-bef6-44e9-976d-89d8468dc79c">Protectedareas_Rb <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Rb</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.RB</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="05096619-ec1b-4029-aca7-064d4648244c" class="xyz-checkbox"/>
                    <label for="05096619-ec1b-4029-aca7-064d4648244c">Protectedareas_Ripn <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Ripn</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.RIPN</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e8d8a32c-9a98-49d1-93f2-05af65655335" class="xyz-checkbox"/>
                    <label for="e8d8a32c-9a98-49d1-93f2-05af65655335">Protectedareas_Rn <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Rn</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-53.6279, -63.3725], [51.3121, 82.645]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.RN</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3c7c0dc2-9893-4f97-9632-b893f99cb101" class="xyz-checkbox"/>
                    <label for="3c7c0dc2-9893-4f97-9632-b893f99cb101">Protectedareas_Rnc <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Rnc</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.RNC</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9fb5006f-965a-40e1-ad8b-6857d0bcb03c" class="xyz-checkbox"/>
                    <label for="9fb5006f-965a-40e1-ad8b-6857d0bcb03c">Protectedareas_Rncf <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Rncf</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.RNCF</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a680610e-e97c-4ac3-9727-457d6aaa0b6e" class="xyz-checkbox"/>
                    <label for="a680610e-e97c-4ac3-9727-457d6aaa0b6e">Protectedareas_Sic <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Sic</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.SIC</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b1d375d5-651c-44f3-965d-ef3f611f6fb7" class="xyz-checkbox"/>
                    <label for="b1d375d5-651c-44f3-965d-ef3f611f6fb7">Protectedareas_Znieff1 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Znieff1</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.ZNIEFF1</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2629ecb4-8bd3-47e9-90c1-9d1ca03670fe" class="xyz-checkbox"/>
                    <label for="2629ecb4-8bd3-47e9-90c1-9d1ca03670fe">Protectedareas_Znieff1_Sea <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Znieff1_Sea</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.ZNIEFF1.SEA</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2bcaa562-7c7f-4cdc-9005-2ccbbb23e252" class="xyz-checkbox"/>
                    <label for="2bcaa562-7c7f-4cdc-9005-2ccbbb23e252">Protectedareas_Znieff2 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Znieff2</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.ZNIEFF2</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="40bef62a-dd1b-42c0-897b-2f4020709e5b" class="xyz-checkbox"/>
                    <label for="40bef62a-dd1b-42c0-897b-2f4020709e5b">Protectedareas_Znieff2_Sea <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Znieff2_Sea</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.ZNIEFF2.SEA</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="309509bd-3f74-4338-9e90-7e7727f5f1f9" class="xyz-checkbox"/>
                    <label for="309509bd-3f74-4338-9e90-7e7727f5f1f9">Protectedareas_Zpr <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Zpr</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-53.6279, -63.3725], [51.3121, 82.645]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.ZPR</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3eb0d5d9-ed93-4557-b8cb-755d2f9bc7c4" class="xyz-checkbox"/>
                    <label for="3eb0d5d9-ed93-4557-b8cb-755d2f9bc7c4">Protectedareas_Zps <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedareas_Zps</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDAREAS.ZPS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8810a881-a5c1-47d1-8832-e0d24a693cb8" class="xyz-checkbox"/>
                    <label for="8810a881-a5c1-47d1-8832-e0d24a693cb8">Protectedsites_Mnhn_Reserves_regionales <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Protectedsites_Mnhn_Reserves_regionales</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>environnement</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PROTECTEDSITES.MNHN.RESERVES-REGIONALES</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="018c8140-47c2-410b-a6d7-c34507882003" class="xyz-checkbox"/>
                    <label for="018c8140-47c2-410b-a6d7-c34507882003">Ocsge_Constructions <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Constructions</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[14.2395, -61.6644], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>OCSGE.CONSTRUCTIONS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5a258629-e53c-46c0-9744-711523b7163a" class="xyz-checkbox"/>
                    <label for="5a258629-e53c-46c0-9744-711523b7163a">Ocsge_Constructions_2002 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Constructions_2002</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.366, -5.13902], [51.089, 9.55982]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.CONSTRUCTIONS.2002</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="dbf5063c-70dd-4107-b95d-3e543e2970ab" class="xyz-checkbox"/>
                    <label for="dbf5063c-70dd-4107-b95d-3e543e2970ab">Ocsge_Constructions_2010 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Constructions_2010</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.CONSTRUCTIONS.2010</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="79096d94-cf0b-45fa-a909-7bbb59345096" class="xyz-checkbox"/>
                    <label for="79096d94-cf0b-45fa-a909-7bbb59345096">Ocsge_Constructions_2011 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Constructions_2011</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.CONSTRUCTIONS.2011</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cfb5fc99-7868-406f-8f0f-229d392f3cf3" class="xyz-checkbox"/>
                    <label for="cfb5fc99-7868-406f-8f0f-229d392f3cf3">Ocsge_Constructions_2014 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Constructions_2014</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.366, -5.13902], [51.089, 9.55982]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.CONSTRUCTIONS.2014</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e059cd75-d174-469f-a63d-099d00168f8d" class="xyz-checkbox"/>
                    <label for="e059cd75-d174-469f-a63d-099d00168f8d">Ocsge_Constructions_2016 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Constructions_2016</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.CONSTRUCTIONS.2016</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8c72d2ff-8866-4941-8c95-5a2aecdc6ca9" class="xyz-checkbox"/>
                    <label for="8c72d2ff-8866-4941-8c95-5a2aecdc6ca9">Ocsge_Constructions_2017 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Constructions_2017</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[14.2395, -61.6644], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.CONSTRUCTIONS.2017</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0ffc778e-7c3f-4a4e-a322-fb21eaa03eba" class="xyz-checkbox"/>
                    <label for="0ffc778e-7c3f-4a4e-a322-fb21eaa03eba">Ocsge_Constructions_2019 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Constructions_2019</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[43.3043, -0.291052], [44.0864, 1.2122]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.CONSTRUCTIONS.2019</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8846c4db-90ca-44e6-afca-1dde1fbff765" class="xyz-checkbox"/>
                    <label for="8846c4db-90ca-44e6-afca-1dde1fbff765">Ocsge_Couverture <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Couverture</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[14.2395, -61.6644], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>OCSGE.COUVERTURE</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2863cfbc-f922-4c02-b20e-c9cb48d178fa" class="xyz-checkbox"/>
                    <label for="2863cfbc-f922-4c02-b20e-c9cb48d178fa">Ocsge_Couverture_2002 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Couverture_2002</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.366, -5.13902], [51.089, 9.55982]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>OCSGE.COUVERTURE.2002</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a6e32f07-e0a2-4ef4-b82a-e421cb835aca" class="xyz-checkbox"/>
                    <label for="a6e32f07-e0a2-4ef4-b82a-e421cb835aca">Ocsge_Couverture_2010 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Couverture_2010</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.COUVERTURE.2010</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="75a59ffb-73c9-482d-a0cf-40de329044fe" class="xyz-checkbox"/>
                    <label for="75a59ffb-73c9-482d-a0cf-40de329044fe">Ocsge_Couverture_2011 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Couverture_2011</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.COUVERTURE.2011</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8d605fef-01fa-4f91-bb4d-a70caca109ff" class="xyz-checkbox"/>
                    <label for="8d605fef-01fa-4f91-bb4d-a70caca109ff">Ocsge_Couverture_2014 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Couverture_2014</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.366, -5.13902], [51.089, 9.55982]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.COUVERTURE.2014</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a1bb76d5-3177-4811-98bb-d14cbe534943" class="xyz-checkbox"/>
                    <label for="a1bb76d5-3177-4811-98bb-d14cbe534943">Ocsge_Couverture_2016 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Couverture_2016</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.COUVERTURE.2016</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="58ac9380-d400-4dc6-a5d8-2e86039553cf" class="xyz-checkbox"/>
                    <label for="58ac9380-d400-4dc6-a5d8-2e86039553cf">Ocsge_Couverture_2017 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Couverture_2017</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[14.2395, -61.6644], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.COUVERTURE.2017</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="dca90b63-e087-47e7-8e13-ef6c88366197" class="xyz-checkbox"/>
                    <label for="dca90b63-e087-47e7-8e13-ef6c88366197">Ocsge_Couverture_2019 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Couverture_2019</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[43.3043, -0.291052], [44.0864, 1.2122]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.COUVERTURE.2019</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e5e87031-f333-42c8-a421-ae99f0d1fd52" class="xyz-checkbox"/>
                    <label for="e5e87031-f333-42c8-a421-ae99f0d1fd52">Ocsge_Usage <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Usage</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[14.2395, -61.6644], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>OCSGE.USAGE</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2a8ac00f-474a-410f-a0bb-367a0a1d9a88" class="xyz-checkbox"/>
                    <label for="2a8ac00f-474a-410f-a0bb-367a0a1d9a88">Ocsge_Usage_2002 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Usage_2002</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.366, -5.13902], [51.089, 9.55982]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>OCSGE.USAGE.2002</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="7230b99a-29bd-47b5-b2a7-0e6cad10c66f" class="xyz-checkbox"/>
                    <label for="7230b99a-29bd-47b5-b2a7-0e6cad10c66f">Ocsge_Usage_2010 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Usage_2010</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.USAGE.2010</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="767be19f-fd54-4955-b95e-203a5d36c43a" class="xyz-checkbox"/>
                    <label for="767be19f-fd54-4955-b95e-203a5d36c43a">Ocsge_Usage_2011 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Usage_2011</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.USAGE.2011</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4659cb6d-aee4-4785-a1d5-4332187f46a2" class="xyz-checkbox"/>
                    <label for="4659cb6d-aee4-4785-a1d5-4332187f46a2">Ocsge_Usage_2014 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Usage_2014</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.366, -5.13902], [51.089, 9.55982]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>OCSGE.USAGE.2014</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="c82dfc10-ee0a-426c-9652-5b5fb61c2d7c" class="xyz-checkbox"/>
                    <label for="c82dfc10-ee0a-426c-9652-5b5fb61c2d7c">Ocsge_Usage_2016 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Usage_2016</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.USAGE.2016</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ee30820e-255e-4107-9dc3-d0eb33ca1f7d" class="xyz-checkbox"/>
                    <label for="ee30820e-255e-4107-9dc3-d0eb33ca1f7d">Ocsge_Usage_2017 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Usage_2017</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[14.2395, -61.6644], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.USAGE.2017</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="1c82b30b-2e3b-428c-890b-8bf6b1596270" class="xyz-checkbox"/>
                    <label for="1c82b30b-2e3b-428c-890b-8bf6b1596270">Ocsge_Usage_2019 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Usage_2019</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[43.3043, -0.291052], [44.0864, 1.2122]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.USAGE.2019</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="efd6f1e1-526f-4766-b85d-32f68be8e808" class="xyz-checkbox"/>
                    <label for="efd6f1e1-526f-4766-b85d-32f68be8e808">Ocsge_Visu_2016 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Visu_2016</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[43.2815, -0.318517], [44.0543, 1.22575]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.VISU.2016</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3a8750bc-67d9-4017-94a8-93b93fc36835" class="xyz-checkbox"/>
                    <label for="3a8750bc-67d9-4017-94a8-93b93fc36835">Ocsge_Visu_2019 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Ocsge_Visu_2019</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[43.2815, -0.321664], [44.1082, 1.22575]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>ocsge</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>nolegend</dd><dt><span>variant</span></dt><dd>OCSGE.VISU.2019</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="c7b24fd5-cdcb-4675-9ac8-aa5a4c5c823c" class="xyz-checkbox"/>
                    <label for="c7b24fd5-cdcb-4675-9ac8-aa5a4c5c823c">Hr_Orthoimagery_Orthophotos <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Hr_Orthoimagery_Orthophotos</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4013, -63.1607], [51.1124, 55.8464]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>ortho</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>HR.ORTHOIMAGERY.ORTHOPHOTOS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="96b904ac-52cc-47c1-ab6a-5e0dd77bb93e" class="xyz-checkbox"/>
                    <label for="96b904ac-52cc-47c1-ab6a-5e0dd77bb93e">Orthoimagery_Orthophos_Restrictedareas <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophos_Restrictedareas</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-22.9723, -178.309], [51.3121, 168.298]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>ortho</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOS.RESTRICTEDAREAS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="10162bec-3a36-4d78-8c42-e314c5540895" class="xyz-checkbox"/>
                    <label for="10162bec-3a36-4d78-8c42-e314c5540895">Orthoimagery_Orthophotos_Bdortho <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Bdortho</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-22.7643, -178.187], [51.1124, 168.19]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>ortho</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.BDORTHO</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="96952d43-cbd0-41e2-9f05-05dacacc60d7" class="xyz-checkbox"/>
                    <label for="96952d43-cbd0-41e2-9f05-05dacacc60d7">Orthoimagery_Orthophotos_Coast2000 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Coast2000</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[43.301, -5.21565], [51.1233, 2.60783]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>ortho</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.COAST2000</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="899279b0-6ac6-4874-947f-4a1af7a3c8d9" class="xyz-checkbox"/>
                    <label for="899279b0-6ac6-4874-947f-4a1af7a3c8d9">Orthoimagery_Orthophotos_Ilesdunord <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Ilesdunord</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[17.8626, -63.1986], [18.1701, -62.7828]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>ortho</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.ILESDUNORD</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f20f1633-eb0e-4652-ab0f-538dec4a5318" class="xyz-checkbox"/>
                    <label for="f20f1633-eb0e-4652-ab0f-538dec4a5318">Orthoimagery_Orthophotos_Irc <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Irc</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4013, -62.9717], [51.1124, 55.8464]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>ortho</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.IRC</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3525e700-0d7d-4ab9-b937-e45903d95965" class="xyz-checkbox"/>
                    <label for="3525e700-0d7d-4ab9-b937-e45903d95965">Orthoimagery_Orthophotos_Irc_express_2023 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Irc_express_2023</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>ortho</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.IRC-EXPRESS.2023</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a6f945bc-5638-435d-9225-813db918e82a" class="xyz-checkbox"/>
                    <label for="a6f945bc-5638-435d-9225-813db918e82a">Orthoimagery_Orthophotos_Ortho_asp_pac2022 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Ortho_asp_pac2022</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.ORTHO-ASP_PAC2022</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="06c00ac4-b0b8-4e4f-a79f-2e3c66f613d9" class="xyz-checkbox"/>
                    <label for="06c00ac4-b0b8-4e4f-a79f-2e3c66f613d9">Orthoimagery_Orthophotos_Ortho_asp_pac2023 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Ortho_asp_pac2023</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>ortho</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.ORTHO-ASP_PAC2023</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="33fc1fad-59a8-4bd7-bd16-0d6297505ac7" class="xyz-checkbox"/>
                    <label for="33fc1fad-59a8-4bd7-bd16-0d6297505ac7">Orthoimagery_Orthophotos_Ortho_express_2023 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Ortho_express_2023</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>ortho</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.ORTHO-EXPRESS.2023</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b0d69724-dc85-4724-b5c2-e1d632053b4b" class="xyz-checkbox"/>
                    <label for="b0d69724-dc85-4724-b5c2-e1d632053b4b">Pcrs_Lamb93 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Pcrs_Lamb93</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[42.6976, -3.80779], [48.8107, 6.92319]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>21</dd><dt><span>apikey</span></dt><dd>ortho</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>PCRS.LAMB93</dd><dt><span>TileMatrixSet</span></dt><dd>LAMB93_5cm_EPSG</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="7186057f-a9ae-4baf-9052-43aac9d466bd" class="xyz-checkbox"/>
                    <label for="7186057f-a9ae-4baf-9052-43aac9d466bd">Thr_Orthoimagery_Orthophotos <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Thr_Orthoimagery_Orthophotos</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[40.4378, -6.92466], [51.9098, 11.4965]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>21</dd><dt><span>apikey</span></dt><dd>ortho</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>THR.ORTHOIMAGERY.ORTHOPHOTOS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b99eb8ef-1cb7-47f7-bfc0-c5a83b4a2291" class="xyz-checkbox"/>
                    <label for="b99eb8ef-1cb7-47f7-bfc0-c5a83b4a2291">Orthoimagery_Orthophotos_1950_1965 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_1950_1965</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4013, -67.7214], [51.0945, 55.8464]]</dd><dt><span>min_zoom</span></dt><dd>3</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.1950-1965</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5934a1e6-9bdf-466e-a48d-f3308b2d4b73" class="xyz-checkbox"/>
                    <label for="5934a1e6-9bdf-466e-a48d-f3308b2d4b73">Orthoimagery_Orthophotos_1980_1995 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_1980_1995</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3125, -2.37153], [49.7785, 9.67536]]</dd><dt><span>min_zoom</span></dt><dd>3</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>BDORTHOHISTORIQUE</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.1980-1995</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="44eee210-6b0c-45a2-b6cc-d8d318724355" class="xyz-checkbox"/>
                    <label for="44eee210-6b0c-45a2-b6cc-d8d318724355">Orthoimagery_Orthophotos_Irc_express_2021 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Irc_express_2021</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.IRC-EXPRESS.2021</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="7cf7c9b8-e1e4-49de-90b8-d6cf72bff6ce" class="xyz-checkbox"/>
                    <label for="7cf7c9b8-e1e4-49de-90b8-d6cf72bff6ce">Orthoimagery_Orthophotos_Irc_express_2022 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Irc_express_2022</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4013, -62.9717], [51.1124, 55.8464]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.IRC-EXPRESS.2022</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0d49ed8c-7333-4549-b607-dd4f69252b2f" class="xyz-checkbox"/>
                    <label for="0d49ed8c-7333-4549-b607-dd4f69252b2f">Orthoimagery_Orthophotos_Irc_2013 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Irc_2013</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[42.5538, -3.74871], [50.3767, 7.17132]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.IRC.2013</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="c321189a-47a8-4842-9607-145a21bd8e7a" class="xyz-checkbox"/>
                    <label for="c321189a-47a8-4842-9607-145a21bd8e7a">Orthoimagery_Orthophotos_Irc_2014 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Irc_2014</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[43.1508, -2.37153], [49.6341, 7.22637]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.IRC.2014</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="40ee4242-fb26-489a-992e-c6eb423f6f46" class="xyz-checkbox"/>
                    <label for="40ee4242-fb26-489a-992e-c6eb423f6f46">Orthoimagery_Orthophotos_Irc_2015 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Irc_2015</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[42.3163, -5.20863], [51.0945, 8.25674]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.IRC.2015</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="097381ee-30d3-42c5-bf5c-36518fa3ecf0" class="xyz-checkbox"/>
                    <label for="097381ee-30d3-42c5-bf5c-36518fa3ecf0">Orthoimagery_Orthophotos_Irc_2016 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Irc_2016</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3215, -3.74871], [50.1839, 9.66314]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.IRC.2016</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="d65d79ff-98c3-4ba0-9d3d-de721c6ed50a" class="xyz-checkbox"/>
                    <label for="d65d79ff-98c3-4ba0-9d3d-de721c6ed50a">Orthoimagery_Orthophotos_Irc_2017 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Irc_2017</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[42.9454, -0.185295], [46.4137, 7.74363]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.IRC.2017</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b06bba76-d204-4cc6-9f36-4ba908279133" class="xyz-checkbox"/>
                    <label for="b06bba76-d204-4cc6-9f36-4ba908279133">Orthoimagery_Orthophotos_Irc_2018 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Irc_2018</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[42.3163, -5.19371], [51.1124, 8.25765]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.IRC.2018</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5ec23c62-e2cf-4405-a4f5-a895d60f6b8e" class="xyz-checkbox"/>
                    <label for="5ec23c62-e2cf-4405-a4f5-a895d60f6b8e">Orthoimagery_Orthophotos_Irc_2019 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Irc_2019</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3125, -3.74871], [50.1928, 9.66314]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.IRC.2019</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="250ec026-1eff-4c77-a9cb-fa5ecbecaaba" class="xyz-checkbox"/>
                    <label for="250ec026-1eff-4c77-a9cb-fa5ecbecaaba">Orthoimagery_Orthophotos_Irc_2020 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Irc_2020</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[42.9454, -2.68142], [49.4512, 7.74363]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.IRC.2020</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="406e7d6e-04d8-4db3-9614-d1877cc0ea80" class="xyz-checkbox"/>
                    <label for="406e7d6e-04d8-4db3-9614-d1877cc0ea80">Orthoimagery_Orthophotos_Ortho_asp_pac2020 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Ortho_asp_pac2020</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.ORTHO-ASP_PAC2020</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="bdb42e86-6991-45ed-a568-4bd18eb71f93" class="xyz-checkbox"/>
                    <label for="bdb42e86-6991-45ed-a568-4bd18eb71f93">Orthoimagery_Orthophotos_Ortho_asp_pac2021 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Ortho_asp_pac2021</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.ORTHO-ASP_PAC2021</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8f6ad18a-e796-4898-b1aa-f6050d18b816" class="xyz-checkbox"/>
                    <label for="8f6ad18a-e796-4898-b1aa-f6050d18b816">Orthoimagery_Orthophotos_Ortho_express_2021 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Ortho_express_2021</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.ORTHO-EXPRESS.2021</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a00b3be9-c23d-4d14-bd58-d28af8a516b2" class="xyz-checkbox"/>
                    <label for="a00b3be9-c23d-4d14-bd58-d28af8a516b2">Orthoimagery_Orthophotos_Ortho_express_2022 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Ortho_express_2022</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4013, -63.1607], [51.1124, 55.8464]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.ORTHO-EXPRESS.2022</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="777f401b-4fbc-4dc0-be5b-11b55ed32f61" class="xyz-checkbox"/>
                    <label for="777f401b-4fbc-4dc0-be5b-11b55ed32f61">Orthoimagery_Orthophotos_Socle_asp_2018 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Socle_asp_2018</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.SOCLE-ASP.2018</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f663e5fa-0f5c-453c-90c0-d9dd28bca761" class="xyz-checkbox"/>
                    <label for="f663e5fa-0f5c-453c-90c0-d9dd28bca761">Orthoimagery_Orthophotos_Urgence_Alex <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos_Urgence_Alex</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[43.8095, 7.07917], [44.1903, 7.64199]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS.URGENCE.ALEX</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="77b08558-294a-41ed-8d6c-d03dde5012db" class="xyz-checkbox"/>
                    <label for="77b08558-294a-41ed-8d6c-d03dde5012db">Orthoimagery_Orthophotos2000 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2000</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2000</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f4dd5951-8420-410a-bae1-9475f5a41083" class="xyz-checkbox"/>
                    <label for="f4dd5951-8420-410a-bae1-9475f5a41083">Orthoimagery_Orthophotos2000_2005 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2000_2005</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4013, -178.187], [64.0698, 55.8561]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2000-2005</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8af46304-5626-402a-9ea5-879cb032d3ab" class="xyz-checkbox"/>
                    <label for="8af46304-5626-402a-9ea5-879cb032d3ab">Orthoimagery_Orthophotos2001 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2001</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[4.47153, -61.2472], [50.3765, 7.23234]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2001</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="c919fbb8-7fc7-420b-832b-737a4eae9600" class="xyz-checkbox"/>
                    <label for="c919fbb8-7fc7-420b-832b-737a4eae9600">Orthoimagery_Orthophotos2002 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2002</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[4.49867, -61.2472], [50.3765, 9.68861]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2002</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b48d8592-4af3-4db4-abe3-cb5c53bd57db" class="xyz-checkbox"/>
                    <label for="b48d8592-4af3-4db4-abe3-cb5c53bd57db">Orthoimagery_Orthophotos2003 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2003</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2003</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0242283c-f3e6-4a5b-afca-504d7390fab9" class="xyz-checkbox"/>
                    <label for="0242283c-f3e6-4a5b-afca-504d7390fab9">Orthoimagery_Orthophotos2004 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2004</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4013, -178.187], [51.091, 55.8561]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2004</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="662e2ea6-d3ff-4992-b412-1f44ffca602f" class="xyz-checkbox"/>
                    <label for="662e2ea6-d3ff-4992-b412-1f44ffca602f">Orthoimagery_Orthophotos2005 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2005</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4013, -178.187], [51.091, 55.8561]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2005</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="92abc9e9-095f-4e58-882f-f02e831e3548" class="xyz-checkbox"/>
                    <label for="92abc9e9-095f-4e58-882f-f02e831e3548">Orthoimagery_Orthophotos2006 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2006</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4013, -178.187], [51.091, 55.8561]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2006</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4571c1c3-0326-4a48-9a17-7a54bd46d243" class="xyz-checkbox"/>
                    <label for="4571c1c3-0326-4a48-9a17-7a54bd46d243">Orthoimagery_Orthophotos2006_2010 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2006_2010</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2006-2010</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8299661b-5dba-4a3e-b5e7-5fa16d6d1ca0" class="xyz-checkbox"/>
                    <label for="8299661b-5dba-4a3e-b5e7-5fa16d6d1ca0">Orthoimagery_Orthophotos2007 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2007</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2007</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0e134681-6434-4226-a7c8-a56f02fb3aa7" class="xyz-checkbox"/>
                    <label for="0e134681-6434-4226-a7c8-a56f02fb3aa7">Orthoimagery_Orthophotos2008 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2008</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4013, -178.187], [51.091, 55.8561]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2008</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="7c154af9-167d-4d5a-841d-50aeac1ef9dd" class="xyz-checkbox"/>
                    <label for="7c154af9-167d-4d5a-841d-50aeac1ef9dd">Orthoimagery_Orthophotos2009 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2009</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2009</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9f297c7f-2dbc-4d2c-b09c-98bc3cfc4e42" class="xyz-checkbox"/>
                    <label for="9f297c7f-2dbc-4d2c-b09c-98bc3cfc4e42">Orthoimagery_Orthophotos2010 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2010</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2010</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="1e5b69a0-2ea0-43a2-ae07-23d09cac0d47" class="xyz-checkbox"/>
                    <label for="1e5b69a0-2ea0-43a2-ae07-23d09cac0d47">Orthoimagery_Orthophotos2011 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2011</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2011</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="93a78625-911a-490b-bc2b-55bcdd7f04fd" class="xyz-checkbox"/>
                    <label for="93a78625-911a-490b-bc2b-55bcdd7f04fd">Orthoimagery_Orthophotos2011_2015 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2011_2015</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4013, -178.187], [51.0945, 55.8561]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2011-2015</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e38d7aa1-e8eb-4fe4-9283-0fc511c260a0" class="xyz-checkbox"/>
                    <label for="e38d7aa1-e8eb-4fe4-9283-0fc511c260a0">Orthoimagery_Orthophotos2012 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2012</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2012</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="556ccad7-fda2-4a67-9724-c349af6c1f5c" class="xyz-checkbox"/>
                    <label for="556ccad7-fda2-4a67-9724-c349af6c1f5c">Orthoimagery_Orthophotos2013 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2013</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2013</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="aba2ada0-a112-4014-9784-db14eb3f8b0a" class="xyz-checkbox"/>
                    <label for="aba2ada0-a112-4014-9784-db14eb3f8b0a">Orthoimagery_Orthophotos2014 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2014</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2014</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="da69875c-b48f-4c87-887b-157096d919a8" class="xyz-checkbox"/>
                    <label for="da69875c-b48f-4c87-887b-157096d919a8">Orthoimagery_Orthophotos2015 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2015</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2015</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ff542572-9f33-43ed-9bae-2d80d4dbb0fb" class="xyz-checkbox"/>
                    <label for="ff542572-9f33-43ed-9bae-2d80d4dbb0fb">Orthoimagery_Orthophotos2016 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2016</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2016</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e1240b5e-1601-4da8-9da4-68354c96bede" class="xyz-checkbox"/>
                    <label for="e1240b5e-1601-4da8-9da4-68354c96bede">Orthoimagery_Orthophotos2017 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2017</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4013, -63.1607], [50.3856, 55.8464]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2017</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0d4906e5-1ac4-44f0-8e95-ef27ebc170a9" class="xyz-checkbox"/>
                    <label for="0d4906e5-1ac4-44f0-8e95-ef27ebc170a9">Orthoimagery_Orthophotos2018 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2018</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[42.3163, -5.20863], [51.1124, 8.25765]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2018</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="973b920f-879f-4c77-8431-f3eb0ba4228d" class="xyz-checkbox"/>
                    <label for="973b920f-879f-4c77-8431-f3eb0ba4228d">Orthoimagery_Orthophotos2019 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2019</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3125, -3.74871], [50.1928, 9.66314]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2019</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f4973273-715d-45e2-a3ac-7ab84105ea75" class="xyz-checkbox"/>
                    <label for="f4973273-715d-45e2-a3ac-7ab84105ea75">Orthoimagery_Orthophotos2020 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Orthophotos2020</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[42.9454, -2.68142], [49.4512, 7.74363]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>orthohisto</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHOPHOTOS2020</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9e12b2ac-c101-49f5-b780-b2c906eb8f9f" class="xyz-checkbox"/>
                    <label for="9e12b2ac-c101-49f5-b780-b2c906eb8f9f">Orthoimagery_Ortho_sat_Pleiades_2012 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Pleiades_2012</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.3539, -53.2686], [50.6037, 55.5544]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.PLEIADES.2012</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="fd51f02d-39ed-477a-9b51-c50528633cc5" class="xyz-checkbox"/>
                    <label for="fd51f02d-39ed-477a-9b51-c50528633cc5">Orthoimagery_Ortho_sat_Pleiades_2013 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Pleiades_2013</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.PLEIADES.2013</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="064bbead-31a1-42c8-b785-244816636141" class="xyz-checkbox"/>
                    <label for="064bbead-31a1-42c8-b785-244816636141">Orthoimagery_Ortho_sat_Pleiades_2014 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Pleiades_2014</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.PLEIADES.2014</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="58ef22f7-30c4-46a4-b3c1-8b3fed700018" class="xyz-checkbox"/>
                    <label for="58ef22f7-30c4-46a4-b3c1-8b3fed700018">Orthoimagery_Ortho_sat_Pleiades_2015 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Pleiades_2015</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.PLEIADES.2015</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a3a84e9b-3f5a-44a0-94e4-bae6ee85db0a" class="xyz-checkbox"/>
                    <label for="a3a84e9b-3f5a-44a0-94e4-bae6ee85db0a">Orthoimagery_Ortho_sat_Pleiades_2016 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Pleiades_2016</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.32, -54.1373], [50.6549, 55.8441]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.PLEIADES.2016</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="377441f1-e948-4aea-92ea-c36a0091bec6" class="xyz-checkbox"/>
                    <label for="377441f1-e948-4aea-92ea-c36a0091bec6">Orthoimagery_Ortho_sat_Pleiades_2017 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Pleiades_2017</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4013, -63.1796], [51.1117, 55.8465]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.PLEIADES.2017</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="fb3ed5c3-37fa-4f23-a710-1a25a57a0d47" class="xyz-checkbox"/>
                    <label for="fb3ed5c3-37fa-4f23-a710-1a25a57a0d47">Orthoimagery_Ortho_sat_Pleiades_2018 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Pleiades_2018</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4094, -63.1702], [51.0841, 55.8649]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.PLEIADES.2018</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="37750f6c-cfb6-4133-aa4b-1a74a4591110" class="xyz-checkbox"/>
                    <label for="37750f6c-cfb6-4133-aa4b-1a74a4591110">Orthoimagery_Ortho_sat_Pleiades_2019 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Pleiades_2019</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4094, -63.1702], [51.1117, 55.8649]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.PLEIADES.2019</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="bf477ec8-6472-404f-a8da-e590a34b9cd6" class="xyz-checkbox"/>
                    <label for="bf477ec8-6472-404f-a8da-e590a34b9cd6">Orthoimagery_Ortho_sat_Pleiades_2020 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Pleiades_2020</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-13.0169, -63.1724], [51.1117, 45.3136]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.PLEIADES.2020</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8b7832da-bc54-445b-951a-1dece4207d6d" class="xyz-checkbox"/>
                    <label for="8b7832da-bc54-445b-951a-1dece4207d6d">Orthoimagery_Ortho_sat_Pleiades_2021 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Pleiades_2021</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.PLEIADES.2021</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8a865899-ef4e-4218-a789-32cf1e99d457" class="xyz-checkbox"/>
                    <label for="8a865899-ef4e-4218-a789-32cf1e99d457">Orthoimagery_Ortho_sat_Pleiades_2022 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Pleiades_2022</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.3733, -67.7132], [69.3108, 55.7216]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.PLEIADES.2022</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="069e2a08-75f5-40bb-a4c1-cdd6afc861c1" class="xyz-checkbox"/>
                    <label for="069e2a08-75f5-40bb-a4c1-cdd6afc861c1">Orthoimagery_Ortho_sat_Rapideye_2010 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Rapideye_2010</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.2014, -5.80725], [50.9218, 10.961]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>15</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.RAPIDEYE.2010</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="96aec4a8-fede-4cab-aab5-9770f870d130" class="xyz-checkbox"/>
                    <label for="96aec4a8-fede-4cab-aab5-9770f870d130">Orthoimagery_Ortho_sat_Rapideye_2011 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Rapideye_2011</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.0227, -5.80725], [51.1752, 10.961]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>15</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.RAPIDEYE.2011</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9aac46e4-29a6-4bc7-9131-ba7f8da561ce" class="xyz-checkbox"/>
                    <label for="9aac46e4-29a6-4bc7-9131-ba7f8da561ce">Orthoimagery_Ortho_sat_Spot_2013 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Spot_2013</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[44.8809, 0.563585], [50.3879, 4.29191]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.SPOT.2013</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd><dt><span>status</span></dt><dd>broken</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="863a568b-f03d-44ac-9ee1-3dbaf517d452" class="xyz-checkbox"/>
                    <label for="863a568b-f03d-44ac-9ee1-3dbaf517d452">Orthoimagery_Ortho_sat_Spot_2014 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Spot_2014</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-75.0, -179.5], [75.0, 179.5]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.SPOT.2014</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="bdb65a07-35ba-463a-a87d-97db5db7862e" class="xyz-checkbox"/>
                    <label for="bdb65a07-35ba-463a-a87d-97db5db7862e">Orthoimagery_Ortho_sat_Spot_2015 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Spot_2015</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4104, -61.8141], [51.106, 55.856]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.SPOT.2015</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0bd439de-2959-41c2-9ba6-9ba1aba46a38" class="xyz-checkbox"/>
                    <label for="0bd439de-2959-41c2-9ba6-9ba1aba46a38">Orthoimagery_Ortho_sat_Spot_2016 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Spot_2016</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4104, -61.85], [51.1123, 55.8562]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.SPOT.2016</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="d759d770-d90e-48eb-a45a-4221eb4b650d" class="xyz-checkbox"/>
                    <label for="d759d770-d90e-48eb-a45a-4221eb4b650d">Orthoimagery_Ortho_sat_Spot_2017 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Spot_2017</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4104, -61.8534], [51.1123, 55.8562]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.SPOT.2017</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3a749599-c85a-4d71-8d73-dd742508fd32" class="xyz-checkbox"/>
                    <label for="3a749599-c85a-4d71-8d73-dd742508fd32">Orthoimagery_Ortho_sat_Spot_2018 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Spot_2018</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.2593, -5.57103], [51.1123, 10.7394]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.SPOT.2018</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="44006782-7913-4cb0-90c2-8f41831bf92e" class="xyz-checkbox"/>
                    <label for="44006782-7913-4cb0-90c2-8f41831bf92e">Orthoimagery_Ortho_sat_Spot_2019 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Spot_2019</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.2593, -5.57103], [51.1123, 10.7394]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.SPOT.2019</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="90a074e3-f5d4-4c9e-901c-210bdb60af2e" class="xyz-checkbox"/>
                    <label for="90a074e3-f5d4-4c9e-901c-210bdb60af2e">Orthoimagery_Ortho_sat_Spot_2020 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Spot_2020</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.2593, -5.57103], [51.1123, 10.7394]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.SPOT.2020</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="d9cb6b05-b704-429f-9038-10a4623750d9" class="xyz-checkbox"/>
                    <label for="d9cb6b05-b704-429f-9038-10a4623750d9">Orthoimagery_Ortho_sat_Spot_2021 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Orthoimagery_Ortho_sat_Spot_2021</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.2593, -5.57103], [51.1123, 10.7394]]</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>satellite</dd><dt><span>format</span></dt><dd>image/jpeg</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>ORTHOIMAGERY.ORTHO-SAT.SPOT.2021</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="73e8fdb0-6b81-413d-9e33-288fd7184c0b" class="xyz-checkbox"/>
                    <label for="73e8fdb0-6b81-413d-9e33-288fd7184c0b">Bdcarto_etat_major_Niveau3 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Bdcarto_etat_major_Niveau3</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[42.3263, -5.15012], [51.0938, 7.19384]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>sol</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>BDCARTO_ETAT-MAJOR.NIVEAU3</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9d5c95da-bd72-46c3-b4c7-bccab5abc8b2" class="xyz-checkbox"/>
                    <label for="9d5c95da-bd72-46c3-b4c7-bccab5abc8b2">Bdcarto_etat_major_Niveau4 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Bdcarto_etat_major_Niveau4</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[41.3252, -5.15047], [51.0991, 9.57054]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>apikey</span></dt><dd>sol</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>BDCARTO_ETAT-MAJOR.NIVEAU4</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8934de39-2ca4-4965-b440-bfa57e77f417" class="xyz-checkbox"/>
                    <label for="8934de39-2ca4-4965-b440-bfa57e77f417">Buildings_Buildings <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Buildings_Buildings</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4969, -63.9692], [71.5841, 55.9644]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>topographie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>BUILDINGS.BUILDINGS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4bc7f5a8-e153-4933-82dd-578e5f90939b" class="xyz-checkbox"/>
                    <label for="4bc7f5a8-e153-4933-82dd-578e5f90939b">Geographicalnames_Names <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Geographicalnames_Names</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4969, -63.9692], [71.5841, 55.9644]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>topographie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>GEOGRAPHICALNAMES.NAMES</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="68fed32c-6b29-4f12-9179-56619659731d" class="xyz-checkbox"/>
                    <label for="68fed32c-6b29-4f12-9179-56619659731d">Hydrography_Hydrography <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Hydrography_Hydrography</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4969, -63.9692], [71.5841, 55.9644]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>topographie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>HYDROGRAPHY.HYDROGRAPHY</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="989e11a0-667d-4b5c-a101-428a26ab16fa" class="xyz-checkbox"/>
                    <label for="989e11a0-667d-4b5c-a101-428a26ab16fa">Transportnetwork_Commontransportelements_Markerpost <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Transportnetwork_Commontransportelements_Markerpost</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>10</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>topographie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>TRANSPORTNETWORK.COMMONTRANSPORTELEMENTS.MARKERPOST</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="55a5d7f1-3eb7-4e0f-8e8f-4dec90bf1d46" class="xyz-checkbox"/>
                    <label for="55a5d7f1-3eb7-4e0f-8e8f-4dec90bf1d46">Transportnetworks_Railways <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Transportnetworks_Railways</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4969, -63.9692], [71.5841, 55.9644]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>topographie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>TRANSPORTNETWORKS.RAILWAYS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3ea8ab17-6d5e-4650-941b-bbd105a60e6c" class="xyz-checkbox"/>
                    <label for="3ea8ab17-6d5e-4650-941b-bbd105a60e6c">Transportnetworks_Roads <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Transportnetworks_Roads</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4969, -63.9692], [71.5841, 55.9644]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>topographie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>TRANSPORTNETWORKS.ROADS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="eaa41a22-7788-4da4-bdef-97c3209ea723" class="xyz-checkbox"/>
                    <label for="eaa41a22-7788-4da4-bdef-97c3209ea723">Transportnetworks_Runways <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Transportnetworks_Runways</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4969, -63.9692], [71.5841, 55.9644]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>topographie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>TRANSPORTNETWORKS.RUNWAYS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ed779720-2dbe-455d-9380-1d8df8dbd290" class="xyz-checkbox"/>
                    <label for="ed779720-2dbe-455d-9380-1d8df8dbd290">Utilityandgovernmentalservices_All <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Utilityandgovernmentalservices_All</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [71.5841, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>topographie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>UTILITYANDGOVERNMENTALSERVICES.ALL</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="7dce72ef-c1e7-4d26-9e8e-67a0c2b66ba9" class="xyz-checkbox"/>
                    <label for="7dce72ef-c1e7-4d26-9e8e-67a0c2b66ba9">Hedge_Hedge <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Hedge_Hedge</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>7</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>topographie</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>hedge.hedge</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="383cb259-f85b-41fe-b67c-7481eb326011" class="xyz-checkbox"/>
                    <label for="383cb259-f85b-41fe-b67c-7481eb326011">Securoute_Te_1te <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Securoute_Te_1te</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>4</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>transports</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>RESEAU ROUTIER 1TE</dd><dt><span>variant</span></dt><dd>SECUROUTE.TE.1TE</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="57cade7c-a8c3-44c9-bc12-7a269a760ae3" class="xyz-checkbox"/>
                    <label for="57cade7c-a8c3-44c9-bc12-7a269a760ae3">Securoute_Te_2te48 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Securoute_Te_2te48</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>transports</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>RESEAU ROUTIER 2TE48</dd><dt><span>variant</span></dt><dd>SECUROUTE.TE.2TE48</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="c9be528f-ab3b-4765-896e-3ef86d591668" class="xyz-checkbox"/>
                    <label for="c9be528f-ab3b-4765-896e-3ef86d591668">Securoute_Te_All <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Securoute_Te_All</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>transports</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>TOUS LES FRANCHISSEMENTS</dd><dt><span>variant</span></dt><dd>SECUROUTE.TE.ALL</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="7affd84d-01a8-42b5-9dca-cb19f55c59b3" class="xyz-checkbox"/>
                    <label for="7affd84d-01a8-42b5-9dca-cb19f55c59b3">Securoute_Te_Oa <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Securoute_Te_Oa</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>transports</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>AUTRES FRANCHISSEMENTS</dd><dt><span>variant</span></dt><dd>SECUROUTE.TE.OA</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="def06b21-0679-4b8d-a476-15d74a5973cb" class="xyz-checkbox"/>
                    <label for="def06b21-0679-4b8d-a476-15d74a5973cb">Securoute_Te_Pn <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Securoute_Te_Pn</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>transports</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>FRANCHISSEMENTS PASSAGE A NIVEAU</dd><dt><span>variant</span></dt><dd>SECUROUTE.TE.PN</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="eee6600d-6a8a-4540-be54-b973d60567b3" class="xyz-checkbox"/>
                    <label for="eee6600d-6a8a-4540-be54-b973d60567b3">Securoute_Te_Pnd <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Securoute_Te_Pnd</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>transports</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>FRANCHISSEMENTS PASSAGE A NIVEAU DIFFICILE</dd><dt><span>variant</span></dt><dd>SECUROUTE.TE.PND</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="70f15511-77bf-4d4b-b2fa-0bc4af572aaa" class="xyz-checkbox"/>
                    <label for="70f15511-77bf-4d4b-b2fa-0bc4af572aaa">Securoute_Te_Te120 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Securoute_Te_Te120</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>transports</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>RESEAU ROUTIER TE120</dd><dt><span>variant</span></dt><dd>SECUROUTE.TE.TE120</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f27d49a8-166f-49c5-9c2e-8cd06f24364c" class="xyz-checkbox"/>
                    <label for="f27d49a8-166f-49c5-9c2e-8cd06f24364c">Securoute_Te_Te72 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Securoute_Te_Te72</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>transports</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>RESEAU ROUTIER TE72</dd><dt><span>variant</span></dt><dd>SECUROUTE.TE.TE72</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="90f158c9-6c8c-4867-a928-d54d115e85a1" class="xyz-checkbox"/>
                    <label for="90f158c9-6c8c-4867-a928-d54d115e85a1">Securoute_Te_Te94 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Securoute_Te_Te94</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>6</dd><dt><span>max_zoom</span></dt><dd>17</dd><dt><span>apikey</span></dt><dd>transports</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>RESEAU ROUTIER TE94</dd><dt><span>variant</span></dt><dd>SECUROUTE.TE.TE94</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cc7dab55-0608-4d28-b64a-09b3ea6e5ff4" class="xyz-checkbox"/>
                    <label for="cc7dab55-0608-4d28-b64a-09b3ea6e5ff4">Transportnetworks_Roads_Direction <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Transportnetworks_Roads_Direction</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[-21.4756, -63.3725], [51.3121, 55.9259]]</dd><dt><span>min_zoom</span></dt><dd>15</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>apikey</span></dt><dd>transports</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>TRANSPORTNETWORKS.ROADS.DIRECTION</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="136cbc7b-6149-48ab-8e97-373014d13184" class="xyz-checkbox"/>
                    <label for="136cbc7b-6149-48ab-8e97-373014d13184">Transports_Drones_Restrictions <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">GeoportailFrance.Transports_Drones_Restrictions</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET={TileMatrixSet}&FORMAT={format}&LAYER={variant}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}</dd><dt><span>html_attribution</span></dt><dd><a target="_blank"href="https://www.geoportail.gouv.fr/">Geoportail France</a></dd><dt><span>attribution</span></dt><dd>Geoportail France</dd><dt><span>bounds</span></dt><dd>[[40.576, -9.88147], [51.4428, 11.6781]]</dd><dt><span>min_zoom</span></dt><dd>3</dd><dt><span>max_zoom</span></dt><dd>15</dd><dt><span>apikey</span></dt><dd>transports</dd><dt><span>format</span></dt><dd>image/png</dd><dt><span>style</span></dt><dd>normal</dd><dt><span>variant</span></dt><dd>TRANSPORTS.DRONES.RESTRICTIONS</dd><dt><span>TileMatrixSet</span></dt><dd>PM</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3a3d4dc5-ffdf-4bdf-abad-51ea99e0a85f" class="xyz-checkbox"/>
                    <label for="3a3d4dc5-ffdf-4bdf-abad-51ea99e0a85f">OneMapSG <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">5 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="4d8ac1cc-b38c-428f-8f84-0e0bab664ac5" class="xyz-checkbox"/>
                    <label for="4d8ac1cc-b38c-428f-8f84-0e0bab664ac5">Default <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OneMapSG.Default</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://maps-{s}.onemap.sg/v3/{variant}/{z}/{x}/{y}.png</dd><dt><span>variant</span></dt><dd>Default</dd><dt><span>min_zoom</span></dt><dd>11</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>bounds</span></dt><dd>[[1.56073, 104.11475], [1.16, 103.502]]</dd><dt><span>html_attribution</span></dt><dd><img src="https://docs.onemap.sg/maps/images/oneMap64-01.png" style="height:20px;width:20px;"/> New OneMap | Map data &copy; contributors, <a href="http://SLA.gov.sg">Singapore Land Authority</a></dd><dt><span>attribution</span></dt><dd>![](https://docs.onemap.sg/maps/images/oneMap64-01.png) New OneMap | Map data (C) contributors, Singapore Land Authority</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ca5559d2-c170-4184-beb9-f9004d9bdbe0" class="xyz-checkbox"/>
                    <label for="ca5559d2-c170-4184-beb9-f9004d9bdbe0">Night <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OneMapSG.Night</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://maps-{s}.onemap.sg/v3/{variant}/{z}/{x}/{y}.png</dd><dt><span>variant</span></dt><dd>Night</dd><dt><span>min_zoom</span></dt><dd>11</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>bounds</span></dt><dd>[[1.56073, 104.11475], [1.16, 103.502]]</dd><dt><span>html_attribution</span></dt><dd><img src="https://docs.onemap.sg/maps/images/oneMap64-01.png" style="height:20px;width:20px;"/> New OneMap | Map data &copy; contributors, <a href="http://SLA.gov.sg">Singapore Land Authority</a></dd><dt><span>attribution</span></dt><dd>![](https://docs.onemap.sg/maps/images/oneMap64-01.png) New OneMap | Map data (C) contributors, Singapore Land Authority</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ea12e64d-a6c6-4302-9b9a-baff5c0be842" class="xyz-checkbox"/>
                    <label for="ea12e64d-a6c6-4302-9b9a-baff5c0be842">Original <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OneMapSG.Original</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://maps-{s}.onemap.sg/v3/{variant}/{z}/{x}/{y}.png</dd><dt><span>variant</span></dt><dd>Original</dd><dt><span>min_zoom</span></dt><dd>11</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>bounds</span></dt><dd>[[1.56073, 104.11475], [1.16, 103.502]]</dd><dt><span>html_attribution</span></dt><dd><img src="https://docs.onemap.sg/maps/images/oneMap64-01.png" style="height:20px;width:20px;"/> New OneMap | Map data &copy; contributors, <a href="http://SLA.gov.sg">Singapore Land Authority</a></dd><dt><span>attribution</span></dt><dd>![](https://docs.onemap.sg/maps/images/oneMap64-01.png) New OneMap | Map data (C) contributors, Singapore Land Authority</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5dce0184-f6f0-483f-a065-829106205d4f" class="xyz-checkbox"/>
                    <label for="5dce0184-f6f0-483f-a065-829106205d4f">Grey <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OneMapSG.Grey</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://maps-{s}.onemap.sg/v3/{variant}/{z}/{x}/{y}.png</dd><dt><span>variant</span></dt><dd>Grey</dd><dt><span>min_zoom</span></dt><dd>11</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>bounds</span></dt><dd>[[1.56073, 104.11475], [1.16, 103.502]]</dd><dt><span>html_attribution</span></dt><dd><img src="https://docs.onemap.sg/maps/images/oneMap64-01.png" style="height:20px;width:20px;"/> New OneMap | Map data &copy; contributors, <a href="http://SLA.gov.sg">Singapore Land Authority</a></dd><dt><span>attribution</span></dt><dd>![](https://docs.onemap.sg/maps/images/oneMap64-01.png) New OneMap | Map data (C) contributors, Singapore Land Authority</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="52c73b15-c346-493f-9e0a-df6e25c91104" class="xyz-checkbox"/>
                    <label for="52c73b15-c346-493f-9e0a-df6e25c91104">LandLot <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OneMapSG.LandLot</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://maps-{s}.onemap.sg/v3/{variant}/{z}/{x}/{y}.png</dd><dt><span>variant</span></dt><dd>LandLot</dd><dt><span>min_zoom</span></dt><dd>11</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>bounds</span></dt><dd>[[1.56073, 104.11475], [1.16, 103.502]]</dd><dt><span>html_attribution</span></dt><dd><img src="https://docs.onemap.sg/maps/images/oneMap64-01.png" style="height:20px;width:20px;"/> New OneMap | Map data &copy; contributors, <a href="http://SLA.gov.sg">Singapore Land Authority</a></dd><dt><span>attribution</span></dt><dd>![](https://docs.onemap.sg/maps/images/oneMap64-01.png) New OneMap | Map data (C) contributors, Singapore Land Authority</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e8801f2c-8ecf-483b-84b2-b068a8ec4031" class="xyz-checkbox"/>
                    <label for="e8801f2c-8ecf-483b-84b2-b068a8ec4031">USGS <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">3 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="f434cd20-290b-441b-8dca-cbe0fd5dcc92" class="xyz-checkbox"/>
                    <label for="f434cd20-290b-441b-8dca-cbe0fd5dcc92">USTopo <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">USGS.USTopo</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a></dd><dt><span>attribution</span></dt><dd>Tiles courtesy of the U.S. Geological Survey</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5496374c-1cc5-48ef-b32f-0c5612ff1b0e" class="xyz-checkbox"/>
                    <label for="5496374c-1cc5-48ef-b32f-0c5612ff1b0e">USImagery <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">USGS.USImagery</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a></dd><dt><span>attribution</span></dt><dd>Tiles courtesy of the U.S. Geological Survey</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0804f3b5-9c78-4731-94fa-a520b2ae8fe8" class="xyz-checkbox"/>
                    <label for="0804f3b5-9c78-4731-94fa-a520b2ae8fe8">USImageryTopo <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">USGS.USImageryTopo</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryTopo/MapServer/tile/{z}/{y}/{x}</dd><dt><span>max_zoom</span></dt><dd>20</dd><dt><span>html_attribution</span></dt><dd>Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a></dd><dt><span>attribution</span></dt><dd>Tiles courtesy of the U.S. Geological Survey</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="4602f9ba-0f72-4c21-bd9b-0ac9b6628e6f" class="xyz-checkbox"/>
                    <label for="4602f9ba-0f72-4c21-bd9b-0ac9b6628e6f">WaymarkedTrails <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">6 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="1ba7ccef-45c8-4481-91c8-08d107d4f97a" class="xyz-checkbox"/>
                    <label for="1ba7ccef-45c8-4481-91c8-08d107d4f97a">hiking <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">WaymarkedTrails.hiking</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tile.waymarkedtrails.org/{variant}/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>html_attribution</span></dt><dd>Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Map style: &copy; <a href="https://waymarkedtrails.org">waymarkedtrails.org</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)</dd><dt><span>attribution</span></dt><dd>Map data: (C) OpenStreetMap contributors | Map style: (C) waymarkedtrails.org (CC-BY-SA)</dd><dt><span>variant</span></dt><dd>hiking</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="fcb8ad6a-d031-4cf0-89be-ecafe3300cc4" class="xyz-checkbox"/>
                    <label for="fcb8ad6a-d031-4cf0-89be-ecafe3300cc4">cycling <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">WaymarkedTrails.cycling</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tile.waymarkedtrails.org/{variant}/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>html_attribution</span></dt><dd>Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Map style: &copy; <a href="https://waymarkedtrails.org">waymarkedtrails.org</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)</dd><dt><span>attribution</span></dt><dd>Map data: (C) OpenStreetMap contributors | Map style: (C) waymarkedtrails.org (CC-BY-SA)</dd><dt><span>variant</span></dt><dd>cycling</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="26a1f1b8-3867-4030-a7ea-90cf2921672a" class="xyz-checkbox"/>
                    <label for="26a1f1b8-3867-4030-a7ea-90cf2921672a">mtb <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">WaymarkedTrails.mtb</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tile.waymarkedtrails.org/{variant}/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>html_attribution</span></dt><dd>Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Map style: &copy; <a href="https://waymarkedtrails.org">waymarkedtrails.org</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)</dd><dt><span>attribution</span></dt><dd>Map data: (C) OpenStreetMap contributors | Map style: (C) waymarkedtrails.org (CC-BY-SA)</dd><dt><span>variant</span></dt><dd>mtb</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cbedcaeb-7a4a-4634-a3f3-f43430ab5cb7" class="xyz-checkbox"/>
                    <label for="cbedcaeb-7a4a-4634-a3f3-f43430ab5cb7">slopes <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">WaymarkedTrails.slopes</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tile.waymarkedtrails.org/{variant}/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>html_attribution</span></dt><dd>Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Map style: &copy; <a href="https://waymarkedtrails.org">waymarkedtrails.org</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)</dd><dt><span>attribution</span></dt><dd>Map data: (C) OpenStreetMap contributors | Map style: (C) waymarkedtrails.org (CC-BY-SA)</dd><dt><span>variant</span></dt><dd>slopes</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="51801217-c7e2-41d4-a7e1-f85beed8cabb" class="xyz-checkbox"/>
                    <label for="51801217-c7e2-41d4-a7e1-f85beed8cabb">riding <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">WaymarkedTrails.riding</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tile.waymarkedtrails.org/{variant}/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>html_attribution</span></dt><dd>Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Map style: &copy; <a href="https://waymarkedtrails.org">waymarkedtrails.org</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)</dd><dt><span>attribution</span></dt><dd>Map data: (C) OpenStreetMap contributors | Map style: (C) waymarkedtrails.org (CC-BY-SA)</dd><dt><span>variant</span></dt><dd>riding</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="9befc212-bfd1-4edf-9b9f-875f6c6ab0f6" class="xyz-checkbox"/>
                    <label for="9befc212-bfd1-4edf-9b9f-875f6c6ab0f6">skating <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">WaymarkedTrails.skating</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tile.waymarkedtrails.org/{variant}/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>html_attribution</span></dt><dd>Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Map style: &copy; <a href="https://waymarkedtrails.org">waymarkedtrails.org</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)</dd><dt><span>attribution</span></dt><dd>Map data: (C) OpenStreetMap contributors | Map style: (C) waymarkedtrails.org (CC-BY-SA)</dd><dt><span>variant</span></dt><dd>skating</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="fc1214c3-eb6f-4f9a-9cb4-e874dae60e39" class="xyz-checkbox"/>
                    <label for="fc1214c3-eb6f-4f9a-9cb4-e874dae60e39">OpenAIP <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenAIP</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://{s}.tile.maps.openaip.net/geowebcache/service/tms/1.0.0/openaip_basemap@EPSG%3A900913@png/{z}/{x}/{y}.{ext}</dd><dt><span>html_attribution</span></dt><dd><a href="https://www.openaip.net/">openAIP Data</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-NC-SA</a>)</dd><dt><span>attribution</span></dt><dd>openAIP Data (CC-BY-NC-SA)</dd><dt><span>ext</span></dt><dd>png</dd><dt><span>min_zoom</span></dt><dd>4</dd><dt><span>max_zoom</span></dt><dd>14</dd><dt><span>tms</span></dt><dd>True</dd><dt><span>detectRetina</span></dt><dd>True</dd><dt><span>subdomains</span></dt><dd>12</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="614f196e-1cdf-45e8-9ac0-8eaee31055a9" class="xyz-checkbox"/>
                    <label for="614f196e-1cdf-45e8-9ac0-8eaee31055a9">OpenSnowMap <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">1 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="d5c5aa02-6452-4435-ba2c-c20a95fb4fb7" class="xyz-checkbox"/>
                    <label for="d5c5aa02-6452-4435-ba2c-c20a95fb4fb7">pistes <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OpenSnowMap.pistes</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://tiles.opensnowmap.org/{variant}/{z}/{x}/{y}.png</dd><dt><span>min_zoom</span></dt><dd>9</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>html_attribution</span></dt><dd>Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors & ODbL, &copy; <a href="https://www.opensnowmap.org/iframes/data.html">www.opensnowmap.org</a> <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a></dd><dt><span>attribution</span></dt><dd>Map data: (C) OpenStreetMap contributors & ODbL, (C) www.opensnowmap.org CC-BY-SA</dd><dt><span>variant</span></dt><dd>pistes</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="48564fee-803b-4c82-8655-4a5214cedc93" class="xyz-checkbox"/>
                    <label for="48564fee-803b-4c82-8655-4a5214cedc93">AzureMaps <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">7 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="b9897841-b7a7-4f38-b800-86f6b42fc5ed" class="xyz-checkbox"/>
                    <label for="b9897841-b7a7-4f38-b800-86f6b42fc5ed">MicrosoftImagery <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">AzureMaps.MicrosoftImagery</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://atlas.microsoft.com/map/tile?api-version={apiVersion}&tilesetId={variant}&x={x}&y={y}&zoom={z}&language={language}&subscription-key={subscriptionKey}</dd><dt><span>html_attribution</span></dt><dd>See https://docs.microsoft.com/en-us/rest/api/maps/render-v2/get-map-tile for details.</dd><dt><span>attribution</span></dt><dd>See https://docs.microsoft.com/en-us/rest/api/maps/render-v2/get-map-tile for details.</dd><dt><span>apiVersion</span></dt><dd>2.0</dd><dt><span>variant</span></dt><dd>microsoft.imagery</dd><dt><span>subscriptionKey</span></dt><dd><insert your subscription key here></dd><dt><span>language</span></dt><dd>en-US</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e444898a-02c4-4000-bd26-af367763ded3" class="xyz-checkbox"/>
                    <label for="e444898a-02c4-4000-bd26-af367763ded3">MicrosoftBaseDarkGrey <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">AzureMaps.MicrosoftBaseDarkGrey</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://atlas.microsoft.com/map/tile?api-version={apiVersion}&tilesetId={variant}&x={x}&y={y}&zoom={z}&language={language}&subscription-key={subscriptionKey}</dd><dt><span>html_attribution</span></dt><dd>See https://docs.microsoft.com/en-us/rest/api/maps/render-v2/get-map-tile for details.</dd><dt><span>attribution</span></dt><dd>See https://docs.microsoft.com/en-us/rest/api/maps/render-v2/get-map-tile for details.</dd><dt><span>apiVersion</span></dt><dd>2.0</dd><dt><span>variant</span></dt><dd>microsoft.base.darkgrey</dd><dt><span>subscriptionKey</span></dt><dd><insert your subscription key here></dd><dt><span>language</span></dt><dd>en-US</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3b0d5380-1ee3-45cb-b0f9-b48fbd8b3a85" class="xyz-checkbox"/>
                    <label for="3b0d5380-1ee3-45cb-b0f9-b48fbd8b3a85">MicrosoftBaseRoad <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">AzureMaps.MicrosoftBaseRoad</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://atlas.microsoft.com/map/tile?api-version={apiVersion}&tilesetId={variant}&x={x}&y={y}&zoom={z}&language={language}&subscription-key={subscriptionKey}</dd><dt><span>html_attribution</span></dt><dd>See https://docs.microsoft.com/en-us/rest/api/maps/render-v2/get-map-tile for details.</dd><dt><span>attribution</span></dt><dd>See https://docs.microsoft.com/en-us/rest/api/maps/render-v2/get-map-tile for details.</dd><dt><span>apiVersion</span></dt><dd>2.0</dd><dt><span>variant</span></dt><dd>microsoft.base.road</dd><dt><span>subscriptionKey</span></dt><dd><insert your subscription key here></dd><dt><span>language</span></dt><dd>en-US</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="3b3aa67a-aec6-4f6e-b9cd-ecb4c817c323" class="xyz-checkbox"/>
                    <label for="3b3aa67a-aec6-4f6e-b9cd-ecb4c817c323">MicrosoftBaseHybridRoad <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">AzureMaps.MicrosoftBaseHybridRoad</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://atlas.microsoft.com/map/tile?api-version={apiVersion}&tilesetId={variant}&x={x}&y={y}&zoom={z}&language={language}&subscription-key={subscriptionKey}</dd><dt><span>html_attribution</span></dt><dd>See https://docs.microsoft.com/en-us/rest/api/maps/render-v2/get-map-tile for details.</dd><dt><span>attribution</span></dt><dd>See https://docs.microsoft.com/en-us/rest/api/maps/render-v2/get-map-tile for details.</dd><dt><span>apiVersion</span></dt><dd>2.0</dd><dt><span>variant</span></dt><dd>microsoft.base.hybrid.road</dd><dt><span>subscriptionKey</span></dt><dd><insert your subscription key here></dd><dt><span>language</span></dt><dd>en-US</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2727c218-f707-49a7-abdf-1baa0d6fa51f" class="xyz-checkbox"/>
                    <label for="2727c218-f707-49a7-abdf-1baa0d6fa51f">MicrosoftTerraMain <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">AzureMaps.MicrosoftTerraMain</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://atlas.microsoft.com/map/tile?api-version={apiVersion}&tilesetId={variant}&x={x}&y={y}&zoom={z}&language={language}&subscription-key={subscriptionKey}</dd><dt><span>html_attribution</span></dt><dd>See https://docs.microsoft.com/en-us/rest/api/maps/render-v2/get-map-tile for details.</dd><dt><span>attribution</span></dt><dd>See https://docs.microsoft.com/en-us/rest/api/maps/render-v2/get-map-tile for details.</dd><dt><span>apiVersion</span></dt><dd>2.0</dd><dt><span>variant</span></dt><dd>microsoft.terra.main</dd><dt><span>subscriptionKey</span></dt><dd><insert your subscription key here></dd><dt><span>language</span></dt><dd>en-US</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="b3c4da9c-da29-49f1-8c49-8c59c09633a4" class="xyz-checkbox"/>
                    <label for="b3c4da9c-da29-49f1-8c49-8c59c09633a4">MicrosoftWeatherInfraredMain <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">AzureMaps.MicrosoftWeatherInfraredMain</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://atlas.microsoft.com/map/tile?api-version={apiVersion}&tilesetId={variant}&x={x}&y={y}&zoom={z}&timeStamp={timeStamp}&language={language}&subscription-key={subscriptionKey}</dd><dt><span>html_attribution</span></dt><dd>See https://docs.microsoft.com/en-us/rest/api/maps/render-v2/get-map-tile#uri-parameters for details.</dd><dt><span>attribution</span></dt><dd>See https://docs.microsoft.com/en-us/rest/api/maps/render-v2/get-map-tile#uri-parameters for details.</dd><dt><span>apiVersion</span></dt><dd>2.0</dd><dt><span>variant</span></dt><dd>microsoft.weather.infrared.main</dd><dt><span>subscriptionKey</span></dt><dd><insert your subscription key here></dd><dt><span>language</span></dt><dd>en-US</dd><dt><span>timeStamp</span></dt><dd>2021-05-08T09:03:00Z</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="20f211ab-58e0-4cee-8fec-9a9de8c8dee2" class="xyz-checkbox"/>
                    <label for="20f211ab-58e0-4cee-8fec-9a9de8c8dee2">MicrosoftWeatherRadarMain <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">AzureMaps.MicrosoftWeatherRadarMain</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://atlas.microsoft.com/map/tile?api-version={apiVersion}&tilesetId={variant}&x={x}&y={y}&zoom={z}&timeStamp={timeStamp}&language={language}&subscription-key={subscriptionKey}</dd><dt><span>html_attribution</span></dt><dd>See https://docs.microsoft.com/en-us/rest/api/maps/render-v2/get-map-tile#uri-parameters for details.</dd><dt><span>attribution</span></dt><dd>See https://docs.microsoft.com/en-us/rest/api/maps/render-v2/get-map-tile#uri-parameters for details.</dd><dt><span>apiVersion</span></dt><dd>2.0</dd><dt><span>variant</span></dt><dd>microsoft.weather.radar.main</dd><dt><span>subscriptionKey</span></dt><dd><insert your subscription key here></dd><dt><span>language</span></dt><dd>en-US</dd><dt><span>timeStamp</span></dt><dd>2021-05-08T09:03:00Z</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="fbb44a7a-6352-425f-b3f8-81f687e19efe" class="xyz-checkbox"/>
                    <label for="fbb44a7a-6352-425f-b3f8-81f687e19efe">SwissFederalGeoportal <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">4 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="e7a9670f-09a0-46b9-924d-cb6a31be39b2" class="xyz-checkbox"/>
                    <label for="e7a9670f-09a0-46b9-924d-cb6a31be39b2">NationalMapColor <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">SwissFederalGeoportal.NationalMapColor</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg</dd><dt><span>html_attribution</span></dt><dd><a target="_blank" href="https://www.swisstopo.admin.ch/">swisstopo</a></dd><dt><span>attribution</span></dt><dd>© swisstopo</dd><dt><span>bounds</span></dt><dd>[[45.398181, 5.140242], [48.230651, 11.47757]]</dd><dt><span>min_zoom</span></dt><dd>2</dd><dt><span>max_zoom</span></dt><dd>18</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="f0386ce3-e7a6-47da-8ec4-f957b3c0842a" class="xyz-checkbox"/>
                    <label for="f0386ce3-e7a6-47da-8ec4-f957b3c0842a">NationalMapGrey <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">SwissFederalGeoportal.NationalMapGrey</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-grau/default/current/3857/{z}/{x}/{y}.jpeg</dd><dt><span>html_attribution</span></dt><dd><a target="_blank" href="https://www.swisstopo.admin.ch/">swisstopo</a></dd><dt><span>attribution</span></dt><dd>© swisstopo</dd><dt><span>bounds</span></dt><dd>[[45.398181, 5.140242], [48.230651, 11.47757]]</dd><dt><span>min_zoom</span></dt><dd>2</dd><dt><span>max_zoom</span></dt><dd>18</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="6e0e1d5d-1763-4796-9718-fb202476947d" class="xyz-checkbox"/>
                    <label for="6e0e1d5d-1763-4796-9718-fb202476947d">SWISSIMAGE <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">SwissFederalGeoportal.SWISSIMAGE</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.swissimage/default/current/3857/{z}/{x}/{y}.jpeg</dd><dt><span>html_attribution</span></dt><dd><a target="_blank" href="https://www.swisstopo.admin.ch/">swisstopo</a></dd><dt><span>attribution</span></dt><dd>© swisstopo</dd><dt><span>bounds</span></dt><dd>[[45.398181, 5.140242], [48.230651, 11.47757]]</dd><dt><span>min_zoom</span></dt><dd>2</dd><dt><span>max_zoom</span></dt><dd>19</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="0166d71f-86c4-4115-8ec8-93ff213dcb74" class="xyz-checkbox"/>
                    <label for="0166d71f-86c4-4115-8ec8-93ff213dcb74">JourneyThroughTime <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">SwissFederalGeoportal.JourneyThroughTime</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.zeitreihen/default/{time}/3857/{z}/{x}/{y}.png</dd><dt><span>html_attribution</span></dt><dd><a target="_blank" href="https://www.swisstopo.admin.ch/">swisstopo</a></dd><dt><span>attribution</span></dt><dd>© swisstopo</dd><dt><span>bounds</span></dt><dd>[[45.398181, 5.140242], [48.230651, 11.47757]]</dd><dt><span>min_zoom</span></dt><dd>2</dd><dt><span>max_zoom</span></dt><dd>18</dd><dt><span>time</span></dt><dd>18641231</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a1dc4324-d0e2-45dc-a094-ecc8a6ae9aa7" class="xyz-checkbox"/>
                    <label for="a1dc4324-d0e2-45dc-a094-ecc8a6ae9aa7">Gaode <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">2 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="af4dc036-1fa8-4906-9479-d311301d5820" class="xyz-checkbox"/>
                    <label for="af4dc036-1fa8-4906-9479-d311301d5820">Normal <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Gaode.Normal</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>attribution</span></dt><dd>&copy; <a href="http://www.gaode.com/">Gaode.com</a></dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="http://www.gaode.com/">Gaode.com</a></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2e60df7d-4121-4229-907a-afc11343e7e4" class="xyz-checkbox"/>
                    <label for="2e60df7d-4121-4229-907a-afc11343e7e4">Satellite <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Gaode.Satellite</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>http://webst01.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}</dd><dt><span>max_zoom</span></dt><dd>19</dd><dt><span>attribution</span></dt><dd>&copy; <a href="http://www.gaode.com/">Gaode.com</a></dd><dt><span>html_attribution</span></dt><dd>&copy; <a href="http://www.gaode.com/">Gaode.com</a></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="a8c9442f-997e-4300-b514-5fd73d9a6061" class="xyz-checkbox"/>
                    <label for="a8c9442f-997e-4300-b514-5fd73d9a6061">Strava <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">5 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="a8a87f4f-9277-4d8a-a67f-1bdbaddf2f05" class="xyz-checkbox"/>
                    <label for="a8a87f4f-9277-4d8a-a67f-1bdbaddf2f05">All <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Strava.All</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://heatmap-external-a.strava.com/tiles/all/hot/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>15</dd><dt><span>attribution</span></dt><dd>Map tiles by <a href="https://labs.strava.com/heatmap">Strava 2021</a></dd><dt><span>html_attribution</span></dt><dd>Map tiles by <a href="https://labs.strava.com/heatmap">Strava 2021</a></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="2e9c9df2-cc83-42ab-bb3b-8af51d64465d" class="xyz-checkbox"/>
                    <label for="2e9c9df2-cc83-42ab-bb3b-8af51d64465d">Ride <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Strava.Ride</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://heatmap-external-a.strava.com/tiles/ride/hot/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>15</dd><dt><span>attribution</span></dt><dd>Map tiles by <a href="https://labs.strava.com/heatmap">Strava 2021</a></dd><dt><span>html_attribution</span></dt><dd>Map tiles by <a href="https://labs.strava.com/heatmap">Strava 2021</a></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="8449b74d-6b8b-4158-adc0-a7bf0cd3e358" class="xyz-checkbox"/>
                    <label for="8449b74d-6b8b-4158-adc0-a7bf0cd3e358">Run <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Strava.Run</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://heatmap-external-a.strava.com/tiles/run/bluered/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>15</dd><dt><span>attribution</span></dt><dd>Map tiles by <a href="https://labs.strava.com/heatmap">Strava 2021</a></dd><dt><span>html_attribution</span></dt><dd>Map tiles by <a href="https://labs.strava.com/heatmap">Strava 2021</a></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="7e6ba8fc-c99c-4c85-92b0-901b8cd078f9" class="xyz-checkbox"/>
                    <label for="7e6ba8fc-c99c-4c85-92b0-901b8cd078f9">Water <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Strava.Water</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://heatmap-external-a.strava.com/tiles/water/blue/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>15</dd><dt><span>attribution</span></dt><dd>Map tiles by <a href="https://labs.strava.com/heatmap">Strava 2021</a></dd><dt><span>html_attribution</span></dt><dd>Map tiles by <a href="https://labs.strava.com/heatmap">Strava 2021</a></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="e48d37a8-0858-4bf9-8a22-56d8612fc97a" class="xyz-checkbox"/>
                    <label for="e48d37a8-0858-4bf9-8a22-56d8612fc97a">Winter <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">Strava.Winter</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://heatmap-external-a.strava.com/tiles/winter/hot/{z}/{x}/{y}.png</dd><dt><span>max_zoom</span></dt><dd>15</dd><dt><span>attribution</span></dt><dd>Map tiles by <a href="https://labs.strava.com/heatmap">Strava 2021</a></dd><dt><span>html_attribution</span></dt><dd>Map tiles by <a href="https://labs.strava.com/heatmap">Strava 2021</a></dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="ec13e1cc-4d2e-4d36-a5c9-c2f7a309e6b4" class="xyz-checkbox"/>
                    <label for="ec13e1cc-4d2e-4d36-a5c9-c2f7a309e6b4">OrdnanceSurvey <span>xyzservices.Bunch</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.Bunch</div>
                        <div class="xyz-name">7 items</div>
                    </div>
                    <div class="xyz-details">
                        <ul class="xyz-collapsible">
    
                <li class="xyz-child">
                    <input type="checkbox" id="0f0c599c-57e6-4fdb-b88d-88d09249d79f" class="xyz-checkbox"/>
                    <label for="0f0c599c-57e6-4fdb-b88d-88d09249d79f">Road <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OrdnanceSurvey.Road</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.os.uk/maps/raster/v1/zxy/Road_3857/{z}/{x}/{y}.png?key={key}</dd><dt><span>html_attribution</span></dt><dd>Contains OS data &copy Crown copyright and database right 2023</dd><dt><span>attribution</span></dt><dd>Contains OS data (C) Crown copyright and database right 2023</dd><dt><span>key</span></dt><dd><insert your valid OS MapsAPI Key. Get a free key here - https://osdatahub.os.uk/></dd><dt><span>min_zoom</span></dt><dd>7</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>max_zoom_premium</span></dt><dd>20</dd><dt><span>bounds</span></dt><dd>[[49.766807, -9.496386], [61.465189, 3.634745]]</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="fd1eafe1-637d-40de-a8ea-2df5c39064cd" class="xyz-checkbox"/>
                    <label for="fd1eafe1-637d-40de-a8ea-2df5c39064cd">Road_27700 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OrdnanceSurvey.Road_27700</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.os.uk/maps/raster/v1/zxy/Road_27700/{z}/{x}/{y}.png?key={key}</dd><dt><span>html_attribution</span></dt><dd>Contains OS data &copy Crown copyright and database right 2023</dd><dt><span>attribution</span></dt><dd>Contains OS data (C) Crown copyright and database right 2023</dd><dt><span>key</span></dt><dd><insert your valid OS MapsAPI Key. Get a free key here - https://osdatahub.os.uk/></dd><dt><span>crs</span></dt><dd>EPSG:27700</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>9</dd><dt><span>max_zoom_premium</span></dt><dd>13</dd><dt><span>bounds</span></dt><dd>[[0, 0], [700000, 1300000]]</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="da68caa6-de71-4652-bb20-bb72e37d86de" class="xyz-checkbox"/>
                    <label for="da68caa6-de71-4652-bb20-bb72e37d86de">Outdoor <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OrdnanceSurvey.Outdoor</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.os.uk/maps/raster/v1/zxy/Outdoor_3857/{z}/{x}/{y}.png?key={key}</dd><dt><span>html_attribution</span></dt><dd>Contains OS data &copy Crown copyright and database right 2023</dd><dt><span>attribution</span></dt><dd>Contains OS data (C) Crown copyright and database right 2023</dd><dt><span>key</span></dt><dd><insert your valid OS MapsAPI Key. Get a free key here - https://osdatahub.os.uk/></dd><dt><span>min_zoom</span></dt><dd>7</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>max_zoom_premium</span></dt><dd>20</dd><dt><span>bounds</span></dt><dd>[[49.766807, -9.496386], [61.465189, 3.634745]]</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="7abb4233-c91b-4b4f-9dd9-e2373d462766" class="xyz-checkbox"/>
                    <label for="7abb4233-c91b-4b4f-9dd9-e2373d462766">Outdoor_27700 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OrdnanceSurvey.Outdoor_27700</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.os.uk/maps/raster/v1/zxy/Outdoor_27700/{z}/{x}/{y}.png?key={key}</dd><dt><span>html_attribution</span></dt><dd>Contains OS data &copy Crown copyright and database right 2023</dd><dt><span>attribution</span></dt><dd>Contains OS data (C) Crown copyright and database right 2023</dd><dt><span>key</span></dt><dd><insert your valid OS MapsAPI Key. Get a free key here - https://osdatahub.os.uk/></dd><dt><span>crs</span></dt><dd>EPSG:27700</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>9</dd><dt><span>max_zoom_premium</span></dt><dd>13</dd><dt><span>bounds</span></dt><dd>[[0, 0], [700000, 1300000]]</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="678ef6d7-c7c0-4a0f-b31b-8edcb675713d" class="xyz-checkbox"/>
                    <label for="678ef6d7-c7c0-4a0f-b31b-8edcb675713d">Light <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OrdnanceSurvey.Light</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.os.uk/maps/raster/v1/zxy/Light_3857/{z}/{x}/{y}.png?key={key}</dd><dt><span>html_attribution</span></dt><dd>Contains OS data &copy Crown copyright and database right 2023</dd><dt><span>attribution</span></dt><dd>Contains OS data (C) Crown copyright and database right 2023</dd><dt><span>key</span></dt><dd><insert your valid OS MapsAPI Key. Get a free key here - https://osdatahub.os.uk/></dd><dt><span>min_zoom</span></dt><dd>7</dd><dt><span>max_zoom</span></dt><dd>16</dd><dt><span>max_zoom_premium</span></dt><dd>20</dd><dt><span>bounds</span></dt><dd>[[49.766807, -9.496386], [61.465189, 3.634745]]</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="5a4ebdd2-5b3d-46bb-a8b2-450045beae21" class="xyz-checkbox"/>
                    <label for="5a4ebdd2-5b3d-46bb-a8b2-450045beae21">Light_27700 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OrdnanceSurvey.Light_27700</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.os.uk/maps/raster/v1/zxy/Light_27700/{z}/{x}/{y}.png?key={key}</dd><dt><span>html_attribution</span></dt><dd>Contains OS data &copy Crown copyright and database right 2023</dd><dt><span>attribution</span></dt><dd>Contains OS data (C) Crown copyright and database right 2023</dd><dt><span>key</span></dt><dd><insert your valid OS MapsAPI Key. Get a free key here - https://osdatahub.os.uk/></dd><dt><span>crs</span></dt><dd>EPSG:27700</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>9</dd><dt><span>max_zoom_premium</span></dt><dd>13</dd><dt><span>bounds</span></dt><dd>[[0, 0], [700000, 1300000]]</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                <li class="xyz-child">
                    <input type="checkbox" id="cd37485b-70c1-4621-bf74-e404d460788c" class="xyz-checkbox"/>
                    <label for="cd37485b-70c1-4621-bf74-e404d460788c">Leisure_27700 <span>xyzservices.TileProvider</span></label>
                    <div class="xyz-inside">
    
            <div>
    
                <div class="xyz-wrap">
                    <div class="xyz-header">
                        <div class="xyz-obj">xyzservices.TileProvider</div>
                        <div class="xyz-name">OrdnanceSurvey.Leisure_27700</div>
                    </div>
                    <div class="xyz-details">
                        <dl class="xyz-attrs">
                            <dt><span>url</span></dt><dd>https://api.os.uk/maps/raster/v1/zxy/Leisure_27700/{z}/{x}/{y}.png?key={key}</dd><dt><span>html_attribution</span></dt><dd>Contains OS data &copy Crown copyright and database right 2023</dd><dt><span>attribution</span></dt><dd>Contains OS data (C) Crown copyright and database right 2023</dd><dt><span>key</span></dt><dd><insert your valid OS MapsAPI Key. Get a free key here - https://osdatahub.os.uk/></dd><dt><span>crs</span></dt><dd>EPSG:27700</dd><dt><span>min_zoom</span></dt><dd>0</dd><dt><span>max_zoom</span></dt><dd>5</dd><dt><span>max_zoom_premium</span></dt><dd>9</dd><dt><span>bounds</span></dt><dd>[[0, 0], [700000, 1300000]]</dd>
                        </dl>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>
    
                    </div>
                </li>
    
                        </ul>
                    </div>
                </div>
            </div>




In this zoom level, the benefits from using OpenStreetMap (such as place
names) do not live to their full potential. Let’s look at a subset of
the travel time matrix: grid cells that are within 15 minutes from the
railway station.

.. code:: ipython3

    ax = accessibility_grid[accessibility_grid.pt_r_t <= 15].plot(
        figsize=(12, 8),
    
        column="pt_r_t",
        scheme="quantiles",
        k=5,
        cmap="Spectral",
        linewidth=0,
        alpha=0.8,
    
        legend=True,
        legend_kwds={"title": "Travel time (min)"}
    )
    contextily.add_basemap(
        ax,
        source=contextily.providers.OpenStreetMap.Mapnik
    )



.. image:: static-maps-2_files/static-maps-2_26_0.png


Finally, we can modify the attribution (copyright notice) displayed in
the bottom left of the map plot. Note that you should *always* respect
the map providers’ terms of use, which typically include a data source
attribution (*contextily*\ ’s defaults take care of this). We can and
should, however, add a data source for any layer we added, such as the
travel time matrix data set:

.. code:: ipython3

    ax = accessibility_grid[accessibility_grid.pt_r_t <= 15].plot(
        figsize=(12, 8),
    
        column="pt_r_t",
        scheme="quantiles",
        k=5,
        cmap="Spectral",
        linewidth=0,
        alpha=0.8,
    
        legend=True,
        legend_kwds={"title": "Travel time (min)"}
    )
    contextily.add_basemap(
        ax,
        source=contextily.providers.OpenStreetMap.Mapnik,
        attribution=(
            "Travel time data (c) Digital Geography Lab, "
            "map data (c) OpenStreetMap contributors"
        )
    )



.. image:: static-maps-2_files/static-maps-2_28_0.png

