Exercise 3
==========

.. image:: https://img.shields.io/badge/launch-CSC%20notebook-blue.svg
   :target: https://notebooks.csc.fi/#/blueprint/d189695c52ad4c0d89ef72572e81b16c


.. admonition:: Start your assignment

    You can start working on your copy of Exercise 3 by `accepting the GitHub Classroom assignment <https://classroom.github.com/a/AAJygAbV>`__.


**Exercise 3 is due by by 17:00 on Thursday the 25th of November 2020** (day before the next practical session).

You can also take a look at the open course copy of `Exercise 3 in the course GitHub repository <https://github.com/AutoGIS-2021/Exercise-3>`__ (does not require logging in).
Note that you should not try to make changes to this copy of the exercise, but rather only to the copy available via GitHub Classroom.


Hints
-----

Coordinate reference systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Remember the difference between defining a crs, and re-projecting a layer to a new crs!
Before re-projecting, the layer should have a valid crs definition which you can check like this: ``data.crs``.

- defining a projection is done like this: ``data.crs = CRS.from_epsg(4326)``  (this command only updates the metadata about coordinate reference system which is stored in the class variable .crs, and does not modify the actual coordinate values. Do this only if the original crs definition is missing or invalid!)
- re-projecting a layer, eg: ``data = data.to_crs(CRS.from_epsg(4326))`` (this one will actually re-project the coordinates in the geometry-column AND re-define the .crs definition)

