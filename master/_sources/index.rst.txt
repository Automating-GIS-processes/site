
.. figure:: img/AutoGIS_banner.jpg

Welcome to Automating GIS-processes 2019!
=========================================

**Automating GIS-processes** -course teaches you how to do different GIS-related tasks in Python programming language.
Each lesson is a tutorial with specific topic(s) where the aim is to learn how to solve common GIS-related problems and
tasks using Python tools. We are using only publicly available data which can be used and downloaded by anyone anywhere.
We also provide a computing environment which allows you to instantly start programming and trying out the materials yourself,
directly in your browser (no installations needed).

Notice: we assume that you know the basics of Python programming. If you are new to Python, we recommend that you start with
the `Geo-Python course materials at geo-python.github.io <https://geo-python.github.io>`_. The Automating GIS processes course ("AutoGIS")
is a direct continuation from the Geo-Python course, which is a join effort between the geography and geology study programmes at
the University of Helsinki, Finland.

Course format
-------------

The majority of this course will be spent in front of a computer learning to program with Python programming language and doing practical exercises.

The computer exercises will focus on developing basic programming skills using Python and applying those skills to various GIS related problems.
Typical exercises will involve a brief introduction, followed by topical computer-based tasks and exercises. At the end of the exercises, you are asked
to submit answers to relevant questions, some related plots, and the Python codes you have written.
You are encouraged to discuss and work together with other students on the laboratory exercises, however the laboratory
summary write-ups that you submit must be completed individually and must clearly reflect your own work.

.. admonition:: Open Access!

    The course is **open for everyone**. The aim of this course is to share the knowledge and help people to get started with their journey for doing GIS more efficiently and in a reproducible manner
    using Python programming.

.. admonition:: Step by step instructions with cloud computing

    The materials are written in a way that you can follow them step by step exactly as they are written, as long as you use the cloud computing resources that
    we provide for you using `Binder <https://mybinder.readthedocs.io/en/latest/>`__ and `CSC Finland <https://www.csc.fi/>`__ cloud computing resources (for Finnish students).
    If you work from your own computer, **you need to adjust the file paths to the data** accordingly.

.. admonition:: For teachers

    If you would like to use these materials for your own teaching or develop them further, we highly support that.
    Please read more about how to do it from `here <course-info/License-terms.html>`_.

.. admonition:: Earlier versions of the course

    Older course materials are available at:
        - `2018 <https://automating-gis-processes.github.io/site/2018>`__
        - `2017 <https://automating-gis-processes.github.io/2017/>`__
        - `2016 <https://automating-gis-processes.github.io/2016/>`__

    Note, that the older course materials might be outdated.


Course topics by week
---------------------
In teaching period 1 (Geo-Python), we focused on learning the basics of Python programming.
See the materials on the `Geo-Python course page <https://geo-python.github.io>`_.

In teaching period 2 (Automating GIS processes), we dive into spatial data management and analysis using python.
This part of the course runs for seven weeks starting on Monday the 28th of October 2019.

Lesson materials are published on these pages each week on Monday, after which they are publicly available for anyone interested:

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
|                |                                 |
+----------------+---------------------------------+
| **4**          |  Reclassifying data,            |
|                |  overlay analysis               |
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
| **7**          | Raster processing (rasterio)    |
|                | Python in QGIS demo             |
|                |                                 |
+----------------+---------------------------------+

|

Contents
--------
*Lesson materials are updated on these pages each week on Monday*

.. toctree::
   :maxdepth: 2
   :caption: Course information

   course-info/course-info
   course-info/course-environment-components
   course-info/grading
   course-info/learning-goals
   course-info/Installing_Anacondas_GIS
   course-info/resources
   course-info/License-terms

.. toctree::
   :maxdepth: 2
   :caption: Lesson 1

   lessons/L1/Intro-Python-GIS
   lessons/L1/overview
   notebooks/L1/geometric-objects.ipynb
   lessons/L1/exercise-1

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
   lessons/L3/exercise-3

    .. toctree::
       :maxdepth: 2
       :caption: Lesson 4

       lessons/L4/overview
       notebooks/L4/reclassify.ipynb
       notebooks/L4/geometric-operations.ipynb
       lessons/L4/exercise-4

    .. toctree::
       :maxdepth: 2
       :caption: Lesson 5

       lessons/L5/overview
       notebooks/L5/static_maps.ipynb
       notebooks/L5/interactive-map-folium.ipynb
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
       :caption: Lesson 7

       lessons/L7/overview
       lessons/L7/pyqgis
       lessons/L7/processing-toolbox
       lessons/L7/processing-script
       lessons/L7/exercise-7

    .. toctree::
       :maxdepth: 2
       :caption: Final Assignment

       lessons/FA/final-assignment

