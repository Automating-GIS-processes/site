# Automatic Sphinx-builds with Travis-CI

## Steps

- Configure your travis build from `.travis.yml` file.
- Update the `push.sh` file to push the built Sphinx pages to `gh-pages` branch.
- Activate the repository from Travis-CI settings
- Once you have set up the `.travis.yml` and activated the repository, build the first version by triggering the build from 
[Travis-CI dashboard](https://travis-ci.org/dashboard)
