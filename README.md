# Automating GIS-processes - Sphinx + GitHub Pages

[![Build Status](https://travis-ci.org/Automating-GIS-processes/site.svg?branch=master)](https://travis-ci.org/Automating-GIS-processes/site)

Source documents for maintaining the [Automating GIS-processes course pages](https://autogis-site.readthedocs.io/en/latest/).

The docs are written using a combination of [Sphinx](http://www.sphinx-doc.org/en/1.4.9/) and [Jupyter Notebooks](http://jupyter.org/). All the rst files for the lesson contents are located in [source/lessons](source/lessons) -folder and all notebooks are located in [source/notebooks](source/notebooks) folder. Build html pages are located in a separate branch called [gh-pages](https://github.com/Automating-GIS-processes/2018/tree/gh-pages).

## License and terms of usage

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" align="left" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a></a>
<img src="https://github.com/Automating-GIS-processes/2016/blob/master/source/img/GPLv3_Logo.jpg" width="80">
 
We hope that the materials provided here would be helpful for others. Thus, we share all the lesson materials openly, and also our source codes and lesson materials are openly available **from these pages**.

**Our materials and code snippets are licensed** with **Creative Commons Attribution-ShareAlike 4.0 International licence** and **GNU GPLv3 license**. 

**Read more about the license and terms of usage from [here](https://github.com/Automating-GIS-processes/2016/blob/master/source/License-terms.rst)**.

## Requirements

Docs are written using [Sphinx](http://www.sphinx-doc.org/en/1.4.9/) with modified version of the [Read The Docs theme](http://docs.readthedocs.io/en/latest/theme.html).
[Google Analytics](https://analytics.google.com/)
is used for tracking the usage of the site. Thus for building these pages with Sphinx you need to install following (we recommend 
installing [conda](http://conda.pydata.org/docs/using/pkgs.html#install-a-package) from [Anaconda Python distribution package](https://www.continuum.io/downloads)):
  
  - Sphinx
  
    ```
    conda install -c anaconda sphinx=1.5.1
    ```
  
  - Read The Docs Theme
     
    ```
    conda install -c anaconda sphinx_rtd_theme=0.1.9 
    ```
    
  - Google Analytics Sphinx plugin (exceptionally install with Pip that comes with Anaconda!)
  
    ```
    pip install https://pypi.python.org/packages/48/7e/1b383d54276a743ee195f6f97a2a77054fa1f976913923e1e64fe500d975/sphinxcontrib-googleanalytics-0.1.tar.gz#md5=f9da59a753b8a045945c5e35ed1e2481
    ```

## Writing .rst files

Sphinx uses .rst -files ([reStucturedText](https://en.wikipedia.org/wiki/ReStructuredText)). Thus all the documentation needs to be written into .rst files. It is easy, intuitive and quite similar 
to write as Markdown but rst makes it possible to include many things that are impossible to do with Markdown (such as including raw html code, embedding videos or interactive visualizations, having nice
colored notes or hints etc.). All the .rst -files should be placed into the [/source](/source) -folder which is the directory where Sphinx tries to find the documentation by default. **Those .rst files are also 
the ones that you want to modify if you desire to make changes to the documents**.

## Writing Jupyter Notebook files

All the programming materials in this site are written using [Jupyter Notebooks](https://jupyter.org/). These notebooks are converted into html pages during the build of the pages using [npsphinx](https://nbsphinx.readthedocs.io/en/0.4.2/) extension to Sphinx.

## Continuous Integration with Travis CI

[Travis-CI](https://travis-ci.org/) makes it possible to build the GitHub pages automatically whenever a change has been pushed to master.
It is highly recommendable to use separate branches for developing the materials (such as using `develop` branch) and then merging the changes
from that branch to `master` using **pull requests**.

- Travis Integration is controlled from [.travis.yml](.travis.yml).
- See a bit more documentation from [Travis-integration.md](Travis-integration.md)

## Browser based programming environment

This course site provides programming environment that allows anyone to immediately try and run all the codes directly in the browser. This functionality is done using [Binder](https://mybinder.org/) and [CSC Notebooks (for Universities in Finland)](https://notebooks.csc.fi/#/) -services.

Binder environment is controlled from [environment.yml](environment.yml). CSC Notebooks are controlled separately from [https://github.com/Automating-GIS-processes/notebooks](https://github.com/Automating-GIS-processes/notebooks) -repository. 

## Contact & Developers

- **Håvard Wallin Aagesen**

- **Henrikki Tenkanen**

- **Vuokko Heikinheimo**

See contact info from [our course website](https://autogis-site.readthedocs.io/en/latest/course-info/course-info.html).


