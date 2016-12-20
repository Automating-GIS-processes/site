# Import arcpy module so we can use ArcGIS geoprocessing tools
import arcpy

# Enable Arcpy to overwrite existing files
arcpy.env.overwriteOutput = True

#---------------------------------------------------------------------------------------------
# 1. Get parameters from the toolbox using 'GetParametersAsText' method
#   --> check ArcGIS help for info how to use methods
#   Method info: http://resources.arcgis.com/en/help/main/10.2/index.html#//018v00000047000000
#---------------------------------------------------------------------------------------------

input_shp = arcpy.GetParameterAsText(0)
output_raster = arcpy.GetParameterAsText(1)
value_attribute = arcpy.GetParameterAsText(2)

#--------------------------------------------------------------------------------------------
# 2. Convert input Shapefile into a Raster Dataset using 'PolygonToRaster_conversion' method
# Method info: http://resources.arcgis.com/en/help/main/10.2/index.html#//001200000030000000
#--------------------------------------------------------------------------------------------

arcpy.PolygonToRaster_conversion(in_features=input_shp, value_field=value_attribute, out_rasterdataset=output_raster)
