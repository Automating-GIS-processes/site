# Import arcpy module so we can use ArcGIS geoprocessing tools
import arcpy
import sys, os

##input_species_shp = arcpy.GetParameterAsText(0)
##output_folder = arcpy.GetParameterAsText(1)
##species_attribute = arcpy.GetParameterAsText(2)
##attribute_name = arcpy.GetParameterAsText(3)
##presence_value = arcpy.GetParameterAsText(4)

input_species_shp = r"C:\HY-Data\HENTENKA\KOODIT\Opetus\Automating-GIS-processes\AutoGIS-Sphinx\data\DAMSELFISH_distributions.shp"
output_folder = r"C:\HY-Data\HENTENKA\KOODIT\Opetus\Automating-GIS-processes\test"
species_attribute = "binomial"
attribute_name = "testCol"
presence_value = 1


# 2. Add a new field into the table using 'AddField_management' method
arcpy.AddField_management(in_table=input_species_shp, field_name=attribute_name, field_type="SHORT")

# 3. Update the presence value for our newly created attribute with 'CalculateField_management' method
arcpy.CalculateField_management(in_table=input_species_shp, field=attribute_name, expression=presence_value)

# 4. Get a list of unique species in the table using 'SearchCursor' method

# 4.1 CREATE a function that returns unique values of a 'field' within the 'table'
def unique_values(table, field):

    # Create a cursor object for reading the table
    cursor = arcpy.da.SearchCursor(table, [field]) # A cursor iterates over rows in table

    # Create an empty list for unique values
    unique_values = []

    # Iterate over rows and append value into the list if it does not exist already
    for row in cursor:
        if not row[0] in unique_values: # Append only if value does not exist
            unique_values.append(row[0])
    return sorted(unique_values) # Return a sorted list of unique values

# 4.2 USE the function to get a list of unique values
unique_species = unique_values(table=input_species_shp, field=species_attribute)


# 5. Create a feature layer from the shapefile with 'MakeFeatureLayer_management' method that enables us to select specific rows
species_lyr = arcpy.MakeFeatureLayer_management(in_features=input_species_shp, out_layer="species_lyr")


# 6. Iterate over unique_species list and:
#   6.1) export individual species as Shapefiles and
#   6.2) convert those shapefiles into Raster Datasets

for individual in unique_species:
    print(individual)
    # 6.1):
    # Create an expression for selection using Python String manipulation
    expression = "%s = '%s'" % (species_attribute, individual)

    # Select rows based on individual breed using 'SelectLayerByAttribute_management' method
    arcpy.SelectLayerByAttribute_management(species_lyr, "NEW_SELECTION", where_clause=expression)

    # Create an output path for Shapefile
    shape_name = individual + ".shp"
    individual_shp = os.path.join(output_folder, shape_name)

    # Export the selection as a Shapefile into the output folder using 'CopyFeatures_management' method
    arcpy.CopyFeatures_management(in_features=species_lyr, out_feature_class=individual_shp)

    # 6.2):
    # Create an output path for the Raster Dataset (*.tif)
    tif_name = individual + ".tif"
    individual_tif = os.path.join(output_folder, tif_name)

    # Convert the newly created Shapefile into a Raster Dataset using 'PolygonToRaster_conversion' method
    arcpy.PolygonToRaster_conversion(in_features=individual_shp, value_field=attribute_name, out_rasterdataset=individual_tif)

    # Print progress info for the user
    info = "Processed: " + individual
    arcpy.AddMessage(info)

# 7. Print that the process was finished successfully
info = "Process was a great success! Wuhuu!"
arcpy.AddMessage(info)
