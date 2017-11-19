Exercise 4 hints
================

General
-------

- Documentation of the Travel Time Matrix dataset and explanation for different column names can be found at the Accessibility Research Group website: `Helsinki Region Travel Time Matrix 2015 <http://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2015>`__

Problem 1
---------

- Note that the input travel time data is stored in text files when reading in the data.
- Keep columns `'from_id'`,`'to_id'`,`'pt_r_tt'` and `'car_r_t'` in the travel time data files
- Join the data using columns `'from_id'` from the travel time data, and `'YKR_ID'` in the grid-shapefile
- See hints for joining the travel time data to the grid shapefile from our earlier materials from first period (Geo-Python course): `Table join <https://geo-python.github.io/2017/lessons/L6/exercise-6-hints.html?highlight=merge#joining-data-from-one-dataframe-to-another>`__
- Plotting the data takes a while (be patient!)

Problem 2
---------

**General steps**:

 1. Read the files and prepare a single DataFrame where you have travel times for all shopping centers
 2. Find out for each row what is the minimum travel time from those shopping centers
 3. Find out for each row what is the column name of that shopping center that had the minimum travel time
 4. Make maps from the results

Reading multiple files efficiently
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here we are reading multiple files from a folder. We could write the filepaths to all of those files but **it is not efficient!**
Instead, you should use `glob()` -function from module glob to get a filtered list of those files that you want to read and then read the files by iterating over the list. There are lesson materials about doing this in [**here**](https://github.com/Python-for-geo-people/Lesson-5-Reading-Writing/blob/master/Lesson/reading-multiple-files.md#list-files).

Renaming column based on 'to_id' value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We want to rename our column from `pt_r_tt` into `pt_r_tt_XXXXXXX` where XXXXXX is a `to_id` of our datafile which is identical for every row. How you should proceed this problem is following:

 - Extract a **single** value from `to_id` column into a variable called `destination` ==> you might want to use `.loc[]` functionality of Pandas
 - Convert the integer value of `destination` variable as **string**
 - Rename the `pt_r_tt` value:

    - Parse the new column name where you combine `pt_r_tt` text and text from `destination` variable into a new variable called `new_name`. See [a hint from earlier materials](https://github.com/Python-for-geo-people/Exercise-3#general-tips).
    - Rename the `pt_r_tt` column using value from `new_name` variable. Use `data.rename()` -function. See [lesson materials](https://automating-gis-processes.github.io/2016/Lesson3-spatial-join.html?highlight=rename#download-and-clean-the-data).

Finding out which shopping center is the closest

We can find out the minimum value from multiple columns simply by applying a `.min()` function to those columns of a row that we are interessted in:

.. code:: python

    # Define the columns that are used in the query
    value_columns = ['center1', 'center2', 'center3']

    # Find out the minimum value of those column of a given row in the DataFrame
    minimum_values = row[value_columns].min()

It is also possible to find out which column contains that value by applying ``.idxmin()`` (http://pandas.pydata.org/pandas-docs/version/0.18.1/generated/pandas.DataFrame.idxmin.html) -function:

.. code:: python

    # Find out which column contains the minimum value
    closest_center = row[value_columns].idxmin()

In order to calculate the results for each row, you can take advantage of the `.iterrows()` and `.loc()` -functions in (geo)pandas.
See example from Geo-Python course: `Lesson 5: Selecting data <https://geo-python.github.io/2017/lessons/L5/pandas-basic-operations.html#selecting-data-using-indices>`__
