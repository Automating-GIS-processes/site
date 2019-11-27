Lesson 5 Overview
=================

This week we will focus on learning how to create beautiful maps in Python and how to share them on GitHub using `GitHub Pages <https://pages.github.com/>`_.

1. `Static maps  <../../notebooks/L5/static_maps.ipynb>`__
2. `Interactive Leaflet maps (Folium and mplleaflet)  <../../notebooks/L5/interactive-map-folium.ipynb>`__
3. :doc:`Sharing interactive maps on GitHub <share-on-github>`
4. :doc:`Exercise 5 <exercise-5>`


We already covered the basics of plotting in Python during the `Geo-Python course week 7 <https://geo-python.github.io/site/lessons/L7/overview.html>`_. As you might remember from that lesson, there are many different Python modules that can be used for making visualizations, and many of them also allows you to create different kinds of maps. 

During this lesson, we will the use of these modules for plotting static and interactive maps:

 - `Matplotlib <http://matplotlib.org/>`_ (static maps, integrated into `Geopandas <http://geopandas.org/>`_)
 - `Folium <https://github.com/python-visualization/folium>`_ (interactive Web maps on Leaflet)
 - `mplleaflet <https://github.com/jwass/mplleaflet>`_ (converts Matplotlib plots easily to interactive Leaflet maps)
 - `contextily <https://github.com/darribas/contextily>`__(for adding basemaps)


Other useful modules to check out (not covered in these course materials):
 - `Plotly Dash <https://plot.ly/dash/>`__ (interactive analytics dashboards)
 - `HoloViews <http://holoviews.org/>`__ and `GeoViews <http://geoviews.org/>`_ 
 - `Bokeh <http://bokeh.pydata.org/en/latest/>`_ (interactive plots)

Learning goals
--------------

After this weeks lesson you should be able to:

 - Create a static map using Geopandas / matplotlib
 - Create a simple interactive map using Folium (or matplotlib + mplleaflet).
 - Share your maps (static / interactive) on GitHub using GitHub pages.


Lecture videos
--------------

.. admonition:: Lesson 5 - Visualizing spatial data in Python: static maps

    .. raw:: html

        <iframe width="560" height="315" src="https://www.youtube.com/embed/p6_1db45e7I" frameborder="0" allowfullscreen></iframe>
        <p>Vuokko Heikinheimo, University of Helsinki <a href="https://www.youtube.com/channel/UCGrJqJjVHGDV5l0XijSAN1Q/playlists">@ AutoGIS channel on Youtube</a>.</p>

    **Contents:**

        - Intro for lesson 5 0:00
        - Excamples for exercise 5 00:47
        - Static maps in geopandas 04:40
        - Adding a basemap using contextily 22:50
        - Subsetting the data 35:05
        - Cropping the map 40:10

.. admonition:: Lesson 5 - Visualizing spatial data in Python: interactive maps

    .. raw:: html

        <iframe width="560" height="315" src="https://www.youtube.com/embed/V0ovj5F-Y3M" frameborder="0" allowfullscreen></iframe>
        <p>Vuokko Heikinheimo, University of Helsinki <a href="https://www.youtube.com/channel/UCGrJqJjVHGDV5l0XijSAN1Q/playlists">@ AutoGIS channel on Youtube</a>.</p>

    **Contents:**

        - Mplleaflet 01:30
        - Folium map 10:10
        - Adding a marker (folium) 21:27
        - Adding a point layer (folium) 27:00
        - Layer control (folium) 31:00
        - Heatmap (folium) 31:50
        - Clustered point map (folium) 37:15
        - Choropleth map (folium) 38:33
        - Exercise 5 intro 50:00
        - Publishing the maps using GitHub pages 52:55



