---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Overview

In this lesson, we will get to know how geopandas handles some typical GIS
operations: **overlay analysis** (e.g., unions, or differences of multiple
geometries), **aggregating** geometries (e.g., smaller statistical units into
larger ones), **simplifying** geometries (to be printed or shown at smaller map
scales), and **classifying** numerical data into categories for map display. 


## Learning goals

After this lesson, you should know how to:

- create new geometries by adding, subtracting or intersecting two geometries,
- combine geometries based on a common attribute (*dissolving* them),
- create categories for numerical data based on classifiers such as *natural
  breaks*, *equal interval*, or *quantiles*, and
- simplify geometries according to a maximum-error threshold


## Lesson video

<iframe width="560" height="315" src="https://www.youtube.com/embed/xpetCZXp9Y4?si=a6aCQZ2rL7wjFZX5" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>