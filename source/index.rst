
.. figure:: img/AutoGIS_banner.jpg

Introduction to Python GIS
==============================

**Welcome to the Introduction to Python GIS course 2021!** This is a 3-day course organized by `CSC Finland - IT Center for Science <https://ssl.eventilla.com/event/pENQa>`_ which introduces you to geographic data analysis in the Python programming language through interactive lessons and hands-on exercises. If you are new to Python, we recommend that you start with the Geo-Python course materials at
`https://geo-python.github.io <https://geo-python.github.io>`_ before diving into the GIS stuff in this course. Geo-Python and Automating GIS processes ("AutoGIS") have been developed at the Department of Geosciences and Geography, University of Helsinki, Finland, and the materials are openly available for anyone interested.


Course format
-------------

The majority of this course will be spent in front of a computer learning to program in the Python language.
The course consists of interactive lectures and exercises. The exercises will focus on developing
basic programming skills using Python and applying those skills to manipulate and analyze geographic information.

Schedule
-----------

+----------------+---------------------------------+
| Time           | Theme                           |
+================+=================================+
| **Day 1, Monday 7.3**                            |
+----------------+---------------------------------+
| 9:00-10.30     | Lesson 1: GIS in Python;        |
|                | Spatial Data Model, Shapely,    |
|                | Geometric Objects               |
+----------------+---------------------------------+
| 10:30-10:45    | Coffee break                    |
+----------------+---------------------------------+
| 10:45-12:15    | Lesson 1 continues              |
+----------------+---------------------------------+
| 12:15-13:00    | Lunch break                     |
+----------------+---------------------------------+
| 13:00-14:30    | Lesson 2: Working with          |
|                | (Geo)DataFrames                 |
+----------------+---------------------------------+
| 14:30-14:45    | Coffee break                    |
+----------------+---------------------------------+
| 14:45-16:15    | Lesson 2 continues              |
+----------------+---------------------------------+
| **Day 2, Tuesday 8.3**                           |
+----------------+---------------------------------+
| 9:00-10.30     | Lesson 3: Geocoding and         |
|                | spatial queries                 |
+----------------+---------------------------------+
| 10:30-10:45    | Coffee break                    |
+----------------+---------------------------------+
| 10:45-12:15    | Lesson 3 continues              |
+----------------+---------------------------------+
| 12:15-13:00    | Lunch break                     |
+----------------+---------------------------------+
| 13:00-13:15    | Running Python scripts          |
|                | on CSC's Puhti supercluster     |
+----------------+---------------------------------+
| 13:15-14:30    | Lesson 4: Geometric operations, |
|                | reclassifying data              |
+----------------+---------------------------------+
| 14:30-14:45    | Coffee break                    |
+----------------+---------------------------------+
| 14:45-16:15    | Lesson 4 continues              |
+----------------+---------------------------------+
| **Day 3, Wednesday 9.3**                         |
+----------------+---------------------------------+
| 9:00-10.30     | Lesson 5: Visualization, static |
|                | and interactive maps            |
+----------------+---------------------------------+
| 10:30-10:45    | Coffee break                    |
+----------------+---------------------------------+
| 10:45-12:15    | Lesson 5 continues              |
+----------------+---------------------------------+
| 12:15-13:00    | Lunch break                     |
+----------------+---------------------------------+
| 13:00-14:30    | Lesson 6: Raster data processing|
|                | in Python                       |
+----------------+---------------------------------+
| 14:30-14:45    | Coffee break                    |
+----------------+---------------------------------+
| 14:45-16:15    | Lesson 6 continues              |
+----------------+---------------------------------+
| **Day 4, Thursday 10.3**                         |
+----------------+---------------------------------+
| Optional for course participants,                |
| open to everybody.                               |
+----------------+---------------------------------+
| 12:30-13.30    | Lesson 7: Running Python code   |
|                | in CSC's Puhti supercomputer    |
+----------------+---------------------------------+
| 13:30-13:45    | Coffee break                    |
+----------------+---------------------------------+
| 13:45-15:15    | Lesson 7 continues with         |
|                | hands-on exercise               |
+----------------+---------------------------------+


Instructors
-----------

* Håvard Wallin Aagesen (University of Helsinki)
* Samantha Wittke (CSC)
* Kylli Ek (CSC)

.. admonition:: Interactive contents

    Each lesson in this course can be turned into an interactive programming session in the browser!
    You can find buttons for activating the python environment using `Thebe <https://thebe.readthedocs.io/en/latest/>`__
    or `Binder <https://mybinder.readthedocs.io/en/latest/>`__ at the top of each programming lesson. Students at Finnish
    higher education institutions are encourage to use the `CSC notebooks <https://notebooks.csc.fi/>`__ environment.

Contents
--------

.. toctree::
   :maxdepth: 1
   :caption: Course information

   course-info/course-info
   course-info/course-environment-components
   course-info/installing-miniconda
   course-info/create-python-gis-env
   course-info/resources
   course-info/License-terms


.. toctree::
   :maxdepth: 2
   :caption: Lesson 1

   lessons/L1/overview
   lessons/L1/course-motivation
   notebooks/L1/geometric-objects.ipynb
   lessons/L1/exercise-1

.. toctree::
   :maxdepth: 2
   :caption: Lesson 2

   lessons/L2/overview
   lessons/L2/definitions.rst
   notebooks/L2/00-data-io.ipynb
   notebooks/L2/01-geopandas-basics.ipynb
   notebooks/L2/02-projections.ipynb
   notebooks/L2/03-create-geodataframes.ipynb
   lessons/L2/exercise-2


.. toctree::
   :maxdepth: 2
   :caption: Lesson 3

   lessons/L3/overview
   lessons/L3/geocoding
   notebooks/L3/01_geocoding_in_geopandas.ipynb
   notebooks/L3/02_point-in-polygon.ipynb
   notebooks/L3/03_spatial-join.ipynb
   notebooks/L3/04_nearest-neighbour.ipynb
   notebooks/L3/05_spatial_index.ipynb
   notebooks/L3/06_nearest-neighbor-faster.ipynb
   lessons/L3/exercise-3

.. toctree::
   :maxdepth: 2
   :caption: Lesson 4

   lessons/L4/overview
   notebooks/L4/geometric-operations.ipynb
   notebooks/L4/create_health_district_polygons.ipynb
   notebooks/L4/reclassify.ipynb
   lessons/L4/exercise-4

.. toctree::
   :maxdepth: 2
   :caption: Lesson 5

   lessons/L5/overview
   notebooks/L5/01_static_maps.ipynb
   notebooks/L5/02_interactive-map-folium.ipynb
   notebooks/L5/03_employment_rate_map.ipynb
   lessons/L5/share-on-github
   lessons/L5/exercise-5

.. toctree::
   :maxdepth: 2
   :caption: Lesson 6

   lessons/L6/overview
   notebooks/L6/00_retrieve_osm_data.ipynb
   notebooks/L6/01_network_analysis.ipynb
   lessons/L6/exercise-6



.. toctree::
   :maxdepth: 2
   :caption: Extra: PyQGIS

   lessons/PyQGIS/overview
   lessons/PyQGIS/pyqgis
   lessons/PyQGIS/additional_pyqgis_functions

.. toctree::
   :maxdepth: 2
   :caption: Extra: Raster

   lessons/Raster/overview
   lessons/Raster/download-data
   notebooks/Raster/reading-raster.ipynb
   notebooks/Raster/plotting-raster.ipynb
   notebooks/Raster/clipping-raster.ipynb
   notebooks/Raster/raster-map-algebra.ipynb
   notebooks/Raster/raster-mosaic.ipynb
   notebooks/Raster/zonal-statistics.ipynb
   notebooks/Raster/read-cogs.ipynb

.. .. toctree::
   :maxdepth: 2
   :caption: Final Assignment

   lessons/FA/final-assignment
   lessons/FA/final-assignment-grading
   lessons/FA/fa-hints



