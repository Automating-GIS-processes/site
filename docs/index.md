# Automating GIS Processes {{year}}


**Welcome to the *Automating GIS processes* course {{year}}!** Through interactive
lessons and hands-on exercises, this course introduces you to geographic data
analysis using the Python programming language. If you are new to Python, we
recommend you first start with the *Geo-Python* course
([geo-python.readthedocs.io](https://geo-python.readthedocs.io/)) before diving
into using it for GIS analyses in this course.

*Geo-Python* and *Automating GIS processes* (‘AutoGIS’) have been developed at
the Department of Geosciences and Geography, University of Helsinki, Finland,
and the teaching material is openly available for anyone interested.


:::{admonition} Open Access
:class: info

Course material and videos are **open for everyone**. The aim of this course is
to share the knowledge and help people to get started with their journey
towards doing GIS analyses more efficiently and in a better reproducible
manner: using Python and its manifold modules. Feel free to share this website
with anyone interested, and use the provided material in your own teaching. 

Read more about the license and terms of usage 
<a href="course-info/license.html">here</a>.

:::


After completing this course, a student is able to manage, analyse, and
visualise spatial data efficiently and in a systematic manner, using Python.
They also know how to evaluate available methods critically. Besides learning
how to handle, manipulate, and analyse geographic data (e.g., read and write
files, manage coordinate reference systems, conduct overlay analysis or network
analysis), students also get to know good programming practices, the benefits of
using a version control system (`git`), and how to document and communicate
their analysis workflow in an online repository (GitHub).



:::{admonition} Interactive content
:class: info

Each lesson in this course can be turned into an interactive programming session
in the browser. You’ll find buttons for activating the python environment using
<a href="https://mybinder.readthedocs.io/">Binder</a> at the top of each
programming lesson. Students at Finnish higher education institutions are
encouraged to use <a href="https://notebooks.csc.fi/">CSC’s *Notebooks*</a>.

:::


## Course format

The majority of this course will be spent in front of a computer learning to
program in the Python language. The course consists of interactive lectures and
weekly exercises. The exercises will focus on developing basic programming
skills using Python and applying those skills to manipulate and analyse
geographic information.

Most exercises in this course involve real world examples and data. For each
exercise, you may be asked to submit the Python codes you have written, output
figures and answers to related questions. You are encouraged to discuss and
work together with other students while working on the weekly exercises. The
final exercise must be completed individually and must clearly reflect your own
work.


:::{admonition} Students at the University of Helsinki
:class: hint

The *Automating GIS processes* course is part of the <a
href="https://www.helsinki.fi/en/degree-programmes/geography-masters-programme">Master's
Programme in Geography</a>, its course code is
<a href="https://studies.helsinki.fi/courses/?searchText=GEOG-329-2">`GEOG-329-2`</a>. 
We recommend you complete *Introduction to advanced geoinformatics* 
(<a href="https://studies.helsinki.fi/courses/?searchText=GEOG-G301">`GEOG-G301`</a>)
before enrolling into this course, and expect basic skills in Python programming, which you can acquire, for instance, in *Geo-Python*
(<a href="https://studies.helsinki.fi/courses/?searchText=GEOG-329-1">`GEOG-329-1`</a>).

:::


## Course topics by week

Over the course of seven weeks, we will dive into manipulating and analysing
geographic data in Python. This course builds upon the skills introduced in the
*[GeoPython](https://geo-python.readthedocs.io/)* course, which focusses on
learning the basics of Python programming. 

At the University of Helsinki, the *Automating GIS processes* course runs for
seven weeks during the second teaching period in the autumn semester, starting
on {{starting_date}}.

During the teaching period, this web page is updated each week before the lecture.

| week  | theme                                                                                     |
| ----- | ----------------------------------------------------------------------------------------- |
| **1** | Shapely and geometry objects (points, lines and polygons)                                |
| **2** | Managing spatial data with GeoPandas (reading and writing data, projections, table joins) |
| **3** | Geocoding and spatial queries                                                             |
| **4** | Reclassifying data, overlay analysis                                                      |
| **5** | Visualisation: static and interactive maps                                                |
| **6** | Course recap and preparing for the final assignment                                       |
| **7** | OpenStreetMap data (osmnx) and Network analysis (networkx)                                |
| **extra material for self‑study** | PyQGIS, Raster processing                                     |
|       |                                                                                           |


## Earlier versions of this course

The course pages and material of earlier years are available at:

- [2021](https://autogis-site.readthedocs.io/en/2021/)
- [2020](https://autogis-site.readthedocs.io/en/2020_/)
- [2019](https://autogis-site.readthedocs.io/en/2019/)
- [2018](https://autogis-site.readthedocs.io/en/2018_/)
- [2017](https://automating-gis-processes.github.io/2017/)
- [2016](https://automating-gis-processes.github.io/2016/)


## Contents

```{toctree}
---
caption: Course information
maxdepth: 1
---

course-info/general-information
course-info/course-environment
course-info/grading
course-info/learning-goals
course-info/installing-python
course-info/create-python-gis-environment
course-info/resources
course-info/license
```

```{toctree}
---
caption: Lesson 1
maxdepth: 2
---
lessons/lesson-1/overview
lessons/lesson-1/course-motivation
lessons/lesson-1/geometry-objects
lessons/lesson-1/exercise-1
```

```{toctree}
---
caption: Lesson 2
maxdepth: 2
---
lessons/lesson-2/overview
lessons/lesson-2/key-concepts
lessons/lesson-2/managing-file-paths
lessons/lesson-2/vector-data-io
lessons/lesson-2/geopandas-an-introduction
lessons/lesson-2/map-projections
lessons/lesson-2/exercise-2
```

```{toctree}
---
caption: Lesson 3
maxdepth: 2
---
lessons/lesson-3/overview
lessons/lesson-3/geocoding
lessons/lesson-3/geocoding-in-geopandas
lessons/lesson-3/point-in-polygon-queries
lessons/lesson-3/intersect
lessons/lesson-3/spatial-join
lessons/lesson-3/exercise-3
```

```{toctree}
---
caption: Lesson 4
maxdepth: 2
---
lessons/lesson-4/overview
lessons/lesson-4/overlay-analysis
lessons/lesson-4/vector-data-aggregating
lessons/lesson-4/simplifying-geometries
lessons/lesson-4/reclassifying-data
lessons/lesson-4/exercise-4
```

```{toctree}
---
caption: Lesson 5
maxdepth: 2
---
lessons/lesson-5/overview
lessons/lesson-5/static-maps
lessons/lesson-5/interactive-maps
lessons/lesson-5/exercise-5
```

```{toctree}
---
caption: Lesson 6
maxdepth: 2
---
lessons/lesson-6/overview
lessons/lesson-6/retrieve-data-from-openstreetmap
lessons/lesson-6/network-analysis
```

```{toctree}
---
caption: Final Assignment
maxdepth: 2
---
final-assignment/final-assignment
final-assignment/final-assignment-grading
final-assignment/final-assignment-hints
```

% ```{toctree}
% ---
% caption: "Extra: PyQGIS"
% maxdepth: 2
% ---
% extra/pyqgis/overview
% extra/pyqgis/pyqgis
% extra/pyqgis/additional_pyqgis_functions
% ```

% ```{toctree}
% ---
% caption: "Extra: Raster handling in Python"
% maxdepth: 2
% ---
% extra/raster/overview
% extra/raster/download-data
% extra/raster/reading-raster
% extra/raster/plotting-raster
% extra/raster/clipping-raster
% extra/raster/raster-map-algebra
% extra/raster/raster-mosaic
% extra/raster/zonal-statistics
% extra/raster/read-cogs
% ```
