Processing toolbox scripts
==========================

Managing and organising complex composite algorithms in the *Graphical Modeler* is not only tedious, it also only offers very limited logic operations. For more flexible and more advanced algorithms, the *processing toolbox* allows to implement python scripts. A python script integrated into the processing toolbox can access all of *processing*’s algorithms and its user interface, the entire python *application programming interface* (API) of QGIS (see. the `PyQGIS Developer Cookbook <http://docs.qgis.org/2.18/en/docs/pyqgis_developer_cookbook/intro.html>`_), and any other python module installed in the same python environment QGIS is running it.

.. note:: Python and its ecosystem are highly modular. It is not uncommon to find multiple python installations on a single computer. Many applications require specific versions of python and/or some of its modules. For developers of python-dependent software, it has become common to supply a ``requirements.txt`` file which can be used to initialise a so-called *virtual environment*, using tools such as `(ana)conda <https://conda.io/>`_. 
        On Microsoft Windows, unfortunately most programs ship with their private python enviroment which is difficult to access outside of the respective program and even harder to install additional packages into. For instance, ESRI ArcGIS and QGIS use entirely separate python installations. On Linux and macOS, QGIS typically uses the system python environment, but QGIS’ own packages are per-default only accessible from within the program.

To add a new python script to the processing toolbox, choose *Scripts → Tools → Create new script* from the toolbox. It is advisable to try the script in the interactive **IPyConsole** first, though. 

*Processing* in the IPython console
-----------------------------------

.. note:: In this course, we use the soon-to-be-released next major QGIS version, 3.0. There have been major changes in QGIS, one of them being a complete rewrite of the *processing API*. At the time of this writing, documentation is still incomplete.

Import the ``processing`` module to use its algorithms:

.. code:: python
    import processing

Previous to QGIS 2.99, *processing* offered a ``processing.alglist()`` command to list all available algorithms and search for keywords in their names. In QGIS 3.0, the following two lines are an easy drop-in for the same search:

.. code:: python
    # search for “buffer” algorithms:
    In [1]: searchTerm = "buffer"
    In [2]: print([a.id() for a in QgsApplication.processingRegistry().algorithms() if searchTerm in a.id()])
    Out[2]: 
        ['gdal:buffervectors',
         'gdal:onesidebuffer',
         'grass7:r.buffer',
         'grass7:r.buffer.lowmem',
         'grass7:v.buffer.column',
         'grass7:v.buffer.distance',
         'native:buffer',
         'qgis:fixeddistancebuffer',
         'qgis:singlesidedbuffer',
         'qgis:variabledistancebuffer']


 .. note:: This code uses a very *pythonic* programming language feature: *list comprehensions*. A *list* is a variable containing zero, one or more values, in the order they were added to the list. To define a list, put its member values (if any) inside brackets, comma-separated: ``["a", "list", "of", "strings"]``. In the above example, the list is filled with values created on-the-fly in a *for-loop* within these brackets. (*List comprehension* is an advanced language feature, and copy-&-paste is fine for the purpose of this course)

To access more information on an individual algorithm, run ``processing.algorithmHelp()``:

.. code:: python
    In [3]: processing.algorithmHelp("native:buffer")
    Out[3]: 
        Buffer (native:buffer)
        
        This algorithm computes a buffer area for all the features in an input layer, using a fixed or dynamic distance.
        
        The segments parameter controls the number of line segments to use to approximate a quarter circle when creating rounded offsets.
        
        The end cap style parameter controls how line endings are handled in the buffer.
        
        The join style parameter specifies whether round, miter or beveled joins should be used when offsetting corners in a line.
        
        The miter limit parameter is only applicable for miter join styles, and controls the maximum distance from the offset curve to use when creating a mitered join.
        
        ----------------
        Input parameters
        ----------------
        
        INPUT:  <QgsProcessingParameterFeatureSource>
                Input layer
        
        DISTANCE:  <QgsProcessingParameterNumber>
                Distance
        
        SEGMENTS:  <QgsProcessingParameterNumber>
                Segments
        
        END_CAP_STYLE:  <QgsProcessingParameterEnum>
                End cap style
                        0 - Round
                        1 - Flat
                        2 - Square
        
        JOIN_STYLE:  <QgsProcessingParameterEnum>
                Join style
                        0 - Round
                        1 - Miter
                        2 - Bevel
        
        MITER_LIMIT:  <QgsProcessingParameterNumber>
                Miter limit
        
        DISSOLVE:  <QgsProcessingParameterBoolean>
                Dissolve result
        
        OUTPUT:  <QgsProcessingParameterFeatureSink>
                Buffered
        
        ----------------
        Outputs
        ----------------
        
        OUTPUT:  <QgsProcessingOutputVectorLayer>
                Buffered


