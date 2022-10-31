#!/bin/bash

### PIP ###

# create a new virtual environment and activate it
python -m venv --clear .virtualenv
source .virtualenv/bin/activate

# install using the _unpinned_ docs/requirements.in.txt
pip install -r docs/requirements.in.txt

# save a pinned docs/requirement.txt
pip freeze --local -r docs/requirements.in.txt > docs/requirements.txt

# deactivate the virtual environment
deactivate


### CONDA ###

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
