Python in QGIS
==============

The core application and libraries of QGIS are programmed in C++. Nevertheless, Python plays an important role in its ecosystem:
Most of the pre-installed plugins and even some of the data provider modules are written in Python,
and virtually all functions of the interface and the libraries are exported to a Python API (*Application Programming Interface*).
It takes only moderate effort to author extensions to QGIS which integrate seamlessly into its user interface,
create stand-alone applications using components of QGIS, such as a map window or a data backend,
or run custom scripts within QGIS. T
o really dive into it, see the `PyQGIS Developer Cookbook <http://docs.qgis.org/3.4/en/docs/pyqgis_developer_cookbook/intro.html>`_
which walks you from easy *Hello World* examples to writing your own applications.

Here, we will introduce some wery basic ways of using Python programming in QGIS. As inspiration, we have used the
excellent `tutorial by Anita Graser <https://anitagraser.com/pyqgis-101-introduction-to-qgis-python-programming-for-non-programmers/>`__.

Using a Python console
----------------------

There is (at least) two different Python consoles available within QGIS:

1. Access the **built-in Python console** from the menu *Plugins → Python Console*. It offers basic functionality, and allows to load and save scripts from and to files.

   .. figure:: img/L7-02-pyqgis-00-builtin-python-console.png

2. The more advanced **iPython console** has to be installed as a Plugin before first use:
   - Go to *Plugins → Manage and Install Plugins*, 
   - Select to search in *All* plugins, and type `ipython` into the search field.
   - Select the **IPyConsole** plugin, and click *Install plugin*

.. figure:: img/L7-02-pyqgis-01-install-ipyconsole.png

.. note:: IPython or Jupyter have to be installed on your computer, see the plugin description for instructions on how to install these requirements. On MS Windows operating systems, installing these modules unfortunately is not straightforward. `This blog post <https://www.lutraconsulting.co.uk/blog/2016/03/02/installing-third-party-python-modules-in-qgis-windows/>`_ has step-by-step instructions (replace ``lxml`` with ``qtconsole`` and ``jupyter==1.0.0``)

The console is now available from the menu *Plugins → IPython QGIS Console → Windowed*

.. figure:: img/L7-02-pyqgis-02-ipyconsole.png



.. admonition:: Note

    In the following steps, we are using the municipalities of Finland from the Statistics Finland
    web feature service: http://geo.stat.fi/geoserver/tilastointialueet/wfs ("Kunnat 2019").
    You can also use any other vector layer as `layer`.


.. figure:: img/add_wfs_layer.png


If you have not installed the IPyConsole, you can also repeat the following steps in the stardard Python Console in QGIS.

By default an ``iface`` object is imported, which allows the access to the currently active QGIS instance’s user interface.
For example, we can easily load a new layer to QGIS, or start interacting with an existing layer in the session:

- Add a vector layer from a web feature service to the QGIS interface, and store it also in a variable called `layer`:

.. code:: python

    # Define source (vector layer)
    source = "http://geo.stat.fi/geoserver/tilastointialueet/wfs?request=GetFeature&typename=tilastointialueet:kunta1000k_2019"

    # Add layer from the source ti the QGIS session:
    layer = iface.addVectorLayer(url, "admin_areas", "ogr")


- In case you already have some layers open in the interface, can start working with one of them:

.. code:: python

    # Get active layer:
    layer = iface.activeLayer()

- Check basic properties of the layer:

.. code:: python

    # Print layer name
    print(layer.name())

    # Number of features
    print(layer.featureCount())

Next, you can ask python to, for example, open the attribute table of that layer:

.. code:: python

    # Open attribute table in a new window
    iface.showAttributeTable(layer)


.. figure:: img/municipalities_attributes.png

We can also view all the attributes in the console:

.. code:: python

    # Print column names
    for field in layer.fields():
        print(field.name()))


You can access a help text on objects using ``help()``:

.. code:: python

    In [1]: help(layer)
    Out[1]: Help on QgsVectorLayer in module qgis._core object:
            
            class QgsVectorLayer(QgsMapLayer, QgsExpressionContextGenerator, QgsFeatureSink, QgsFeatureSource)
             |  Represents a vector layer which manages a vector based data sets.
             |  
             |   The QgsVectorLayer is instantiated by specifying the name of a data provider,
             |   such as postgres or wfs, and url defining the specific data set to connect to.
             |   The vector layer constructor in turn instantiates a QgsVectorDataProvider subclass
             |   corresponding to the provider type, and passes it the url. The data provider
             |   connects to the data source.
             |  
             |   The QgsVectorLayer provides a common interface to the different data types. It also
             |   manages editing transactions.
             |  
             |    Sample usage of the QgsVectorLayer class:
             |  
             |   \code
             |       QString uri = "point?crs=epsg:4326&field=id:integer";
             |       QgsVectorLayer *scratchLayer = new QgsVectorLayer(uri, "Scratch point layer",  "memory");
             |   \endcode
             |  
             |   The main data providers supported by QGIS are listed below.
             |  
             |   \section providers Vector data providers
             |  
             |   \subsection memory Memory data providerType (memory)
             |  
             |   The memory data provider is used to construct in memory data, for example scratch
             |   data or data generated from spatial operations such as contouring. There is no
             |   inherent persistent storage of the data. The data source uri is constructed. The
             |   url specifies the geometry type ("point", "linestring", "polygon",
             |   "multipoint","multilinestring","multipolygon"), optionally followed by url parameters
             |   as follows:
                 …
                 …

This help text is the same information listed in QGIS’ API documentation at `qgis.org/pyqgis <https://qgis.org/pyqgis/3.4/>`_.
