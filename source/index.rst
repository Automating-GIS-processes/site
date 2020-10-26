
.. figure:: img/AutoGIS_banner.jpg

Automating GIS-processes 2020
==============================

**Welcome to Automating GIS-processes 2020!** This course teaches you how to do different GIS-related tasks in Python programming language.
Each lesson is a tutorial with specific topic(s) where the aim is to learn how to solve common GIS-related problems and
tasks using Python tools. We are using only publicly available data which can be used and downloaded by anyone anywhere.
We also provide a computing environment which allows you to instantly start programming and trying out the materials yourself,
directly in your browser (no installations needed).

Notice: we assume that you know the basics of Python programming. If you are new to Python, we recommend that you start with
the Geo-Python course materials at `https://geo-python.github.io <https://geo-python.github.io>`_. The Automating GIS processes course ("AutoGIS")
is a direct continuation from the Geo-Python course, which is a join effort between the geography and geosciences study programmes at
the University of Helsinki, Finland.

.. admonition:: Open Access!

    Course materials and recorded lesson videos are **open for everyone** on these pages. The aim of this course is to share the
    knowledge and help people to get started with their journey for doing GIS more efficiently and in a reproducible manner
    using Python programming. Feel free to share this website to anyone interested, and to use these materials in your own teaching.
    You can read more info about the license and terms of usage in `here <course-info/License-terms.html>`_.

Course format
-------------

The majority of this course will be spent in front of a computer learning to program with Python programming language and doing practical exercises.

The computer exercises will focus on developing basic programming skills using Python and applying those skills to various GIS related problems.
Typical exercises will involve a brief introduction, followed by topical computer-based tasks and exercises. At the end of the exercises, you are asked
to submit answers to relevant questions, some related plots, and the Python codes you have written.
You are encouraged to discuss and work together with other students on the laboratory exercises, however the laboratory
summary write-ups that you submit must be completed individually and must clearly reflect your own work.


.. admonition:: Online teaching

    Please note that the course is organized completely online during the 2020 Autumn semester.
    Access to zoom, slack and CSC notebooks is available to students at Finnish higher education institutes. Recorded
    lesson videos and course materials are openly available to everyone interested.

.. admonition:: University of Helsinki students

    The Automating GIS processes course is part of the
    `Master's Programme in Geography at the University of Helsinki <https://www.helsinki.fi/en/admissions/degree-programmes/geography-masters-programme>`__.
    under the course code ``GEOG-329-2``.

.. admonition:: Interactive contents

    Each lesson in this course can be turned into an interactive programming session in the browser!
    You can find buttons for activating the python environment using `Thebe <https://thebe.readthedocs.io/en/latest/>`__
    or `Binder <https://mybinder.readthedocs.io/en/latest/>`__ at the top of each programming lesson. Students at Finnish
    higher education institutions are encourage to use the `CSC notebooks <https://notebooks.csc.fi/>`__ environment.


Course topics by week
---------------------

During this course, we will dive into manipulating and analyzing geographic data in Python. This course builds upon topics
introduced in the Geo-Python course, where we focused on learning the basics of Python programming.
You can find materials from the Geo-Python course at `https://geo-python.github.io <https://geo-python.github.io>`_.

The Automating GIS processes course runs for seven weeks at the University of Helsinki
starting in the second teaching period on Tuesday the 27th of October 2020. Topics per week are listed below.
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
| **6**          | OpenStreetMap data (osmnx) and  |
|                | Network analysis (networkx)     |
|                |                                 |
+----------------+---------------------------------+
| **7**          | Course recap and                |
|                | Preparing for the final         |
|                | assignment                      |
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
   :maxdepth: 1
   :caption: Lesson 1

   lessons/L1/overview
   course-motivation.rst
   notebooks/L1/geometric-objects.ipynb
   lessons/L1/exercise-1

..
    .. toctree::
       :maxdepth: 2
       :caption: Lesson 2

       lessons/L2/overview
       lessons/L2/quiz.rst
       notebooks/L2/data_io.ipynb
       notebooks/L2/geopandas-basics.ipynb
       notebooks/L2/projections.ipynb
       notebooks/L2/calculating-distances.ipynb
       notebooks/L2/geopandas-geometries.ipynb
       lessons/L2/exercise-2

    .. toctree::
       :maxdepth: 2
       :caption: Lesson 3

       lessons/L3/overview
       lessons/L3/geocoding
       notebooks/L3/geocoding_in_geopandas.ipynb
       notebooks/L3/point-in-polygon.ipynb
       notebooks/L3/spatial_index.ipynb
       notebooks/L3/spatial-join.ipynb
       notebooks/L3/nearest-neighbour.ipynb
       notebooks/L3/nearest-neighbor-faster.ipynb
       lessons/L3/exercise-3

    .. toctree::
       :maxdepth: 2
       :caption: Lesson 4

       lessons/L4/overview
       notebooks/L4/geometric-operations.ipynb
       notebooks/L4/reclassify.ipynb
       lessons/L4/exercise-4

    .. toctree::
       :maxdepth: 2
       :caption: Lesson 5

       lessons/L5/overview
       notebooks/L5/static_maps.ipynb
       notebooks/L5/interactive-map-folium.ipynb
       notebooks/L5/Employment_in_Finland.ipynb
       lessons/L5/share-on-github
       lessons/L5/exercise-5

    .. toctree::
       :maxdepth: 2
       :caption: Lesson 6

       lessons/L6/overview
       notebooks/L6/retrieve_osm_data.ipynb
       notebooks/L6/network-analysis.ipynb
       lessons/L6/exercise-6

    .. toctree::
       :maxdepth: 2
       :caption: PyQGIS

       lessons/L7/overview
       lessons/L7/pyqgis
       lessons/L7/additional_pyqgis_functions

    .. toctree::
       :maxdepth: 2
       :caption: Raster

       lessons/Raster/overview
       lessons/Raster/download-data
       notebooks/Raster/reading-raster.ipynb
       notebooks/Raster/plotting-raster.ipynb
       notebooks/Raster/clipping-raster.ipynb
       notebooks/Raster/raster-map-algebra.ipynb
       notebooks/Raster/raster-mosaic.ipynb
       notebooks/Raster/zonal-statistics.ipynb
       notebooks/Raster/read-cogs.ipynb

    .. toctree::
       :maxdepth: 2
       :caption: Final Assignment

       lessons/FA/final-assignment
       lessons/FA/final-assignment-grading
       lessons/FA/fa-hints




