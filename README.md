# Automating GIS-processes - Sphinx + GitHub Pages

Source documents for maintaining the [Automating GIS-processes course pages, year 2016](https://automating-gis-processes.github.io/2016/).

The docs are written in [Sphinx](http://www.sphinx-doc.org/en/1.4.9/) and all the rst files for the lesson contents are located in the [source](source/) -folder. 
Build html pages are located in the [docs](docs/) -folder.

## License and terms of usage

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /></a> 

We hope that the materials provided here would be helpful for others. Thus, we share all the lesson materials openly, and also our source codes and lesson materials are openly available **from these pages**.

**Our materials and code snippets are licensed** with **Creative Commons Attribution-ShareAlike 4.0 International licence** and **GNU GPLv3 license**. 

**Read more about the license and terms of usage from [here](https://github.com/Automating-GIS-processes/2016/blob/master/source/License-terms.rst)**.

## Requirements

Docs are written using [Sphinx](http://www.sphinx-doc.org/en/1.4.9/) with modified version of the [Read The Docs theme](http://docs.readthedocs.io/en/latest/theme.html). [Google Analytics](https://analytics.google.com/)
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

## Building the pages

Unlike Markdown pages (such as this page), Sphinx pages need to be build before you can see the final result. This is because Sphinx produces html pages (into [/docs](/docs) -folder) 
that can have many nice features such as the navigation bar on the left, efficient search functionality etc. 
  
Build the pages by navigating to the root of the repository (i.e. to a folder where this README.md -file is located) and executing following command:
 
 ```
 make html
 ```
 
Sphinx will then start building the pages and the final html pages will be located in [/docs](/docs) -folder. This is a custom location (by default the docs would go to /build -folder) that matches how GitHub 
wants them so that GitHub Pages works. I have edited the [make.bat](make.bat) for achieving this. 

### Sphinx actually runs the codes! 

One of the most powerful features that Sphinx has (in my opinion), is that it will actually run all the Python codes that are written under the `.. ipython:: python` code block. This makes
it possible that you can e.g. plot images dynamically to the pages without doing any manual work (adding images with links), see and show the contents of a datafile on the pages without needing to 
add them manually (which is how you would do it on Markdown pages). Hence, doing the documentation reminds a bit how you can write documents with [Jupyter Notebooks](https://jupyter.org/) but with a nicer 
looking pages.  

### Data needs to be in the repository

What this kind of dynamic Python interpreter of Sphinx means though, is that you need to also keep the data that you use in the documentation together with the docs. I keep all the datasets 
used for building these pages in the [/data](/data) -folder and then read the files from there in the background (hidden from the user). See an example of how to hide (with `:suppress:` command) 
the data-reading-procedure from the user, from [here](https://raw.githubusercontent.com/Automating-GIS-processes/2016/master/source/Lesson3-table-join.rst).    

## Contact & Developers

Main developer and maintainer of these materials: **Henrikki Tenkanen**

Co-developers: **Vuokko Heikinheimo**.

See contact info from [here](https://github.com/Automating-GIS-processes/2016/blob/master/source/course-info.rst#instructors).


