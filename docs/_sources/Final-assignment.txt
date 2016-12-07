Final assignment
================

Start your final assignment by accepting the `GitHub Classroom <https://classroom.github.com/assignment-invitations/ae5cbb5c4e2b20259fc0607c929c25c6>`_ for the final work.

Aim of the work
---------------

The final assignment is a project of your own where the aim is to apply the programming techniques and skills that we have learned during the course and do
something useful with them.

You have two options for the final project that you can choose from:

#. AccessViz_ which is a GIS-tool that can visualize and compare travel times by different travel modes in Helsinki Region.
#. Your-own-project_. If you have a tool, problem or analysis of your own in mind, send your idea to us by email (before Friday 9.12.2016), and we can discuss and accept your idea if it is suitable for the final project.

Think the final project as a challenge for yourself to show and implement the programming skills that you have learned this far. You have learned a lot already!

What should be returned?
~~~~~~~~~~~~~~~~~~~~~~~~

Write your codes into a single (or multiple) Python file(s) and return the codes to your GitHub repository.
Good documentation of the code will be highly regarded and
will affect positively in the grading of the final work. You can choose yourself what tools / techniques / modules you want to use.

When is the deadline?
~~~~~~~~~~~~~~~~~~~~~

You should **return your final assignment in GitHub by 6.1.2017 at 23:59** at latest. Of course, you can return your work also before the deadline! If you are ready
before the deadline, please send us a note about it (e.g. raise an issue), so that we know and can start evaluating your work.

Grading
~~~~~~~

In the evaluation of the final work different functionalities of the code are evaluated individually.
Thus, if you do not get all different parts / functionalities of the tool working that are described below, it is not the *"the end of the world"*.
The main idea in the final project is that you try to use your skills and do GIS analyses in Python **independently**.

**Good documentation of the code and your project is highly appreciated!!!** One more time: Good documentation of the code and your project is highly appreciated!

The grading is based on a typical 0-5 scale.

Best practices
--------------

There are several guidelines how to do programming "in a proper way". These best practices when doing programming are well described in `this article <https://arxiv.org/pdf/1210.0530.pdf>`_
Wilson et al. (2013) that include aspects such as:

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

Good documentation is one the most important aspect when doing any programming. It allows us (and also yourself) to understand
what you have done or tried to do with the code. Thus, we cannot emphasize it more to document your codes, and the work in general, properly. Hence, use comments
in the code where you explain the purpose of different parts of the code.

In addition, **describe and explain your work also in general**, so that everyone understands:

 - What your codes should do? (a general description about the aim of the work)

 - How your code / tool(s) should be used?

    - A practical example of how the tool is used should always be included!

    - What function(s) the user can use and how? Describe.

    - What parameters your function(s) have and what are the possible input values for them. Describe.

The general description of your tool / codes / analyses and how they work should be written into the **README.md** -file that is located in the root of the
final assignment GitHub repository.

Commit your work frequently!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the previous exercises that we have done during the course, it has not maybe been that important that you commit (upload) your work frequently to GitHub because the
size and complexity of the codes have been relatively low. However, now
as you are doing a larger programming project, I really recommend that you **commit and upload your changes to GitHub frequently!** Whenever you get some functionality
working in your code, it is a good time to commit your changes. In that way, your work is saved and if something goes wrong and your code does not work anymore as planned,
you can **go back in history** and start from a state that was still working.

Hints
~~~~~

Similarly as before, we gather hints separately to `here <https://github.com/Automating-GIS-processes/Final-Assignment-hints>`_. However, because this is the final work, we encourage you to try hard yourself first,
find information from the internet, and ask your friends before asking help from us. However, if there is a common problem or some of the instructions needs more
explanation, we will update those into the hints page.

.. _AccessViz:

AccessViz
---------

What the tool should do?
~~~~~~~~~~~~~~~~~~~~~~~~

**AccessViz** is a set of tools that can be used for managing and helping to analyze
Helsinki Region Travel Time Matrix data (2013 / 2015) that can be downloaded from
`here <http://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix/>`_.
Read also the description of the dataset from the web-pages so that you get familiar with the data.

AccessViz tool package has following main functionalities (i.e. functions) that should work independently:

1. AccessViz finds from the data folder all the matrices that user has specified by assigning a list of integer values that should correspond to YKR-IDs found from the attribute table of a Shapefile called `MetropAccess_YKR_grid.shp <http://www.helsinki.fi/science/accessibility/data/MetropAccess-matka-aikamatriisi/MetropAccess_YKR_grid.zip>`_.
If the ID-number that the user has specified does not exist in the data folders, the tools should warn about this to the user but still continue running.
The tool should also inform the user about the execution process: tell the user what file is currently under process and how many files there are left
(e.g. "Processing file travel_times_to_5797076.txt.. Progress: 3/25").

2. AccessViz can create Shapefiles from the chosen Matrix text tables (e.g. *travel_times_to_5797076.txt*) by joining the Matrix file with
MetropAccess_YKR_grid Shapefile  where ``from_id`` in Matrix file corresponds to ``YKR_ID`` in the Shapefile. The tool saves the result in the output-folder
that user has defined. You should name the files in a way that it is possible to identify the ID from the name (e.g. 5797076).

3. AccessViz can visualize the travel times of selected YKR_IDs based on the travel mode that the user specifies. It can save those maps into a folder that user specifies. The output
maps can be either **static** or **interactive** and user can choose which one with a parameter. You can freely design yourself the style of the map, colors, travel time intervals (classes)
etc. Try to make the map as informative as possible!

4. AccessViz can also compare **travel times** or **travel distances** between two different travel modes (more than two travel modes are not allowed).
Thus IF the user has specified two travel modes (passed in as a list) for the AccessViz, the tool will calculate the time/distance difference of those travel modes
into a new data column that should be created in the Shapefile. The logic of the calculation is following the order of the items passed on the list where first
travel mode is always subtracted by the last one: ``travelmode1 - travelmode2``.
The tool should ensure that distances are not compared to travel times and vice versa. If the user chooses to compare travel modes to each other,
you should add the travel modes to the filename such as ``Accessibility_5797076_pt_vs_car.shp``. If the user has not specified any travel modes,
the tool should only create the Shapefile but not execute any calculations. It should be only possible to compare two travel modes between each other at the time.
Accepted travel modes are the same ones that are found in the actual TravelTimeMatrix file (pt_r_tt, car_t, etc.).
If the user specifies something else, stop the program, and give advice what are the acceptable values.

5. (optional). Bundled with AccessViz there is also a separate interactive map that shows the YKR grid values in Helsinki region. The purpose of the map is to help
the user to choose the YKR-IDs that s/he is interested to visualize / analyze.

6. (optional). AccessViz can also visualize the travel mode comparisons that were described in step 4. You can design the style of the map yourself, but try to make it
as informative as possible!

.. note::

    **NoData values**

    Notice that there are NoData values present in the data (value -1). In such cases the result cell should always end up having a value -1 when doing travel
    mode comparisons. In the visualizations, the NoData values should be removed before visualizing the map.

.. hint::

    **Modularize your code**

    One of the best practice guidelines is that you should avoid repeating yourself. Thus, we recommend to modularize different tasks in your
    code and use functions as much as possible. Use meaningful parameter and variable names when defining the functions, so that they are intuitive but short.

.. _Your-own-project:

Own project work
----------------

If you have own idea for the final project that you would be willing to do, send us a short description of your idea and
we can have a short meeting where we can chat if your project would fit the requirements for the final project.
You should send us a description of your own idea **before 9th of December** so that we can soon decide if it meets the requirements
of the final project.

Your own final project could be for example:

  - a specific tool that you would like to create for some purpose that you think would be useful

  - a GIS analysis or a set of analyses that you would be interested to conduct and write a short report about them

What is at least required from the final project, is that you have:

 - a working piece of code for your task / problem / analyses that solves it

 - a GOOD documentation explaining how your tool works

 - OR a report about your analyses and what we can learn from them

The documentation of your tool or analysis / report needs to be written in MarkDown into the same repository
where you upload your codes.