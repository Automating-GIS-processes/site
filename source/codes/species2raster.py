##Rasterize Species Range Maps=name
##Conservation Geography=group
##Species_Range_Polygons=vector polygon
##Species_Attribute=field Species_Range_Polygons
##Presence_Field_Name=string presence
##Presence_Field_Value=expression 1
##Output_Directory=folder /tmp/


import os.path


algorithmOutput = processing.run(
    "qgis:fieldcalculator",
    {
        "INPUT": Species_Range_Polygons,
        "FIELD_NAME": Presence_Field_Name,
        "FIELD_TYPE": 1,
        "FIELD_LENGTH": 5,
        "FIELD_PRECISION": 0,
        "NEW_FIELD": True,
        "FORMULA": Presence_Field_Value,
        "OUTPUT": "memory:speciesRangePolygonsWithPresenceValue"
    }
)
speciesRangePolygonsWithPresenceValue = algorithmOutput["OUTPUT"]

# get the field index for the column "Species_Attribute"
fields = speciesRangePolygonsWithPresenceValue.fields()
fieldIndex = fields.indexFromName(Species_Attribute)

# get unique values for this columns
uniqueSpecies = Species_Range_Polygons.uniqueValues(fieldIndex)

# loop over unique species
for species in uniqueSpecies:

    # define output file name:
    outputFile = os.path.join(
        Output_Directory,
        species.replace(" ","_")    
    )

    # select only feature with the current species
    algorithmOutput = processing.run(
        "qgis:selectbyattribute",
        {
            "INPUT": speciesRangePolygonsWithPresenceValue,
            "FIELD": Species_Attribute,
            "OPERATOR": 0,
            "VALUE": species
        }
    )
    oneSpeciesRangePolygons = algorithmOutput["OUTPUT"]
    
    # save intermediate vector file
    algorithmOutput = processing.run(
        "native:saveselectedfeatures",
        {
            "INPUT": oneSpeciesRangePolygons,
            "OUTPUT": outputFile + ".shp"
        }
    )
    oneSpeciesRangePolygons = algorithmOutput["OUTPUT"]

    # rasterise the vector layer
    algorithmOutput = processing.run(
        "gdal:rasterize",
        {
            "INPUT": oneSpeciesRangePolygons,
            "FIELD": Presence_Field_Name,
            "DIMENSIONS": 0,
            "WIDTH": 2000,
            "HEIGHT": 1000,
            "RAST_EXT": "",
            "RTYPE": 0,
            "OUTPUT": outputFile + ".tif"
        }
    )
