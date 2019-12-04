Zonal statistics
================

Quite often you have a situtation when you want to summarize raster datasets based on vector geometries.
`Rasterstats <https://github.com/perrygeo/python-rasterstats>`__ is a Python module that does exactly that, easily.

.. ipython:: python

    import rasterio
    from rasterio.plot import show
    from rasterstats import zonal_stats
    import osmnx as ox
    import geopandas as gpd

- Specify filepath, this is the mosaic raster file that was created earlier.

.. ipython:: python

    dem_fp = r"C:\HY-DATA\HENTENKA\KOODIT\Opetus\Automating-GIS-processes\Data\CSC_Lesson6\Helsinki_DEM_2x2m_Mosaic.tif"

- Read in the DEM data

.. ipython:: python

    dem = rasterio.open(dem_fp)


- Specify place names for Kallio and Pihlajamäki that Nominatim can identify https://nominatim.openstreetmap.org/

.. ipython:: python

    kallio_q = "Kallio, Helsinki, Finland"
    pihlajamaki_q = "Pihlajamäki, Malmi, Helsinki, Finland"

- Retrieve 'Kallio' and 'Pihlajamäki' regions from OpenStreetMap

.. ipython:: python

    kallio = ox.gdf_from_place(kallio_q)
    pihlajamaki = ox.gdf_from_place(pihlajamaki_q)

- Reproject the regions to same CRS as the DEM

.. ipython:: python

    kallio = kallio.to_crs(crs=dem.crs.data)
    pihlajamaki = pihlajamaki.to_crs(crs=dem.crs.data)

- Plot the DEM and the regions on top of it

.. ipython:: python

    ax = show((dem, 1))
    kallio.plot(ax=ax, facecolor='None', edgecolor='red', linewidth=2)
    @savefig zonal_stat_areas.png width=450px
    pihlajamaki.plot(ax=ax, facecolor='None', edgecolor='blue', linewidth=2)

**Which one is higher? Kallio or Pihlajamäki? We can use zonal statistics to find out!**

- First we need to get the values of the dem as numpy array and the affine of the raster

.. ipython:: python

    array = dem.read(1)
    affine = dem.affine

- Now we can calculate the zonal statistics by using the function ``zonal_stats``.

.. ipython:: python

    zs_kallio = zonal_stats(kallio, array, affine=affine, stats=['min', 'max', 'mean', 'median', 'majority'])
    zs_pihla = zonal_stats(pihlajamaki, array, affine=affine, stats=['min', 'max', 'mean', 'median', 'majority'])

Okey. So what do we have now?

.. ipython:: python

    print(zs_kallio)
    print(zs_pihla)

Super! Now we can see that ``Pihlajamäki`` seems to be slightly higher compared to ``Kallio``.