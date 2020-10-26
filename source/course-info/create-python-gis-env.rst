Creating a Python GIS environment
=================================

Python environments
--------------------

Installing various GIS packages in Python can be sometimes a bit tricky due to various dependencies
among the packages. Sometimes an older version of the package, or even an older Python version might be required for a
specific tool to work. As mentioned earlier, it is also good practice to install as many packages as possible from the same
conda channel, and not to mix conda and pip for installations if not strictly necessary. The easiest way to get the installation working smoothly is to build a dedicated
Python environment for the GIS tools.

In practice, a python environment is a separate installation of all required tools including
the Python interpreter, libraries and script files. Python has it's own `virtualenv library <https://virtualenv.pypa.io/en/latest/>`__
for creating isolated Python environments. During this course, we recommend using conda form installing and managing
Python packages and we will introduce how to create
`Python environment using conda <https://conda.io/docs/user-guide/tasks/manage-environments.html>`_
that includes all tools needed during this course.

Create an environment from scratch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Conda has an excellent documentation about `creating and managing conda environments <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`__
where you can check details of the used commands.

Main steps of creating a conda environment include 1) creating the environment, 2) activating the environment. 3) installing pacakges.
The following commands should work in different operating systems where Anaconda or Miniconda has been installed:

1. Create an environment and give it a name:

.. code-block::

    conda create --name python-gis

Follow the instructions in the terminal window and react (hit enter or "YES") if needed.

2. Activate the environment:

.. code-block::

    conda activate python-gis

You should now see the name of the environment at the start of the command line.

2. Install needed packages:

.. code-block::

    # Install jupyter lab + git extension
    conda install -c conda-forge jupyterlab
    conda install -c conda-forge jupyterlab-git

    # Install packages
    conda install -c conda-forge geopandas
    conda install -c conda-forge matplotlib
    conda install -c conda-forge geojson
    conda install -c conda-forge mapclassify
    conda install -c conda-forge contextily
    conda install -c conda-forge folium
    conda install -c conda-forge mplleaflet
    conda install -c conda-forge osmnx
    # ... install other packages

After you have installed all required packages, you can start working in a local Jupyter Lab environment that is
linked to your python-gis conda environment by launchin jupyter lab on the command line:



Create an environment from an .yml file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~















Install Python GIS environment using YML configuration file
===========================================================

Installing various GIS packages in Python can be sometimes a bit tricky because there might exist complex dependencies
that requires specific versions of different packages and even specific version of Python itself.
The easiest way to get the installation working smoothly is to build a dedicated `Python environment <https://conda.io/docs/user-guide/tasks/manage-environments.html>`__
for GIS using conda and preferably installing packages using mostly the same `conda channel <https://conda.io/docs/glossary.html#channels>`__.
Using dedicated environment has the advantage that you can load the environment when needed.
In this way, it won't break any existing installations that you might have.

There are basically three steps required to install GIS packages and start using them in your operating system:

 1. Download suitable environment file (.yml) to your operating system
 2. Install packages and create a dedicated conda environment for ``gis``
 3. Activate the environment and start using the packages

1. Download environment file for your operating system
------------------------------------------------------

A dedicated repository contains a list of *.yml* environment files created for different operating systems
(*work in progress*). Go to `<https://github.com/Automating-GIS-processes/install>`__ repository.

You should download a version that suits your operating system and then follow the instructions below.

2. Install GIS packages into dedicated environment
--------------------------------------------------

Once you have downloaded the yml file that fits your operating system you can install the packages
by using following command:

.. code:: bash

    $ conda env create -f gis-win-10.yml

.. note::

    Solving the environment and installing all the packages might take surprisingly long time, so be patient.

3. Activate the GIS environment and start doing GIS
---------------------------------------------------

Once the installations have been done, you are ready to start using the GIS packages by activating the environment.
It can be done by running following command from the command prompt / terminal:

.. code:: bash

    $ source activate gis

