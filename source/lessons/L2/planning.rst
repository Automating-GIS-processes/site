Planning
--------

Last year there was only Pandas as Geopandas stuff. Now we have more time to focus on Geopandas.

**Things to cover in Lesson 2:**

- Reading / writing Shapefile
- Basic structure / attributes of a GeoDataFrame
- Working with geometries in GeoDataFrame (calculating areas etc.)
- Iterating over rows and creating a LineString from centroid of Polygons to specific destination point (to demonstrate the usefulness of apply function)
- Projections --> Reprojecting data
    - We could create a function that returns a GeoDataFrame with identical crs for each input dataset
- Recap of a table join

**Things to cover in Lesson 3:**

- Geocoding, using Nominatim (http://nominatim.openstreetmap.org/) --> provider='nominatim' --> does not require API key
- Point in Polygon / Intersect
- Spatial Join
- Nearest point (scipy.spatial)

**Things to cover in Lesson 4:**

- Overlay analysis
- Aggregating data
- Simplifying geometries
- Data reclassification (own made + pysal)

**Things to cover in Lesson 5:**

- Visualizing static maps (how to put layers on top of each other)
  - Create a subplot with different maps and a graph
- Visualizing interactive maps with Bokeh
  - Use map tiles e.g. from OpenStreetMap
- Create functions that handles MultiPolygon and MultiLineStrings (show the problem)








