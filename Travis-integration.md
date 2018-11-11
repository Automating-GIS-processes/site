# Automatic Sphinx-builds with Travis-CI

## Steps

### Prepare Github Pages

- Update the `push.sh` file to push the built Sphinx pages to `gh-pages` branch.
- Initialize an empty `gh-pages` -branch (if does not exist already) with:
   - `git checkout --orphan gh-pages`
       - if gh-pages branch exists activate it
   - create `.nojekyll` file to ensure that GitHub pages are built correctly
       - $ touch .nojekyll
   - commit and push to gh-pages branch on your repository

### Set up Travis 
- Create [Personall Access Token](https://github.com/settings/tokens) for your GitHub repository (needs to be done separately for each repository)
  - Copy / Paste the token temporarily to somewhere (needed on the next step)
- Create (locally) encrypted Travis Token for your repository using Ruby's [travis -library](https://rubygems.org/gems/travis/versions/1.8.8)
   - You need to have Ruby installed on your computer + travis package (`gem install travis`)
   - Generate token with travis library with command `$ travis encrypt GH_TOKEN=[paste your token here]`
- Configure your travis build from `.travis.yml` file.
- Activate the repository from Travis-CI settings
- Once you have set up the `.travis.yml` and activated the repository, build the first version by triggering the build from 
[Travis-CI dashboard](https://travis-ci.org/dashboard)

