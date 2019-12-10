Additional PyQGIS functions
---------------------------

Below are two functions you can use for challenge, inspiration, or fun
when further diving into PyQGIS. Simply copy the code to QGIS’s code
editor and you’re good to go. Both of the functions have additional
coding challenges below them.

Buffer Party
~~~~~~~~~~~~

This function takes the currently active QgsVectorLayer and creates
buffers of random size around each individual feature. The user can
define the min and max size of the buffers when calling the function.

.. code:: python

    import random
    
    def bufferParty(min_length=1, max_length=100):
        """This function takes the currently active (vector) layer, loops through its
            features and for each geometry creates a buffer of random size. The size
            falls within the parameters given. A new vector layer is created from these
            and added to the current project."""
        original_layer = iface.activeLayer()
        buffered_feat_list = []
        
        # looping through features of the active layer
        for id, feat in enumerate(original_layer.getFeatures()):
            # original geometry
            geometry = feat.geometry()
            
            # random integer within the defined values
            buffer_radius = random.randint(min_length, max_length)
            
            # create the buffered geometry. The other integer is the number
            # of segments
            buffer = geometry.buffer(buffer_radius, 16)
            
            # creating a new feature that shares the same id number but new geometry
            feat = QgsFeature(id)
            feat.setGeometry(buffer)
            
            # adding all the features to a list
            buffered_feat_list.append(feat)
        
        # making sure the CRS is the same in both layers
        layer_crs = original_layer.sourceCrs().toWkt()
        
        # creating the new vector layer as a temporary (memory) layer
        buff_layer = QgsVectorLayer('Polygon?crs='+layer_crs, "Buffered "+ original_layer.sourceName(), "memory")
        
        # adding all the features to it
        buff_layer.dataProvider().addFeatures(buffered_feat_list)
        
        #check the layer is valid
        if buff_layer.isValid():
            # inserting the new layer to the project
            QgsProject.instance().addMapLayer(buff_layer)
        else:
            print("faulty layer")
    
    # call the function
    bufferParty(min_length=10, max_length=1000)


.. admonition:: Tasks

    -  Can you think of a way to check that the current layer is indeed a
       vector layer and not raster or empty?

    -  Can you think of a way keep the original attributes in the new layer
       as well? Check out the documentation for the relevant classes,
       e.g. \ `QgsFeature <https://qgis.org/pyqgis/3.2/core/Feature/QgsFeature.html>`__.

Polygon drawing window
~~~~~~~~~~~~~~~~~~~~~~

This neat function throws a new window in which the user may freely draw
by clicking on the canvas. When user closes the window, the map points
are printed in console. Consists of two classes with multiple methods:
the window itself and the polygon drawing tool.

.. code:: python

    class drawWindow(QMainWindow):
        def __init__(self):
            """Initializing the necessary resources."""
            QMainWindow.__init__(self)
            
            # creating map canvas, which draws the maplayers
            # setting up features like canvas color
            self.canvas = QgsMapCanvas()
            self.canvas.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            self.canvas.setCanvasColor(Qt.white)
            self.canvas.enableAntiAliasing(True)
            
            # Qmainwindow requires a central widget. Canvas is placed
            self.setCentralWidget(self.canvas)
            
            # creating each desired action
            self.actionPan = QAction("Pan tool", self)
            self.actionDraw = QAction("Polygon tool", self)
            self.actionConnect = QAction("Connect polygon", self)
            self.actionClear = QAction("Clear", self)
            self.actionClose = QAction("Close", self)
            
            # these two function as on/off. the rest are clickable
            self.actionPan.setCheckable(True)
            self.actionDraw.setCheckable(True)
            
            # when actions are clicked, do corresponding function
            self.actionPan.triggered.connect(self.pan)
            self.actionDraw.triggered.connect(self.draw)
            self.actionClear.triggered.connect(self.clear)
            self.actionConnect.triggered.connect(self.connect)
            self.actionClose.triggered.connect(self.close)
            
            # toolbar at the top of the screen: houses actions as buttons
    
            self.toolbar = self.addToolBar("Canvas actions")
            # ensure user can't close the toolbar
            self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
            self.toolbar.setMovable(False)
            # change order here to change their placement on toolbar
            self.toolbar.addAction(self.actionPan)
            self.toolbar.addAction(self.actionDraw)
            self.toolbar.addAction(self.actionConnect)
            self.toolbar.addAction(self.actionClear)
            self.toolbar.addAction(self.actionClose)
            
            # link action to premade map tool
            self.toolPan = QgsMapToolPan(self.canvas)
            self.toolPan.setAction(self.actionPan)
            # And the draw tool created below
            self.toolDraw = PolygonMapTool(self.canvas)
            self.toolDraw.setAction(self.actionDraw)
    
            # set draw tool by default
            self.draw()
            
        def pan(self):
            """Simply activates pan tool"""
            self.canvas.setMapTool(self.toolPan)
            # make sure the other button isn't checked to avoid confusion
            self.actionDraw.setChecked(False)
            
        def draw(self):
            """Activates draw tool"""
            self.canvas.setMapTool(self.toolDraw)
            self.actionPan.setChecked(False)
            
        def clear(self):
            self.toolDraw.reset()
        
        def connect(self):
            """Calls the polygon tool to connect an unconnected polygon"""
            self.toolDraw.finishPolygon()
        
        def showWindow(self):
            """Shows the map canvas: currently the canvas is empty,
           but a reference layer can be added to it """
           
            """
            Add code here if you want to add a layer to the window
            self.canvas.setExtent(self.layer.extent())
            self.canvas.setLayers([self.layer])
            """
            self.show()
            
        def closeEvent(self, event):
            """Activated anytime Mapwindow is closed either programmatically or
                if the user finds some other way to close the window. Automatically
                finishes the polygon if it's unconnected.
            """
            self.toolDraw.finishPolygon()
            points = self.getPolygon()
            if points:
                for point in points:
                    print(point)
            QMainWindow.closeEvent(self, event)
            
        def getPolygon(self):
            return self.toolDraw.getPoints()
        
        def getPolygonBbox(self):
            return self.toolDraw.getPolyBbox()
            
    class PolygonMapTool(QgsMapToolEmitPoint):
        """This class holds a map tool to create a polygon from points got by clicking
            on the map window. Points are stored in a list of point geometries, which is when finishing the polygon"""
        def __init__(self, canvas):
            self.canvas = canvas
            QgsMapToolEmitPoint.__init__(self, self.canvas)
            # rubberband class gives the user visual feedback of the drawing
            self.rubberBand = QgsRubberBand(self.canvas, True)
            
            # setting up outline and fill color: both red
            self.rubberBand.setColor(QColor(235,36,21))
            # RGB color values, last value indicates transparency (0-255)
            self.rubberBand.setFillColor(QColor(255,79,66,140))
            self.rubberBand.setWidth(3)
            
            self.points = []
            # a flag indicating when a single polygon is finished
            self.finished = False
            self.poly_bbox = False
            self.double_click_flag = False
            self.reset()
          
        def reset(self):
            """Empties the canvas and the points gathered thus far"""
            self.rubberBand.reset(True)
            self.poly_bbox = False
            self.points.clear()
    
        def keyPressEvent(self, e):
            """Pressing ESC resets the canvas. Pressing enter connects the polygon"""
            if (e.key() == 16777216):
                self.reset()
            if (e.key() == 16777220):
                self.finishPolygon()
                
        def canvasDoubleClickEvent(self, e):
            """Finishes the polygon on double click"""
            self.double_click_flag = True
            self.finishPolygon()
    
        def canvasReleaseEvent(self, e):
            """Activated when user clicks on the canvas. Gets coordinates, draws
            them on the map and adds to the list of points."""
            if self.double_click_flag:
                self.double_click_flag = False
                return
            
            # if the finished flag is activated, the canvas will be reset
            # for a new polygon
            if self.finished:
                self.reset()
                self.finished = False
            
            self.click_point = self.toMapCoordinates(e.pos())
            
            self.rubberBand.addPoint(self.click_point, True)
            self.points.append(self.click_point)
            self.rubberBand.show()
    
            
        def finishPolygon(self):
            """Activated by user or when the map window is closed without connecting
                the polygon. Makes the polygon valid by making first and last point
                the same. This is reflected visually. Up until now the user has been
                drawing a line: a polygon is created and shown on the map."""
            # nothing will happen if the code below has already been ran
            if self.finished:
                return
            # connecting the polygon is valid if there's already at least 3 points
            elif len(self.points)>2:
                first_point = self.points[0]
                self.points.append(first_point)
                self.rubberBand.closePoints()
                self.rubberBand.addPoint(first_point, True)
                self.finished = True
                # a polygon is created and added to the map for visual purposes
                map_polygon = QgsGeometry.fromPolygonXY([self.points])
                self.rubberBand.setToGeometry(map_polygon)
                # get the bounding box of this new polygon
                self.poly_bbox = self.rubberBand.asGeometry().boundingBox()
            else:
                self.finished = True
                
        def getPoints(self):
            """Returns list of PointXY geometries, i.e. the polygon in list form"""
            self.rubberBand.reset(True)
            return self.points
            
    myDrawWindow = drawWindow()
    myDrawWindow.showWindow()


.. admonition:: Tasks

    -  The polygon is drawn in an eye catching red. Find where the color is
       defined, figure out how it works and change it to something else

    -  Check out method showWindow in class drawWindow. There’s some code
       for adding a layer to the canvas. Find out how to add the active
       layer to the map canvas to use for drawing reference.
