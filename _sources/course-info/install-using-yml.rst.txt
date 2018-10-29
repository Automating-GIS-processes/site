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

You should download a version that suites your operating system and then follow the instructions below.

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

