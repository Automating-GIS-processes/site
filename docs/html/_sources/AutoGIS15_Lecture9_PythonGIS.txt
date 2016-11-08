
Automating GIS-processes - Lecture 9: Python GIS
================================================

Useful functionalities for processing the data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*Pandas* and *Geopandas* have many useful functionalities for managing
the data. This lecture focuses on showing how few of them can be used.

Grouping data
~~~~~~~~~~~~~

One useful function that can be used in Pandas/Geopandas is
***.groupby()***. This function groups data based on values on selected
column(s) (similar to what we did with earlier with arcpy and
modelbuilder).

Let's do one more time the grouping of the individual fishes in
'DAMSELFISH.shp' and export the species to individual Shapefiles.

.. code:: python

    # Import the necessary modules
    import geopandas as gpd
    import pandas as pd
    import os
    
    # Set file path
    fp = r"C:\HY-Data\HENTENKA\Data\DAMSELFISH_distributions.shp"
    
    # Read the data
    data = gpd.read_file(fp)
    
    # Let's see what the data looks like
    data.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>ORIG_FID</th>
          <th>binomial</th>
          <th>category</th>
          <th>citation</th>
          <th>class_name</th>
          <th>compiler</th>
          <th>dist_comm</th>
          <th>family_nam</th>
          <th>genus_name</th>
          <th>geometry</th>
          <th>...</th>
          <th>rl_update</th>
          <th>seasonal</th>
          <th>shape_Area</th>
          <th>shape_Leng</th>
          <th>source</th>
          <th>species_na</th>
          <th>subpop</th>
          <th>subspecies</th>
          <th>tax_comm</th>
          <th>year</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>0</td>
          <td>Stegastes leucorus</td>
          <td>VU</td>
          <td>International Union for Conservation of Nature...</td>
          <td>ACTINOPTERYGII</td>
          <td>IUCN</td>
          <td>None</td>
          <td>POMACENTRIDAE</td>
          <td>Stegastes</td>
          <td>POLYGON ((-115.6437454219999 29.71392059300007...</td>
          <td>...</td>
          <td>2012.1</td>
          <td>1</td>
          <td>28.239363</td>
          <td>82.368856</td>
          <td>None</td>
          <td>leucorus</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>2010</td>
        </tr>
        <tr>
          <th>1</th>
          <td>0</td>
          <td>Stegastes leucorus</td>
          <td>VU</td>
          <td>International Union for Conservation of Nature...</td>
          <td>ACTINOPTERYGII</td>
          <td>IUCN</td>
          <td>None</td>
          <td>POMACENTRIDAE</td>
          <td>Stegastes</td>
          <td>POLYGON ((-105.589950704 21.89339825500002, -1...</td>
          <td>...</td>
          <td>2012.1</td>
          <td>1</td>
          <td>28.239363</td>
          <td>82.368856</td>
          <td>None</td>
          <td>leucorus</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>2010</td>
        </tr>
        <tr>
          <th>2</th>
          <td>0</td>
          <td>Stegastes leucorus</td>
          <td>VU</td>
          <td>International Union for Conservation of Nature...</td>
          <td>ACTINOPTERYGII</td>
          <td>IUCN</td>
          <td>None</td>
          <td>POMACENTRIDAE</td>
          <td>Stegastes</td>
          <td>POLYGON ((-111.159618439 19.01535626700007, -1...</td>
          <td>...</td>
          <td>2012.1</td>
          <td>1</td>
          <td>28.239363</td>
          <td>82.368856</td>
          <td>None</td>
          <td>leucorus</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>2010</td>
        </tr>
        <tr>
          <th>3</th>
          <td>1</td>
          <td>Chromis intercrusma</td>
          <td>LC</td>
          <td>International Union for Conservation of Nature...</td>
          <td>ACTINOPTERYGII</td>
          <td>IUCN</td>
          <td>None</td>
          <td>POMACENTRIDAE</td>
          <td>Chromis</td>
          <td>POLYGON ((-80.86500229899997 -0.77894492099994...</td>
          <td>...</td>
          <td>2012.1</td>
          <td>1</td>
          <td>87.461539</td>
          <td>729.012180</td>
          <td>None</td>
          <td>intercrusma</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>2010</td>
        </tr>
        <tr>
          <th>4</th>
          <td>1</td>
          <td>Chromis intercrusma</td>
          <td>LC</td>
          <td>International Union for Conservation of Nature...</td>
          <td>ACTINOPTERYGII</td>
          <td>IUCN</td>
          <td>None</td>
          <td>POMACENTRIDAE</td>
          <td>Chromis</td>
          <td>POLYGON ((-67.33922225599997 -55.6761029239999...</td>
          <td>...</td>
          <td>2012.1</td>
          <td>1</td>
          <td>87.461539</td>
          <td>729.012180</td>
          <td>None</td>
          <td>intercrusma</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>2010</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 27 columns</p>
    </div>



In the column 'binomial' we have the individual fish species defined and
we can use that column for grouping the data with .groupby() function.

.. code:: python

    # Group the data by column 'binomial'
    grouped = data.groupby('binomial')
    
    # Let's see what we got
    grouped




.. parsed-literal::

    <pandas.core.groupby.DataFrameGroupBy object at 0x0000000003FB6710>



Group by function gives us an object called *DataFrameGroupBy* which is
similar to list of keys and values that we can iterate over.

.. code:: python

    # Iterate over the group object 
    
    for key, values in grouped:
        individual_fish = values
        
    # Let's see what is the LAST item that we iterated
    individual_fish




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>ORIG_FID</th>
          <th>binomial</th>
          <th>category</th>
          <th>citation</th>
          <th>class_name</th>
          <th>compiler</th>
          <th>dist_comm</th>
          <th>family_nam</th>
          <th>genus_name</th>
          <th>geometry</th>
          <th>...</th>
          <th>rl_update</th>
          <th>seasonal</th>
          <th>shape_Area</th>
          <th>shape_Leng</th>
          <th>source</th>
          <th>species_na</th>
          <th>subpop</th>
          <th>subspecies</th>
          <th>tax_comm</th>
          <th>year</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>27</th>
          <td>8</td>
          <td>Teixeirichthys jordani</td>
          <td>LC</td>
          <td>Red List Index (Sampled Approach), Zoological ...</td>
          <td>ACTINOPTERYGII</td>
          <td>None</td>
          <td>None</td>
          <td>POMACENTRIDAE</td>
          <td>Teixeirichthys</td>
          <td>POLYGON ((121.6300326400001 33.04248618400004,...</td>
          <td>...</td>
          <td>2012.2</td>
          <td>1</td>
          <td>116.786519</td>
          <td>498.057966</td>
          <td>None</td>
          <td>jordani</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>2012</td>
        </tr>
        <tr>
          <th>28</th>
          <td>8</td>
          <td>Teixeirichthys jordani</td>
          <td>LC</td>
          <td>Red List Index (Sampled Approach), Zoological ...</td>
          <td>ACTINOPTERYGII</td>
          <td>None</td>
          <td>None</td>
          <td>POMACENTRIDAE</td>
          <td>Teixeirichthys</td>
          <td>POLYGON ((32.56219482400007 29.97488975500005,...</td>
          <td>...</td>
          <td>2012.2</td>
          <td>1</td>
          <td>116.786519</td>
          <td>498.057966</td>
          <td>None</td>
          <td>jordani</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>2012</td>
        </tr>
        <tr>
          <th>29</th>
          <td>8</td>
          <td>Teixeirichthys jordani</td>
          <td>LC</td>
          <td>Red List Index (Sampled Approach), Zoological ...</td>
          <td>ACTINOPTERYGII</td>
          <td>None</td>
          <td>None</td>
          <td>POMACENTRIDAE</td>
          <td>Teixeirichthys</td>
          <td>POLYGON ((130.9052090560001 34.02498196400006,...</td>
          <td>...</td>
          <td>2012.2</td>
          <td>1</td>
          <td>116.786519</td>
          <td>498.057966</td>
          <td>None</td>
          <td>jordani</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>2012</td>
        </tr>
        <tr>
          <th>30</th>
          <td>8</td>
          <td>Teixeirichthys jordani</td>
          <td>LC</td>
          <td>Red List Index (Sampled Approach), Zoological ...</td>
          <td>ACTINOPTERYGII</td>
          <td>None</td>
          <td>None</td>
          <td>POMACENTRIDAE</td>
          <td>Teixeirichthys</td>
          <td>POLYGON ((56.32233070000007 -3.707270205999976...</td>
          <td>...</td>
          <td>2012.2</td>
          <td>1</td>
          <td>116.786519</td>
          <td>498.057966</td>
          <td>None</td>
          <td>jordani</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>2012</td>
        </tr>
        <tr>
          <th>31</th>
          <td>8</td>
          <td>Teixeirichthys jordani</td>
          <td>LC</td>
          <td>Red List Index (Sampled Approach), Zoological ...</td>
          <td>ACTINOPTERYGII</td>
          <td>None</td>
          <td>None</td>
          <td>POMACENTRIDAE</td>
          <td>Teixeirichthys</td>
          <td>POLYGON ((40.64476131800006 -10.85502363999996...</td>
          <td>...</td>
          <td>2012.2</td>
          <td>1</td>
          <td>116.786519</td>
          <td>498.057966</td>
          <td>None</td>
          <td>jordani</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>2012</td>
        </tr>
        <tr>
          <th>32</th>
          <td>8</td>
          <td>Teixeirichthys jordani</td>
          <td>LC</td>
          <td>Red List Index (Sampled Approach), Zoological ...</td>
          <td>ACTINOPTERYGII</td>
          <td>None</td>
          <td>None</td>
          <td>POMACENTRIDAE</td>
          <td>Teixeirichthys</td>
          <td>POLYGON ((48.11258402900006 -9.335103113999935...</td>
          <td>...</td>
          <td>2012.2</td>
          <td>1</td>
          <td>116.786519</td>
          <td>498.057966</td>
          <td>None</td>
          <td>jordani</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>2012</td>
        </tr>
        <tr>
          <th>33</th>
          <td>8</td>
          <td>Teixeirichthys jordani</td>
          <td>LC</td>
          <td>Red List Index (Sampled Approach), Zoological ...</td>
          <td>ACTINOPTERYGII</td>
          <td>None</td>
          <td>None</td>
          <td>POMACENTRIDAE</td>
          <td>Teixeirichthys</td>
          <td>POLYGON ((51.75403543100003 -9.21679305899994,...</td>
          <td>...</td>
          <td>2012.2</td>
          <td>1</td>
          <td>116.786519</td>
          <td>498.057966</td>
          <td>None</td>
          <td>jordani</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>2012</td>
        </tr>
      </tbody>
    </table>
    <p>7 rows × 27 columns</p>
    </div>



.. code:: python

    # Let's check the type of the grouped object
    type(individual_fish)




.. parsed-literal::

    geopandas.geodataframe.GeoDataFrame



.. code:: python

    # Let's check what the 'key' variable contains
    key




.. parsed-literal::

    'Teixeirichthys jordani'



As can be seen from the example above, each set of data are now grouped
into separate GeoDataFrames that we can export into Shapefiles using the
variable 'key' for creating the output filepath names. Let's now export
those species into individual Shapefiles.

.. code:: python

    # Determine outputpath
    outFolder = r"C:\HY-Data\HENTENKA\Data"
    
    # Create a new folder called 'Results' (if does not exist) to that folder using os.makedirs() function
    resultFolder = os.path.join(outFolder, 'Results')
    if not os.path.exists(resultFolder):
        os.makedirs(resultFolder)
    
    # Iterate over the 
    for key, values in grouped:
        # Format the filename
        outName = "%s.shp" % key.replace(" ", "_")
        
        # Print some information for the user
        print("Processing: %s" % key)
        
        # Create an output path
        outpath = os.path.join(resultFolder, outName)
        
        # Export the data
        values.to_file(outpath)
    


.. parsed-literal::

    Processing: Abudefduf concolor
    Processing: Abudefduf declivifrons
    Processing: Abudefduf troschelii
    Processing: Amphiprion sandaracinos
    Processing: Azurina eupalama
    Processing: Azurina hirundo
    Processing: Chromis alpha
    Processing: Chromis alta
    Processing: Chromis atrilobata
    Processing: Chromis crusma
    Processing: Chromis cyanea
    Processing: Chromis flavicauda
    Processing: Chromis intercrusma
    Processing: Chromis limbaughi
    Processing: Chromis pembae
    Processing: Chromis punctipinnis
    Processing: Chrysiptera flavipinnis
    Processing: Hypsypops rubicundus
    Processing: Microspathodon bairdii
    Processing: Microspathodon dorsalis
    Processing: Nexilosus latifrons
    Processing: Stegastes acapulcoensis
    Processing: Stegastes arcifrons
    Processing: Stegastes baldwini
    Processing: Stegastes beebei
    Processing: Stegastes flavilatus
    Processing: Stegastes leucorus
    Processing: Stegastes rectifraenum
    Processing: Stegastes redemptus
    Processing: Teixeirichthys jordani
    
