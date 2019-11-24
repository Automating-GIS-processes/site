Final assignment
================

.. image:: https://img.shields.io/badge/launch-CSC%20notebook-blue.svg
   :target: https://notebooks.csc.fi/#/blueprint/8d7886c2f0ac402aa99235f8d289a52b

.. admonition:: Start your assignment

    Start your final assignment by accepting the `GitHub Classroom <https://classroom.github.com/a/t_W3zC8p>`_ for the final work.


Aim of the work
---------------

The final project is an individual task where the aim is to apply Python programming to automating a GIS analysis process.
**The main aim is to create a GIS analysis workflow that can be easily repeated for similar input data.**

You can select a pre-defined topic, or develop your own question. You should take advantage of your programming skills
(basics of python, defining your own functions, reading and writing data, data analysis usign pandas, spatial analysis using geopandas,
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
~~~~~~~~~~~~~~~~~~~

Here is the suggested structure of the work, that also serves as the basis for grading:

1. Data acquisition (Fetching data, subsetting data, storing intermediate outputs etc.)
2. Data analysis (Enriching and analyzing the data, eg. spatial join, overlay, buffering, other calculations..)
3. Visualization (Visualizing main results and other relevant information as maps and graphs)

You can write your code into python script files and /or jupyter notebook files. You can freely organize your final work into one single file, or several files (for example, write your own functions into a separate `.py` file and apply them in one or several jupyter notebook `.ipynb` files.

**The workflow should be repeatable and well documented.** In other words, anyone who gets a copy of your repository should be able to run your code, and read your code. 

What should be returned?
~~~~~~~~~~~~~~~~~~~~~~~~

Organize all your code(s) / notebook(s) into your personal Final-Assignment repository and add links to all relevant files to the README.md file. Anyone who downloads the repository should be able to **read your code** and documentation and understand what is going on, and **run your code** in order to reproduce the same results :)

*Note: If your code requires some python packages not found in the csc notebooks environment, please mention them also in the README.md file and provide installation instrutions.*

When is the deadline?
~~~~~~~~~~~~~~~~~~~~~

Label your submissions as "submitted" in the exercise repository's `README.md` under "status" once you are finished with the Final assignment.
GitHub classroom creates an automatic commit to the repository at the deadline.

**Deadline: January 15th 2020 at 4pm**
- You should commit all changes to GitHub by Wednesday the 15th of January 2020 at 16:00.
- Those who submit by this deadline will get their grades at the end of January.
- If you need your grade earlier, please contact Vuokko via Slack so we can agree on an earlier schedule

**Late submissions:**
- Submitted between Wednesday the 15th of January 2020 at 16:00 and Wednesday the 26th of February 2020 at 16:00
- Will get grades by easter
- Maximum grade 4/5

**Very late submissions:**
- Submitted after Wednesday the 26th of February 2020 at 16:00
- Agree with Vuokko on the schedule :)
- Maximum grade 3/5


Grading
~~~~~~~
The grading is based on a typical 0-5 scale. See detailed grading criteria :doc:`here <final-assignment-grading>`.
The final assignment is graded based on:

- Main analysis steps / functionality
- Repeatability (it should be possible to repeat the main analysis steps for different input files / input parameters)
- Quality of visualizations
- Overall documentation of the work

**Good documentation of the code and your project is highly appreciated!!!**
You should add necessary details to the `README.md`file, and use inline comments and Markdown cells to document your work along the way.
Ttake a look of these hints for using markdown in a useful way:
- `using markdown in Jupyter Notebooks  <http://www.firstpythonnotebook.org/markdown/>`_
- `General Markdown syntax guide <https://guides.github.com/features/mastering-markdown/>`__.

.. _AccessViz:

AccessViz
---------

What the tool should do?
~~~~~~~~~~~~~~~~~~~~~~~~

**AccessViz** is a set of tools that can be used for managing and helping to analyze
Helsinki Region Travel Time Matrix data (2013 / 2015 / 2018) that can be downloaded from
`here <http://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix/>`_.
Read also the description of the dataset from the web-pages so that you get familiar with the data.

AccessViz tool package (i.e. a set of Notebooks) has following main functionalities (i.e. functions) that should work independently. You should demonstrate the usage of the functionalities in your Notebook:

1. AccessViz finds from the data folder all the matrices that user has specified by assigning a list of integer values that should correspond to YKR-IDs found from the attribute table of a Shapefile called `MetropAccess_YKR_grid.shp <http://www.helsinki.fi/science/accessibility/data/MetropAccess-matka-aikamatriisi/MetropAccess_YKR_grid.zip>`_.
If the ID-number that the user has specified does not exist in the data folders, the tools should warn about this to the user but still continue running. The tool should also inform the user about the execution process: tell the user what file is currently under process and how many files there are left
(e.g. "Processing file travel_times_to_5797076.txt.. Progress: 3/25").

2. AccessViz can create Shapefiles from the chosen Matrix text tables (e.g. *travel_times_to_5797076.txt*) by joining the Matrix file with
MetropAccess_YKR_grid Shapefile  where ``from_id`` in Matrix file corresponds to ``YKR_ID`` in the Shapefile. The tool saves the result in the output-folder
that user has defined. You should name the files in a way that it is possible to identify the ID from the name (e.g. 5797076).

3. AccessViz can visualize the travel times of selected YKR_IDs based on the travel mode that the user specifies. It can save those maps into a folder that user specifies. The output maps can be either **static** or **interactive** and user can choose which one with a parameter. You can freely design yourself the style of the map, colors, travel time intervals (classes) etc. Try to make the map as informative as possible!

4. AccessViz can also compare **travel times** or **travel distances** between two different travel modes (more than two travel modes are not allowed). Thus IF the user has specified two travel modes (passed in as a list) for the AccessViz, the tool will calculate the time/distance difference of those travel modes
into a new data column that should be created in the Shapefile. The logic of the calculation is following the order of the items passed on the list where first travel mode is always subtracted by the last one: ``travelmode1 - travelmode2``. The tool should ensure that distances are not compared to travel times and vice versa. If the user chooses to compare travel modes to each other, you should add the travel modes to the filename such as ``Accessibility_5797076_pt_vs_car.shp``. If the user has not specified any travel modes, the tool should only create the Shapefile but not execute any calculations. It should be only possible to compare two travel modes between each other at the time. Accepted travel modes are the same ones that are found in the actual TravelTimeMatrix file (pt_r_tt, car_t, etc.). If the user specifies something else, stop the program, and give advice what are the acceptable values.

**Additionally, you should choose and implement one of the following functionalities**:

5. (option 1). Bundled with AccessViz there is also a separate interactive map that shows the YKR grid values in Helsinki region. The purpose of the map is to help the user to choose the YKR-IDs that s/he is interested to visualize / analyze.

6. (option 2). AccessViz can also visualize the travel mode comparisons that were described in step 4. You can design the style of the map yourself, but try to make it as informative as possible!

7. (option 3). AccessViz can also visualize shortest path routes (walking, cycling, and/or driving) using OpenStreetMap data from Helsinki Region.
The impedance value for the routes can be distance (as was shown in Lesson 7) or time (optional for the most advanced students).
This functionality can also be a separate program (it is not required to bundle include this with the rest of the AccessViz tool)

.. note::

    **NoData values**

    Notice that there are NoData values present in the data (value -1). In such cases the result cell should always end up having a value -1 when doing travel mode comparisons. In the visualizations, the NoData values should be removed before visualizing the map.

.. hint::

    **Modularize your code**

    One of the best practice guidelines is that you should avoid repeating yourself. Thus, we recommend to modularize different tasks in your code and use functions as much as possible. Use meaningful parameter and variable names when defining the functions, so that they are intuitive but short.

.. _UrbanIndicators:

Urban indicators
----------------

In this assignment, the aim is to analyze and compare **two cities or neighborhoods in Finland** (e.g. Helsinki and Tampere, or neighborhood areas in Helsinki) from different perspectives using different indicators. This assignment is not accurately defined, as the idea is to allow you to use your own imagination and interest to explore different datasets and conduct analyses that interest to you, still providing useful insights about the urban areas using specific set of indicators (you should use 2-4 different indicators, see examples from below).

Data
~~~~

You can use any (spatial) data that you can find, and generate your own report describing how the cities differ from each other based on different perspectives (see below hints about possible analyses). You can use any data that is available for example from OpenStreetMap (e.g. streets, buildings, points of interest), or use data that can be found (for example) from:

  - `PaiTuli <https://avaa.tdata.fi/web/paituli/latauspalvelu>`__,
  - `Avoindata.fi service <https://www.avoindata.fi/en>`__
  - `Helsinki Region Infoshare <https://hri.fi/en_gb/>`__.
  - `Open data service of Tampere <https://data.tampere.fi/en_gb/>`__

Data sources are not limited to these, hence you can also use other data from any source that you can find (remember to document where the data is coming from!).

Example analyses
~~~~~~~~~~~~~~~~

In this assignment, you can for example analyze (not limited to these ones):

 - **Population distribution and demographics**

   - create maps and provide some key statistical measures


 - **Building density**

    - create a map showing the building distribution and calculate building density indices for the cities and describe how the areas differ

 - **Green area index**

    - How much green area cities have (in percentages)? Create a map and statistics.

 - **Urban population growth**

    - compare two years to each other and make a comparison map

 - **Accessibility**: Travel times (walking or driving by car) e.g. from railway station to different administrative areas of the city (neighborhoods), or to certain services (e.g. health care, education)

    - Create a tool that visualizes the travel times to selected sports facilities across the Helsinki region

 - **Urban design**: Street network indicators (see Lesson 6 and examples from `here <https://github.com/gboeing/osmnx-examples/tree/master/notebooks>`__)

Structure of the final report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the assignment you should follow traditional structure of scientific article (conduct a *"mini-study"*) where you should provide:

  - A short introduction to the topic (present 2-4 research questions that you aim to answer)
  - Short description of the datasets you used
  - Short generic description of the methods you used
  - Actual codes and visualizations to produce the **results**
  - Description of the results (what should we understand and see from them?)
  - Evaluate with **healthy** criticism the indicators, data and the analyses
    - What kind of assumptions, biases or uncertainties are related to the data and/or the analyses that you did?
    - Any other notes that the reader should know about the analysis

Technical considerations
~~~~~~~~~~~~~~~~~~~~~~~~

In the Notebook, you should present the previous points. Also take care that you:

 - Document your analyses well using the Markdown cells and describe 1) what you are doing and 2) what you can see from the data and your results.

 - Use informative visualizations

   - Create maps (static or interactive)
   - Create other kind of graphs (e.g. line plots)
   - Create subplots that allows to easily compare the cities to each other

 - When writing the codes, we highly recommend that you use and write functions for repetitive parts of the code. As a motivation: think that you should repeat your analyses for all cities in Finland, write your codes in a way that this would be possible. Furthermore, we recommend that you save those functions into a separate .py -script file that you import into the Notebook (`see example from Geo-Python Lesson 4 <https://geo-python.github.io/2018/notebooks/L4/functions.html#Calling-functions-from-a-script-file>`__)

Literature + inspiration
~~~~~~~~~~~~~~~~~~~~~~~~

Following readings provide you some useful backgound information and inspiration for the analyses (remember to cite if you use them):

 - `European Commission (2015). "Indicators for Sustainable Cities" <http://ec.europa.eu/environment/integration/research/newsalert/pdf/indicators_for_sustainable_cities_IR12_en.pdf>`__

 - `Rob Kitchin, Tracey Lauriault & Gavin McArdle (2015). Knowing and governing cities through urban indicators, city benchmarking and real-time dashboards <https://github.com/Automating-GIS-processes/2018/raw/develop/literature/Kitchin_et_al_(2015).pdf>`__ . *Regional Studies, Regional Science,* Vol. 2, No. 1, 6–28.

.. _Your-own-project:

Own project work
----------------

If you have own idea for the final project that you would be willing to do, send us a short description of your idea and we can have a short meeting where we can chat if your project would fit the requirements for the final project. You should send us a description of your own idea **before 21st of December** so that we can soon decide if it meets the requirements of the final project.

Your own final project could be for example:

  - a specific tool that you would like to create for some purpose that you think would be useful

  - a GIS analysis or a set of analyses that you would be interested to conduct and write a short report about them

What is at least required from the final project, is that you have:

 - a working piece of code for your task / problem / analyses that solves it

 - a GOOD documentation (i.e. a tutorial) associated with your Notebook explaining how your tool works

 - OR a report about your analyses and what we can learn from them

The documentation of your tool or analysis / report needs to be written in MarkDown into the same repository
where you upload your codes.
