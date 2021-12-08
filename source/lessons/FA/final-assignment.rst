Final assignment
================

.. image:: https://img.shields.io/badge/launch-CSC%20notebook-blue.svg
   :target: https://notebooks.csc.fi/#/blueprint/d189695c52ad4c0d89ef72572e81b16c

.. admonition:: Start your assignment

    Start your final assignment by accepting the `GitHub Classroom <https://classroom.github.com/a/CnsJqTEr>`_ for the final work.

.. admonition:: Final Assignment

    .. raw:: html

        <iframe title='Final Assignment' width='720' height='405' src='https://www.youtube.com/embed/QmZ0zgbpndM' frameborder='0' allowfullscreen allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture'></iframe><p>Håvard Wallin Aagesen, University of Helsinki <a href='https://www.youtube.com/c/AutomatingGISprocesses'>@ AutoGIS channel on Youtube</a>.</p>

.. admonition:: Summary

    `Summary of the Final Assignment instructions (PDF) <https://autogis-site.readthedocs.io/en/latest/_static/autogis-final-assignment-2021.pdf>`_

.. admonition:: Presentation

    .. raw:: html

        <embed title='Presentation' style='display:flex; width:100%;height:30em;' src='https://haavardaagesen.github.io/autogis-presentations/final_assignment_2021.html'>

Aim of the work
---------------

The final project is an individual task where the aim is to apply Python programming to automating a GIS analysis process.
**The main aim is to create a GIS analysis workflow that can be easily repeated for similar input data.**

You can select a pre-defined topic, or develop your own question. You should take advantage of your programming skills
(basics of Python, defining your own functions, reading and writing data, data analysis usign pandas, spatial analysis using geopandas,
creating static and/or interactive data visualizations, ...), version control skills (git + GitHub),
and good coding practices (writing readable code) when doing the final assignment.

Final work topic
~~~~~~~~~~~~~~~~~~~

You have three options for the final project that you can choose from:

#. AccessViz_ - a GIS-tool that can visualize and compare travel times by different travel modes in Helsinki Region.
#. UrbanIndicators_ - a workflow that calculates and reports different urban indicators for an urban region, and allows the comparison of different urban areas based on these indicators.
#. Your-own-project_ - your own tool or analysis process (for example, related to your thesis!). Suggest your idea before the last practical exercise!

Think about the final project as a challenge for yourself to show and implement the programming skills that you have learned this far. You have learned a lot already!

Final work structure
~~~~~~~~~~~~~~~~~~~~~~~~

Here is the suggested structure of the work, that also serves as the basis for grading:

1. **Data acquisition** (Fetching data, subsetting data, storing intermediate outputs etc.)
2. **Data analysis** (Enriching and analyzing the data, eg. spatial join, overlay, buffering, other calculations..)
3. **Visualization** (Visualizing main results and other relevant information as maps and graphs)

You can write your code into python script files and /or jupyter notebook files. You can freely organize your final work into one single file, or several files (for example, write your own functions into a separate `.py` file and apply them in one or several jupyter notebook `.ipynb` files.

**The workflow should be repeatable and well documented.** In other words, anyone who gets a copy of your repository should be able to run your code, and read your code. 

What should be returned?
~~~~~~~~~~~~~~~~~~~~~~~~

Organize all your code(s) / notebook(s) into your personal Final-Assignment repository (GitHub classroom link at the top of this page)
and **add links to all relevant files to the README.md file**. Anyone who downloads the repository should be able to **read your code** and documentation and understand what is going on, and **run your code** in order to reproduce the same results :)

*Note: If your code requires some python packages not found in the csc notebooks environment, please mention them also in the README.md file and provide installation instrutions.*

When is the deadline?
~~~~~~~~~~~~~~~~~~~~~

Label your submissions as "submitted" in the exercise repository's `README.md` under "status" once you are finished with the Final assignment.

You can choose from these two deadlines:
- 1st deadline: Thursday the 31st December 2021
- 2nd deadline Friday the 16th of January 2022

Submissions are checked after each deadline (you can get the feedback earlier if aiming for the first deadline).
If you need the course grade earlier, please contact the course instructor.


Grading
~~~~~~~
The grading is based on a typical 0-5 scale. See detailed grading criteria :doc:`here <final-assignment-grading>`.
The final assignment is graded based on:

- Main analysis steps (data fetching, data analysis, visualization)
- Repeatability (it should be possible to repeat the main analysis steps for different input files / input parameters)
- Quality of visualizations (maps and graphs)
- Overall documentation of the work (use markdown cells for structuring the work, and code comments to explain details)

**Good documentation of the code and your project is highly appreciated!!!**
You should add necessary details to the `README.md` file, and use inline comments and Markdown cells to document your work along the way. Take a look of these hints for using markdown:

- `General Markdown syntax guide <https://guides.github.com/features/mastering-markdown/>`__.

.. _AccessViz:

AccessViz
---------

General Description
~~~~~~~~~~~~~~~~~~~~~~~~

**AccessViz** is a set of tools that can be used for managing and helping to analyze the
**Helsinki Region Travel Time Matrix** data set. The data can be downloaded from
`here <http://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix/>`_. The travel time matrix is available from three different years (2013 / 2015 / 2018).
You can develop the tool by using data from one year. Optionally, your tool could compare travel times from different years!

The travel time matrix contsists of 13231 text files. Each file contains travel time and travel distance information by different modes of transport (walking, biking, public transport and car) from all other grid squares to one target grid square.
The files are named and organized based on their ID number in th YKR ID data set. For example, the Travel Time Matrix file for the railway station is named `travel_times_to_5975375.txt`, and this
file is located in folder `5975xxx`. All possible YKR ID values can be found from the attribute table of a Shapefile called MetropAccess_YKR_grid.shp that you can download from `here <https://zenodo.org/record/3247564/files/MetropAccess_YKR_grid.zip?download=1>`_.
Read further description about the travel time matrix from the `Digital Geography Lab / Accessibility research group blog <http://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix/>`__.

What should this tool do?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AccessViz is a Python tool (i.e. a set of Notebooks and/or Python script files) for managing, analyzing and visualizing the Travel Time Matrix data set. AccessViz consist of Python functions, and examples on how to use these functions.
AccessViz has four main components for accessing the files, joining the attribute information to spatial data, visualizing the data and comparing different travel modes:

**1. FileFinder:** The AccessViz tool finds a list of travel time matrix files based on a list of YKR ID values from a specified input data folder. The code should work for different list lengths and different YKR ID values.
If the YKR ID number does not exist in the input folder (and it's subfolders), the tools should warn about this to the user but still continue running.
The tool should also inform the user about the execution process: tell the user what file is currently under process and how many files there are left
(e.g. `"Processing file travel_times_to_5797076.txt.. Progress: 3/25"`). As output, FileFinder compiles a list of FilePaths for further processing. (Optional feature: FileFinder can also print out a list of filepaths into a text file.)

**2. TableJoiner:** The AccessViz tool creates a spatial layer from the chosen Matrix text table (e.g. *travel_times_to_5797076.txt*) by joining the Matrix file with
MetropAccess_YKR_grid Shapefile where ``from_id`` in Matrix file corresponds to ``YKR_ID`` in the Shapefile. The tool saves the result in the output-folder
that user has defined. Output file format can be Shapefile or Geopackage. You should name the files in a way that it is possible to identify the ID from the name (e.g. 5797076).
The table joiing can be applied to files that correspond to a list of selected YKR ID files (FileFinder handles finding the correct input files!).

**3. Visualizer:** AccessViz can visualize the travel times of selected YKR_IDs based on different travel modes (it should be possible to use the same tool for visualizing travel times by car, public transport, walking or biking depending on an input parameter!).
It saves the maps into a specified folder for output images. The output maps can be either **static** or **interactive** - it should be possible to select which kind of map output is generated when running the tool. You can freely design yourself the style of the map, colors, travel time intervals (classes) etc.
Try to make the map as informative as possible! The visualizations can be applied to files that correspond to a list of selected YKR ID files (FileFinder handles finding the correct input files!). Remember to handle no data values.

**4. Comparison tool:** AccessViz can also compare **travel times** or **travel distances** between two different travel modes. For example, the tool can compare rush hour travel times by public transport and car based on columns `pt_r_t` and `car_r_t`, and rush hour travel distances based on columns `pt_r_d` and `car_r_d`.
It should be also possible to run the AccessViz tool without doing any comparisons. Thus IF the user has specified two travel modes (passed in as a list) for the AccessViz, the tool will calculate the time/distance difference of those travel modes
into a new column. In the calculation, the first travel mode is always subtracted by the last one: ``travelmode1 - travelmode2`` according to the order in which the travel modes were listed.
The tool should ensure that distances are not compared to travel times and vice versa. The tool saves outputs as new files (Shapefile or Geopackage file format) with an informative name, for example: ``Accessibility_5797076_pt_vs_car.shp``.
It should be possible to compare only two travel modes between each other at the time. Accepted travel modes are the same ones that are found in the actual TravelTimeMatrix file (walking, biking, public transport and car).
If the tool gets invalid parameters (for example, a travel mode that does not exists, or too many travel modes), stop the program, and give advice what are the acceptable values. Remember to handle no data values.

**If you are pursuing the highest grade, you should implement also at least one of the following components**:

5. The  AccessViz documentation also contains a separate interactive map that shows the YKR grid values in Helsinki region. The purpose of the map is to help the user to choose the YKR-IDs that they are interested to visualize / analyze.

6. AccessViz can also visualize the travel mode comparisons that were described in step 4.

7. AccessViz can also visualize shortest path routes (walking, cycling, and/or driving) using OpenStreetMap data from Helsinki Region. The impedance value for the routes can be distance (as was shown in Lesson 7) or time.

8. AccessViz can also compare travel time data from two different years. For example, this tool could plot a map that shows the difference with public transport travel times between 2013 and 2018.

.. note::

    **NoData values**

    Notice that there are NoData values present in the data (value -1). In such cases the result cell should always end up having a value -1 when doing travel mode comparisons. In the visualizations, the NoData values should be removed before visualizing the map.

.. hint::

    **Modularize your code**

    One of the best practice guidelines is that you should avoid repeating yourself. Thus, we recommend to modularize different tasks in your code and use functions as much as possible. Use meaningful parameter and variable names when defining the functions, so that they are intuitive but short.

.. _UrbanIndicators:

Urban indicators
----------------

In this assignment, the aim is to **develop an urban analytics tool** and apply it to at least two cities or neighborhoods (e.g. Helsinki and Tampere, or neighborhood areas in Helsinki).
The main idea is to calculate a set of metrics / indicators based on the urban form and/or population, and to compare the cities/regions based on these measures.
This assignment is not accurately defined, as the idea is to allow you to use your own imagination and interest to explore different datasets and conduct analyses that interest to you,
still providing useful insights about the urban areas using specific set of indicators (you should use 2-4 different indicators, see examples from below).

Data
~~~~

You can use any (spatial) data that you can find, and generate your own report describing how the cities differ from each other based on different perspectives (see below hints about possible analyses).
You can use any data that is available, for example, from the following sources:

  - `OpenSreetMap <https://www.openstreetmap.org>`__ (e.g., streets, buildings, points of interest) following the approach from lesson 6.)
  - `PaiTuli <https://avaa.tdata.fi/web/paituli/latauspalvelu>`__
  - `Avoindata.fi service <https://www.avoindata.fi/en>`__
  - `Helsinki Region Infoshare <https://hri.fi/en_gb/>`__
  - `Open data service of Tampere <https://data.tampere.fi/en_gb/>`__

Data sources are not limited to these, hence you can also use other data from any source that you can find (remember to document where the data is coming from!).

Example analyses
~~~~~~~~~~~~~~~~

The tool should calculate 2-4 indicators about the urban areas. Here are some examples of potential metrics:

**Population distribution and demographics**

   - Input data management (table joins, data cleaning etc.)
   - Calculate key statistics
   - create maps and graphs

**Urban population growth**

    - Fetch population data from at least two different years
    - Compare statistics from different years
    - Visualize as graphs and maps

**Accessibility**:

    - Decide what travel tiles you are focusing on (walking, driving, public transport..)
    - Decide what types of destinations you are focusing on (transport stations, health care, education, sports facilities..)
    - Get travel time data from the Travel Time Matrix OR calculate shortest paths in a network
    - Calculate travel time / travel distance metrics, or dominance areas
    - Visualize the results as graphs and maps

**Green area index**

    - Fetch green area polygons and filter the data if needed
    - Calculate the percentage of green areas in the city /region + other statistics
    - Visualize the results

**Street network metrics**

    - Fetch street network data
    - Calculate street network metrics (see Lesson 6 and examples from `here <https://github.com/gboeing/osmnx-examples/tree/master/notebooks>`__)
    - Visualize the results

**Building density**

    - Fetch the data, and filter if needed
    - Calculate building density and other metrics
    - create maps showing the building types and density

Structure of the urban indicators tool assignmnent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can design the structure of your assignment freely. We suggest that you create functions in separate script files, and demonstrate the use of those functions in one or several notebooks.
In addition, you should provide some basic information in the README.md file of your final assignment. All in all, the work should include these components:

  - A topic for your work (eg. "Urban indicators: analyzing the street netowrk structure in Helsinki and Tampere").
  - A short introduction to the topic (present 2-4 research questions that you aim to answer using the indicators)
  - Short description of the datasets you used
  - Short generic description of the methods you used
  - Actual codes and visualizations to produce the **results**
  - Short discussion related to the results (what should we understand and see from them?)
  - Short reflection about the analysis, for example:
    - What kind of assumptions, biases or uncertainties are related to the data and/or the analyses that you did?
    - Any other notes that the reader should know about the analysis

Technical considerations
~~~~~~~~~~~~~~~~~~~~~~~~

Take care that you:

 - Document your analyses well using the Markdown cells and describe 1) what you are doing and 2) what you can see from the data and your results.

 - Use informative visualizations

   - Create maps (static or interactive)
   - Create other kind of graphs (e.g. bar graphs, line graphs, scatter plots etc.)
   - Use subplots that allows to easily compare results side-by-side

 - When writing the codes, we highly recommend that you use and write functions for repetitive parts of the code. As a motivation: think that you should repeat your analyses for all cities in Finland, write your codes in a way that this would be possible. Furthermore, we recommend that you save those functions into a separate .py -script file that you import into the Notebook (`see example from Geo-Python Lesson 4 <https://geo-python-site.readthedocs.io/en/latest/notebooks/L4/functions.html#calling-functions-from-a-script-file>`__)

Literature + inspiration
~~~~~~~~~~~~~~~~~~~~~~~~

Following readings provide you some useful background information and inspiration for the analyses (remember to cite if you use them):

 - `European Commission (2015). "Indicators for Sustainable Cities" <http://ec.europa.eu/environment/integration/research/newsalert/pdf/indicators_for_sustainable_cities_IR12_en.pdf>`__

 - `Rob Kitchin, Tracey Lauriault & Gavin McArdle (2015). Knowing and governing cities through urban indicators, city benchmarking and real-time dashboards <https://github.com/Automating-GIS-processes/site/blob/master/literature/Kitchin_et_al_(2015).pdf>`__ . *Regional Studies, Regional Science,* Vol. 2, No. 1, 6–28.

.. _Your-own-project:

Own project work
----------------

Develop your own topic! In general, your own topic should also contain these sections:

1. **Data acquisition** (Fetching data, subsetting data, storing intermediate outputs etc.)
2. **Data analysis** (Enriching and analyzing the data, eg. spatial join, overlay, buffering, other calculations..)
3. **Visualization** (Visualizing main results and other relevant information as maps and graphs)

But feel free to be creative! Your own project might be, for example, related to your thesis or work project.
Remember to describe clearly what you are doing in the final assignment repository README.md -file.
Preferably, present your idea to the course instructors before the winter holidays.


What is at least required from the final project, is that you have:

 - a working piece of code for your task / problem / analyses that solves it

 - Good documentation (i.e. a tutorial) explaining how your tool works OR a report about your analyses and what we can learn from them
