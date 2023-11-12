---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Intersect
 
Similar to the spatial relationships `within` and `contains` covered in the [previous section](point-in-polygon-queries), another common geospatial query asks whether two geometries intersect or touch.

Both queries are implemented in `shapely`:
- [`intersects()`](https://shapely.readthedocs.io/en/stable/manual.html#object.intersects): two objects intersect if the boundary or interior of one object intersect in any way with the boundary or interior of the other object.
- [`touches()`](https://shapely.readthedocs.io/en/stable/manual.html#object.touches): two objects touch if the objects have at least one point in common, but their interiors do not intersect with any part of the other object.

Let’s try these functions out, for instance, using two lines:

```{code-cell}
import shapely.geometry

line1 = shapely.geometry.LineString([(0, 0), (1, 1)])
line2 = shapely.geometry.LineString([(1, 1), (0, 2)])
```

```{code-cell}
line1.intersects(line2)
```

The lines intersect. Do they also touch?

```{code-cell}
line1.touches(line2)
```

`line1` touches `line2`. Adding them both to a multi-line is a quick way of
drawing them inside a Jupyter notebook:

```{code-cell}
shapely.geometry.MultiLineString([line1, line2])
```

We can see here, that the share the point `(1, 1)`, in which `line1` ends, and
`line2` begins. The two lines do not intersect otherwise (‘in their interior’),
so the predicament ’`touch()`’ - as defined above - is true.

If the lines would share some of their interior, that would not be counted as
touching. For instance, `line1` does not touch `line1` (itself), but fulfils
all requirements to be counted as `intersect()`ing with itself:

```{code-cell}
line1.touches(line1)
```

```{code-cell}
line1.intersects(line1)
```
