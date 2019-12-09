Automatize data download
========================

For this lesson, we need to download data from couple of different places. For this purpose I will show
how to download data automatically using Python programming which might be quite useful thing to know.

The data files that we are using in this tutorial will be obtained from `PaITuli spatial data service <https://avaa.tdata.fi/web/paituli/latauspalvelu>`__.
We will be using Landsat 8 image from Helsinki area produced by NASA, USGS & Latuviitta which I have already clipped to reduce the size of the file (raster files are often fairly large in size),
and a 2mx2m Digital Elevation Model (DEM) produced by National Land Survey of Finland.

You can download those files into your computer automatically with following script in which we will be using `urllib module <https://docs.python.org/3/library/urllib.html>`__ to download the data with Python:

.. code:: python

    import os
    import urllib

    def get_filename(url):
        """
        Parses filename from given url
        """
        if url.find('/'):
            return url.rsplit('/', 1)[1]

    # Filepaths
    outdir = r"data"

    # File locations
    url_list = ["https://github.com/Automating-GIS-processes/CSC18/raw/master/data/Helsinki_masked_p188r018_7t20020529_z34__LV-FIN.tif"]

    # Create folder if it does no exist
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # Download files
    for url in url_list:
        # Parse filename
        fname = get_filename(url)
        outfp = os.path.join(outdir, fname)
        # Download the file if it does not exist already
        if not os.path.exists(outfp):
            print("Downloading", fname)
            r = urllib.request.urlretrieve(url, outfp)