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
linked to your python-gis conda environment by launching jupyter lab on the command line.

It's a good idea to first navigate to the folder where your Jupyter Notebook -files are located before launching Jupyter Lab.


.. code-block::

    jupyter lab

Note, Jupyter Lab will probably prompt you to "Build" the installation in order to get the git-plugin to show.

Create an environment from an YAML file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is also possible to create a conda environment based on a pre-defined configuration file.
Requirements for the conda environment can be written into a YAML-file (file extension .yaml or .yml).

You can find and download a configuration file that contains all required packages needed during the autogis course
in `here <https://github.com/Automating-GIS-processes/site/blob/master/ci/py38-GIS.yaml>`__.

The contents of the configuration file look like this:

.. code-block::

    name: python-gis

    channels:
      - conda-forge
      - patrikhlobil

    dependencies:
      - python=3.8
      - jupyterlab
      - jupyterlab-git
      - matplotlib
      - geopandas
      - geojson
      - pysal
      - mapclassify
      - osmnx
      - pyrosm
      - geopy
      - geojson
      - rasterio
      - contextily
      - folium
      - mplleaflet
      - bokeh
      - patrikhlobil::pandas-bokeh
      - pip


Once you have downloaded the file to your own computer, you can navigate to that folder and run this command to create
the conda environment using the file:

.. code-block::

    conda env create -f py38-GIS.yaml

Solving the environment and installing all the packages might take a surprisingly long time, so be patient.

Once the installations have been done, you are ready to start using the GIS packages by activating the environment.

.. code-block::

    source activate python-gis

Finally, you should be able to start working with Jupyter lab by activating it on the command line.
It's a good idea to first navigate to the folder where your Jupyter Notebook -files are located before launching Jupyter Lab.

.. code-block::

    jupyter lab


Docker environments
--------------------

Docker is a platform that can be used to "package" computing tools into a so called container.
Docker allows to develop applications and computing environments that are "ready-to-run" without
further hassle with installations.

For example, the instances at CSC notebooks are based on a docker image that contains
a ubuntu operating system with Jupyter Lab, Python and relevant Python packages for this course.
Dockerfiles used for setting up the CSC notebooks environments for Geo-Python and AutoGIS are
documented at `https://github.com/csc-training/geocomputing/ <https://github.com/csc-training/geocomputing/tree/master/rahti/autogis-course-part1>`__.

For the purposes of this course, we recommend students to use the YAML file above to manage the installations.