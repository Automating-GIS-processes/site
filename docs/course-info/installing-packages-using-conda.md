# Installing Python packages using conda

Conda has an excellent [online user guide](https://docs.conda.io/projects/conda)
that covers most of the basic things, such as installing new packages.

## `conda install`

You can install new packages using the [`conda
install`](https://docs.conda.io/projects/conda/en/latest/commands/install.html)
command. The basic syntax for installing packages is `conda install
package-name`.
In many cases, we also want to specify the **conda channel** from which the package is downloaded using the parameter `-c`.

To install [Pandas](https://pandas.pydata.org) from the
[conda-forge](https://anaconda.org/conda-forge/) channel, run the following command:

```
conda install -c conda-forge pandas
```

Conda will automatically install other packages that are needed as
dependencies. It will also make sure that the versions of all installed packages
are compatible, and update or even downgrade packages, accordingly. Read more
about how packages are installed and managed in [conda’s
documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html#installing-packages).

You can **install other useful packages in a similar way**:

```
conda install -c conda-forge matplotlib
conda install -c geopandas
```


:::{note}

[Conda channels](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/channels.html)
are remote locations where packages are stored. During this course, we download
most packages from the [conda-forge](https://conda-forge.org/#about) channel.

:::


:::{admonition} Conflicting packages
:class: hint

A good rule of thumb is to **always install packages from the same channel**
(for this course, we prefer the `conda-forge` channel). 

In case you encounter an error message when installing new packages, you might
want to first check the versions and channels of existing packages using the
`conda list` command before trying again.

:::
