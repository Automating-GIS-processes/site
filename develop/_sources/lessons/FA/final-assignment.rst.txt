Final assignment
================

Start your final assignment by accepting the `GitHub Classroom <https://classroom.github.com/a/ZsdqHr4m>`_ for the final work.

Aim of the work
---------------

The final assignment is a project of your own where the aim is to apply the programming techniques and skills that we have learned during the course and do something useful with them.

You have three options for the final project that you can choose from:

#. AccessViz_ which is a GIS-tool that can visualize and compare travel times by different travel modes in Helsinki Region.
#. UrbanIndicators_ which is a *"mini-study"* where the aim is to use different urban indicators to understand urban areas and compare them to each other.
#. Your-own-project_. If you have a tool, problem or analysis of your own in mind, send your idea to us by email or in Slack (before Friday 21.12.2018), and we can discuss and accept your idea if it is suitable for the final project.

Think the final project as a challenge for yourself to show and implement the programming skills that you have learned this far. You have learned a lot already!

Feel free to be creative with the final assignment. Here is the suggested structure of the work, that also serves as the basis for grading:

1. Data acquisition (Fetching data, subsetting data, storing intermediate outputs etc.)
2. Data analysis (Enriching and analyzing the data, eg. spatial join, overlay, buffering, other calculations..)
3. Visualization (Visualizing main results and other relevant information as maps and graphs)
4. Repeating the steps for another set of input data (eg. another city, or another target location)
5. Good documentation


What should be returned?
~~~~~~~~~~~~~~~~~~~~~~~~

Write your codes into a single (or multiple) notebook(s) and return the codes to your GitHub repository.
Good documentation of the code will be highly regarded and
will affect positively in the grading of the final work. You can choose yourself what tools / techniques / modules you want to use.

When is the deadline?
~~~~~~~~~~~~~~~~~~~~~

You should **return your final assignment in GitHub by 11.1.2018 at 23:59** at latest. Of course, you can return your work also before the deadline! If you are ready
before the deadline, please send us a note about it (e.g. in Slack), so that we know and can start evaluating your work.

Grading
~~~~~~~

In the evaluation of the final work different functionalities of the code are evaluated individually.
Thus, if you do not get all different parts / functionalities of the tool working that are described below, it is not the *"the end of the world"*.
The main idea in the final project is that you try to use your skills and do GIS analyses in Python **independently**.

**Good documentation of the code and your project is highly appreciated!!!**
One more time: Good documentation of the code and your project is highly appreciated!
You should use Markdown cells to document your work along the way (take a look of these small tutorials to see `how to add a Markdown cell to Notebook <http://www.firstpythonnotebook.org/markdown/>`_ and `how to use Markdown syntax <https://guides.github.com/features/mastering-markdown/>`_git st ).

The grading is based on a typical 0-5 scale. See detailed grading criteria :doc:`here <final-assignment-grading>`.

Best practices
--------------

There are several guidelines how to do programming "in a proper way". These best practices when doing programming are well described in `this article <http://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745>`_
Wilson et al. (2014) that include aspects such as:

 1. *"Write programs for people, not computers."*

 2. *"Let the computer do the work."*

 3. *"Make incremental changes."*

 4. *"Don't repeat yourself (or others)."*

 5. *"Plan for mistakes."*

 6. *"Optimize software only after it works correctly."*

 7. *"Document design and purpose, not mechanics."*

 8. *"Collaborate."*

These kind of guidelines are extremely useful. I recommend that you take at least a short look at the article before starting your final project because it helps you to
finnish your project efficiently and in such a manner that works and makes your life (and others) easier!

For this final project, the most important aspects from the list above are numbers 1-4 and number 7 (although they are all important).
Thus, at least take a look at those aspects from the article before
starting your work.

Documenting your work
~~~~~~~~~~~~~~~~~~~~~

Good documentation is one the most important aspect when doing any programming. It allows us (and also yourself) to understand what you have done, or tried to do with the code. Thus, we cannot emphasize it more to document your codes, and the work in general, properly. Hence, use comments in the code and also using Markdown cells where you explain the purpose of different parts of the code.

Commit your work frequently!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the previous exercises that we have done during the course, it has not maybe been that important that you commit (upload) your work frequently to GitHub because the size and complexity of the codes have been relatively low. However, now as you are doing a larger programming project, I really recommend that you **commit and upload your changes to GitHub frequently!** Whenever you get some functionality working in your code, it is a good time to commit your changes. In that way, your work is saved and if something goes wrong and your code does not work anymore as planned, you can **go back in history** and start from a state that was still working.

Hints
~~~~~

Similarly as before, we gather hints separately to `here <https://automating-gis-processes.github.io/2018/lessons/FA/fa-hints.html>`_. However, because this is the final work, we encourage you to try hard yourself first, find information from the internet, and ask your friends before asking help from us. However, if there is a common problem or some of the instructions needs more
explanation, we will update those into the hints page.

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

    - Create e.g. a travel time map (choropleth) that shows travel times to centroids of different neighborhoods

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