
.. figure:: img/AutoGIS_banner.jpg

Automating GIS-processes 2021
==============================

**Welcome to the Automating GIS-processes course 2021!** This course introduces you to geographic data analysis in
the Python programming language through interactive lessons and hands-on exercises. If you are new to Python, we recommend that you start with
the Geo-Python course materials at `https://geo-python.github.io <https://geo-python.github.io>`_ before diving into the GIS stuff in this course.
Geo-Python and Automating GIS processes ("AutoGIS") have been developed at the Department of Geosciences and Geography, University of Helsinki, Finland, and
the materials are openly available for anyone interested.

.. admonition:: Open Access!

    Course materials and recorded lesson videos are **open for everyone**. The aim of this course is to share the
    knowledge and help people to get started with their journey for doing GIS more efficiently and in a reproducible manner
    using Python programming. Feel free to share this website to anyone interested, and to use these materials in your own teaching.
    You can read more info about the license and terms of usage in `here <course-info/License-terms.html>`_.

After completing this course, the students can manage, analyze and visualize spatial data
systematically and efficiently using Python, and critically evaluate the available methods.
In addition to geographic data manipulation and analysis skills (for example, reading and writing files,
managing coordinate reference systems,overlay analysis, network analysis) in Python,
the students continue to learn good programming practices, including the use of a version control system (git) and
documenting and communicating their analysis workflow in online repositories (GitHub).

.. admonition:: Interactive contents

    Each lesson in this course can be turned into an interactive programming session in the browser!
    You can find buttons for activating the python environment using `Thebe <https://thebe.readthedocs.io/en/latest/>`__
    or `Binder <https://mybinder.readthedocs.io/en/latest/>`__ at the top of each programming lesson. Students at Finnish
    higher education institutions are encourage to use the `CSC notebooks <https://notebooks.csc.fi/>`__ environment.

Course format
-------------

The majority of this course will be spent in front of a computer learning to program in the Python language.
The course consists of interactive lectures and weekly exercises. The exercises will focus on developing
basic programming skills using Python and applying those skills to manipulate and analyze geographic information.

Most exercises in this course involve real world examples and data.
For each exercise, you may be asked to submit the Python codes you have written, output figures and answers
to related questions. You are encouraged to discuss and work together with other students while working
on the weekly exercises. The final exercise must be completed individually and
must clearly reflect your own work (in short, don't copy paste from other students).

.. admonition:: University of Helsinki students

    The Automating GIS processes course is part of the
    `Master's Programme in Geography at the University of Helsinki <https://www.helsinki.fi/en/admissions/degree-programmes/geography-masters-programme>`__
    under the course code ``GEOG-329-2``.

.. admonition:: Online teaching

    Please note that the course is organized online during the 2021 Autumn semester.
    Access to Zoom, Slack and CSC notebooks is available to students at Finnish higher education institutes. Recorded
    lesson videos and course materials are openly available to everyone interested.


Course topics by week
---------------------

During this course, we will dive into manipulating and analyzing geographic data in Python. This course builds upon topics
introduced in the Geo-Python course, where we focused on learning the basics of Python programming.
You can find materials from the Geo-Python course at `https://geo-python.github.io <https://geo-python.github.io>`_.

The Automating GIS processes course runs for seven weeks at the University of Helsinki
starting in the second teaching period on Tuesday the 2nd of November 2021. Topics per week are listed below.
Please note that this web page is updated each week before the lesson:

+----------------+---------------------------------+
| Week           | Theme                           |
+================+=================================+
| **1**          | Shapely and geometric objects   |
|                | (points, lines and polygons)    |
|                |                                 |
|                |                                 |
+----------------+---------------------------------+
| **2**          | Managing spatial data with      |
|                | Geopandas (reading and writing  |
|                | data, projections, table joins) |
|                |                                 |
+----------------+---------------------------------+
| **3**          | Geocoding and spatial           |
|                | queries                         |
|                |                                 |
+----------------+---------------------------------+
| **4**          | Reclassifying data,             |
|                | overlay analysis                |
|                |                                 |
+----------------+---------------------------------+
| **5**          | Visualization: static           |
|                | and interactive maps            |
|                |                                 |
+----------------+---------------------------------+
| **6**          | Course recap and                |
|                | Preparing for the final         |
|                | assignment                      |
|                |                                 |
+----------------+---------------------------------+
| **7**          | OpenStreetMap data (osmnx) and  |
|                | Network analysis (networkx)     |
|                |                                 |
+----------------+---------------------------------+
| **Extra**      |  PyQGIS, Raster processing      |
| **materials**  |                                 |
| **for**        |                                 |
| **self-study** |                                 |
+----------------+---------------------------------+

|

.. admonition:: Earlier versions of the course

    Older course materials are available at:
        - `2020 <https://autogis-site.readthedocs.io/en/2020_/>`__
        - `2019 <https://autogis-site.readthedocs.io/en/2019/>`__
        - `2018 <https://autogis-site.readthedocs.io/en/2018_/>`__
        - `2017 <https://automating-gis-processes.github.io/2017/>`__
        - `2016 <https://automating-gis-processes.github.io/2016/>`__

Contents
--------

.. toctree::
   :maxdepth: 1
   :caption: Course information

   course-info/course-info
   course-info/course-environment-components
   course-info/grading
   course-info/learning-goals
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
   :caption: Final Assignment

   lessons/FA/final-assignment
   lessons/FA/final-assignment-grading
   lessons/FA/fa-hints

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





