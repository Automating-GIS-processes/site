Nearest Neighbour Analysis
==========================

One commonly used GIS task is to be able to find the nearest neighbour. For instance, you might have a single Point object
representing your home location, and then another set of locations representing e.g. public transport stops. Then, quite typical question is *"which of the stops is closest one to my home?"*
This is a typical nearest neighbour analysis, where the aim is to find the closest geometry to another geometry.

In Python this kind of analysis can be done with shapely function called ``nearest_points()`` that `returns a tuple of the nearest points in the input geometrie <https://shapely.readthedocs.io/en/latest/manual.html#shapely.ops.nearest_points>`__.

