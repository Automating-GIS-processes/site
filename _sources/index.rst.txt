
.. figure:: img/AutoGIS_banner.jpg

Welcome to Automating GIS-processes 2018!
=========================================

**Automating GIS-processes** -course teaches you how to do different GIS-related tasks in Python programming language.
Each lesson is a tutorial with specific topic(s) where the aim is to learn how to solve common GIS-related problems and
tasks using Python tools. We are using only publicly available data which can be used and downloaded by anyone anywhere.
We also provide a computing environment which allows you to instantly start programming and trying out the materials yourself,
directly in your browser (no installations needed).

Notice: we assume that you know the basics of Python programming. If Python is not familiar to you, we recommend to start with
our earlier course that prepares you for this course, and focuses on learning the basics of Python, see `geo-python.github.io <https://geo-python.github.io>`_.

Course format
-------------

The majority of this course will be spent in front of a computer learning to program with Python programming language and doing practical exercises.
During Teaching Period I, the Automating GIS-processes and `Introduction to Quantitative Geology <https://introqg.github.io>`_ courses met together and focused on
`learning the basics of programming with Python <https://geo-python.github.io>`_. Previously, both these courses lacked sufficient time for students to properly learn the basic concepts of programming in Python.

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
    Please read more about how to do it from `here <License-terms.html>`_.

.. admonition:: Earlier versions of the course

    Older course materials are available at:
        - `2017 <https://automating-gis-processes.github.io/2017/>`__
        - `2016 <https://automating-gis-processes.github.io/2016/>`__

    Note, that the contents of the course are updated for each year. Hence, the older course materials may not be used, and they
    might be outdated.


Course topics by week
---------------------
See earlier materials for learning the basics of Python programming from `here <https://geo-python.github.io>`_.

The materials are divided into weekly sections that are published at these pages every Monday morning. Lessons are held with following schedule:

+----------------+---------------------------------+
| Time           | Theme                           |
+================+=================================+
| **Class 1**    | GIS in Python;                  |
|   29.10.2018   | Spatial data model;             |
|                | Geometric Objects; Shapely      |
|                |                                 |
+----------------+---------------------------------+
| **Class 2**    | Working with GeoDataFrames;     |
|  5.11.2018     | Managing projections;           |
|                | Table join;                     |
|                |                                 |
+----------------+---------------------------------+
| **Class 3**    | Geocoding and making spatial    |
|  12.11.2018    | queries                         |
|                |                                 |
|                |                                 |
+----------------+---------------------------------+
| **Class 4**    | Geometric operations;           |
|  19.11.2018    | Reclassifying data with Pysal   |
|                |                                 |
+----------------+---------------------------------+
| **Class 5**    | Visualization, making static    |
|  26.11.2018    | and interactive maps            |
|                |                                 |
+----------------+---------------------------------+
| **Class 6**    | Network analysis and routing    |
|  3.12.2018     | in Python (transport modelling) |
|                |                                 |
+----------------+---------------------------------+
| **Class 7**    | Using Python programming in     |
|  10.12.2018    | QGIS                            |
|                |                                 |
+----------------+---------------------------------+

|

Contents
--------
*Lesson content, readings and due dates are subject to change*

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
   lessons/L1/ex-1
   lessons/L1/exercise-1-hints