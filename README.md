# Automating GIS-processes

This repository contains the source files for the course [Automating GIS
processes II](https://studies.helsinki.fi/courses/?searchText=GEOG-329-2) at the
[University of Helsinki](https://helsinki.fi/). While the course is taught as an
on-site lab course for students of the Masters’ programme in geography there,
anybody interested in learning **how to use Python to automate the handling and
analysis of geographic information** is welcome to follow the course content at
[autogis-site.readthedocs.io](https://autogis-site.readthedocs.io/).

## License and terms of usage

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img
alt="Creative Commons License" style="border-width:0" align="left"
src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a></a> <img
src="https://github.com/Automating-GIS-processes/2016/blob/master/source/img/GPLv3_Logo.jpg"
width="80">
 
We hope that the teaching material provided here is helpful to other teachers
and learners. Thus, we share all the lessons openly, as well as the source code
and sample data.

**Teaching material and code snippets are licensed** under the **Creative
Commons Attribution-ShareAlike 4.0 International licence** and the **GNU GPLv3
license**, respectively.

**Read more about the license and terms of usage
[here](https://autogis-site.readthedocs.io/en/latest/course-info/license.html)**.

## Browser based programming environment

The instructions in this course provide a programming environment that allows
anyone to immediately try and run all sample code directly in the browser. This
functionality is realised using [Binder](https://mybinder.org/) and the
[CSC](https://csc.fi/)’s [Notebooks](https://notebooks.csc.fi/) (the latter are
available to students and staff at Finnish universities, only).

## Instructions for updating the University of Helsinki course each year

There a few tasks that need to be done to prepare this course for being taught
each autumn. Even without updating any of the content, reserve at minimum a
few days to get everything set up.

1. Before you do anything else, make sure the previous year’s course content has
   been tagged, so that readthedocs provides a yearly version. This can (and
   should) have been done at the end of last autumn’s course, but please
   double-check: 

    ```
    git clone git@github.com:Automating-GIS-processes/site
    cd site
    git tag -a 2022  # <- CHANGE THE YEAR!
    git push --tags
    ```

2. Update the Python environment (ensure stable versions throughout the lifetime
   of the course and of the course page’s version for the current year)
    - Update the pinned versions in pip’s `requirements.txt`:
        ```
        # remove a possibly existing stale environment
        rm -Rf .virtualenv/

        # create a new virtual environment and activate it
        python -m venv .virtualenv
        source .virtualenv/bin/activate

        # install using the _unpinned_ docs/requirements.in.txt
        pip install -r docs/requirements.in.txt

        # save a pinned docs/requirement.txt
        pip freeze > docs/requirement.txt

        # deactivate the virtual environment
        deactivate
        ```
    - Update conda’s `environment.yml` in a similar way:
        - First, make sure [`environment.in.yml`](ci/environment.in.yml) pins
          Python (the interpreter itself) to the [lastest major version available
          from conda-forge](https://anaconda.org/conda-forge/python). In autumn
          2022, the version listed is `3.10.6`, accordingly, the respective line
          in the environment file should read `- python=3.10`.
        - Then use the following commands (they’re analogue to the pip workflow,
          above):
            ```
            # remove a possibly existing stale environment
            conda env remove --name=autogis

            # install a new environment using the _unpinned_
            # ci/environment.in.yml
            conda env create --file=ci/environment.in.yml

            # save a pinned vi/environment.yml
            # (removing the ‘prefix:’ line because it hard-codes
            # your system’s path)
            conda env export --no-builds --name autogis \
            | grep -Ev '^prefix:' \
            > ci/environment.yml
            ```

**Note**, that Python’s release schedule typically foresees a new Python version
around the time of the start of the course. For instance, 2022, Python 3.11 was released
7 days before the course started. Most likely you want to stick with the
previous version, as some of the packages might not have been updated in time.

97. Update, rebuild and upload the docker image TODO

97. Create a *CSC Notebooks* ‘workspace’ and ‘application’

98. Slack TODO

99. Set up GitHub classroom TODO (make new org, create per-exercise repository)

99. Update the course details defined in [`conf.py`](docs/conf.py). Things that
change every year are set up as ‘substitutions’, variables that are replaced
throughout all documents. Edit them to reflect this year’s course’s details
(as of October 2022, this block is starting [at line 42 of
`conf.py`](docs/conf.py#L42)):

```
# The following are the main things that need to be updated every year
# These variables are replaced throughout the course documents
# (see the comment for the first item for an example)
myst_substitutions = { 
    "year": "2022",  # use {{year}} in markdown files to replace it with the current value
    "starting_date": "Tuesday, 1 November 2022",
    "lectures_weekday_time_location": "Tuesday, 15:15-16:45, Exactum C222",
    "work_sessions_weekday_time_location": "Friday, 12:15-16:00, Physicum A113+A114 (GIS lab)",
    ...
}
```

<!--
TODO: Add instructions for future teachers of this course:
    - How to set up GitHub class rooms
    - How to update the documents (including setting the
      substitution-variable in conf.py)
    - How to set up CSC Notebooks
    - How to set up Slack, and where to change the links
    - How to update the dependencies at the beginning of a new year,
      and how to lock them to certain versions
    - How to locally install the dependencies using a virtual env, or conda env
    - How to regenerate the docs locally
    - How to fork the repository, and use merge requests as a way to test
      changes before going live
    - How to remove the lesson contents and add them week after week using pull requests
    - Refreshing the notebooks, and also adding them week after week.
    - ...
-->

## Contact

This course was conceived and designed by Henrikki Tenkanen, and has been
taught, maintained and improved over the years by Vuokko Heikinheimo and Håvard
Wallin Aagesen. Currently (autumn term 2022), Christoph Fink is the responsible
teacher.

You can find contact information on the [course
website](https://autogis-site.readthedocs.io/en/latest/course-info/course-info.html).
