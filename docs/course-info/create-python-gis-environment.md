# Create a Python GIS environment

## Python environments

Especially on Windows, installing Python packages can sometimes become tricky,
as dependencies between packages and dependencies on external libraries are
difficult to manage there. At times, a specific tool might require an older
version of a package, or even an older Python version. As mentioned earlier, it
is also good practice to install packages from one source, primarily, such as
from the same conda channel. Fortunately, there is a mechanism that allows us to
keep the packages needed for different Python projects separated: **Python
environments**. 

Generally speaking, a *Python environment* is a separate local installation of
all tools required for a particular task, including a Python interpreter, Python
packages, and underlying libraries. Python has built-in, offical tools for
managing environments: the [venv
module](https://docs.python.org/library/venv.html) and the [virtualenv
package](https://virtualenv.pypa.io/). However, there has been a time when GIS
packages installed using these tools did not always function properly on
Windows, because they relied on external libraries. This is why there exists a
historically grown tendency to use `conda` to manage Python environments for
geo-spatial applications. 

Also during this course, we will use `conda` to install and manage Python
packages. Read below how to create a Python environment that includes all tools
needed for this course.


### Creating a conda environment from scratch

Conda’s documentation has an excellent section on how to [create and manage conda
environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).
Please check it for reference on the commands we use below.

Creating a conda environment entails three basic steps: 

1. Create an environment,
2. activate the environment, and
3. install packages into the environment.

The command below work across different operating systems, granted that Anaconda
or Miniconda have been installed.

**Create an environment** and give it a name:

```
conda create --name autogis
```

**Activate the newly created environment**:

```
conda activate autogis
```

You should now see the name of the environment at the command line prompt (at
the beginning of the line).

**Install packages** into the activated environment:

```
# Install jupyter lab + git extension
conda install -c conda-forge jupyterlab jupyterlab-git

# Install packages
conda install -c conda-forge geopandas
conda install -c conda-forge matplotlib
conda install -c conda-forge geojson
conda install -c conda-forge folium
# ... install other packages
```

After you have installed all required packages, you can start working in a local
JupyterLab environment that is linked to your `autogis` conda environment:

```
jupyter lab
```

:::{tip}

It is a good idea to navigate to the folder of your Jupyter Notebook files
before launching JupyterLab.

:::


### Create a conda environment from a YAML file

It is also possible to create a conda environment based on a pre-defined
configuration file. Requirements for the conda environment can be written into a
YAML-file (file extension `.yaml` or .`yml`). 

You can find and download a configuration file that contains all required
packages needed during the *Automating GIS processes* course from its GitHub
repository: [github.com/Automating-GIS-processes/site/](https://github.com/Automating-GIS-processes/site/blob/main/environment.yml)

The configuration file looks like this:

```
name: autogis

channels:
    - conda-forge

dependencies:
    - python=3.10

    # sphinx + dependencies
    - myst-nb
    - sphinx
    - sphinx-book-theme

    # JupyterLab
    - jupyterlab
    - jupyterlab-git

    # lessons
    - bokeh
    - folium
    - geojson
    - geopandas
    - geopy
    - matplotlib
    - osmnx
    - pyrosm
    - r5py
```

Once you have downloaded the file, navigate to its folder, and run the following
command to create a new conda environment according to the specifications set
forward in the file:

```
conda env create --file=environment.yml
```

Solving all dependencies and installing the required packages might take a
surprisingly long time, please remain patient. Once the installation has
finished, you are ready to use your shiny new GIS package environment. Activate
it using conda:

```
conda activate autogis
```


## Docker environments

Docker is a platform that can be used to ‘package’ computing tools into a so
called container. Docker allows to develop applications and computing
environments that are ‘ready-to-run’ without further hassle with installations.

For example, the instances at CSC notebooks are based on a docker image that
contains a ubuntu operating system with Jupyter Lab, Python and relevant Python
packages for this course. Dockerfiles used for setting up the CSC notebooks
environments for Geo-Python and AutoGIS are documented at
[github.com/csc-training/geocomputing](https://github.com/csc-training/geocomputing/).
