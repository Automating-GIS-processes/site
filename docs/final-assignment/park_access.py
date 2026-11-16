"""
Green space accessibility in Helsinki
=====================================

This script calculates, for each major district of Helsinki, the share of
residents who live within walking distance (300 m) of a public park.

Data sources:
- Parks: OpenStreetMap (leisure=park), downloaded with osmnx
- Population: HSY population grid (250 m x 250 m cells), downloaded via WFS
- Districts: major districts of Helsinki (local GeoPackage file)

The workflow is fully parameterised, and can be reused for other cities by
changing the values in CONFIG.
"""

import logging
import time
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import osmnx as ox

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


CONFIG = {
    "place_name": "Helsinki, Finland",
    "districts_file": Path("data") / "helsinki_city_districts_2021.gpkg",
    "population_layer": "asuminen_ja_maankaytto:Vaestotietoruudukko_2024",
    "distance_m": 300,  # WHO recommendation: green space within 300 m of home
    "metric_crs": "EPSG:3857",  # projected CRS in metres, for accurate distances
    "output_dir": Path("output"),
    "cache_dir": Path("cache"),
}

WFS_URL = "https://kartta.hsy.fi/geoserver/wfs"


def retry(func, attempts=3, wait_s=5):
    """Call `func()`, and try again if it fails (e.g., due to network errors)."""
    for attempt in range(1, attempts + 1):
        try:
            return func()
        except Exception as error:
            logger.warning("Attempt %d/%d failed: %s", attempt, attempts, error)
            if attempt == attempts:
                raise
            time.sleep(wait_s)


def load_districts(path: Path) -> gpd.GeoDataFrame:
    """Read the district polygons, and keep only the name and geometry."""
    districts = gpd.read_file(path)
    districts = districts.rename(columns={"name": "district"})
    return districts[["district", "geometry"]]


def load_population(layer: str, cache_dir: Path) -> gpd.GeoDataFrame:
    """Download the HSY population grid, or read it from the local cache."""
    cache_file = cache_dir / f"{layer.split(':')[1]}.gpkg"
    if cache_file.exists():
        logger.info("Reading population grid from cache: %s", cache_file)
        return gpd.read_file(cache_file)

    url = (
        f"{WFS_URL}?service=wfs&version=2.0.0&request=GetFeature"
        f"&typeName={layer}&srsName=EPSG:3879"
    )
    grid = retry(lambda: gpd.read_file(url)).set_crs("EPSG:3879")
    grid = grid[["asukkaita", "geometry"]].rename(columns={"asukkaita": "population"})
    grid["population"] = grid["population"].fillna(0)

    cache_dir.mkdir(parents=True, exist_ok=True)
    grid.to_file(cache_file)
    logger.info("Downloaded %d population grid cells", len(grid))
    return grid


def load_parks(place_name: str) -> gpd.GeoDataFrame:
    """Download public parks from OpenStreetMap."""
    parks = retry(lambda: ox.features_from_place(place_name, tags={"leisure": "park"}))
    parks = parks[parks.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]
    parks = parks[["name", "geometry"]].reset_index(drop=True)
    logger.info("Downloaded %d parks", len(parks))
    return parks


def residents_near_parks(
    population: gpd.GeoDataFrame, parks: gpd.GeoDataFrame, distance_m: float
) -> gpd.GeoDataFrame:
    """Flag the grid cells whose residents live within `distance_m` of a park."""
    park_zone = parks.buffer(distance_m).unary_union
    population = population.copy()
    population["near_park"] = population.centroid.within(park_zone)
    return population


def summarise_by_district(
    population: gpd.GeoDataFrame, districts: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Calculate the total population and the share living near a park per district."""
    joined = gpd.sjoin(population, districts, how="inner", predicate="intersects")
    joined["population_near_park"] = joined["population"].where(joined["near_park"], 0)

    summary = joined.groupby("district")[["population", "population_near_park"]].sum()
    summary["share_near_park"] = summary["population_near_park"] / summary["population"]

    return districts.merge(summary.reset_index(), on="district")


def run_checks(population: gpd.GeoDataFrame, result: gpd.GeoDataFrame) -> None:
    """Validate the results."""
    assert population.crs == result.crs, "CRS mismatch between inputs and result"
    assert result["share_near_park"].between(0, 1).all(), "Shares must be between 0 and 1"
    assert result["population"].sum() > 0, "No population found in the districts"
    logger.info("All checks passed")


def plot_result(result: gpd.GeoDataFrame, distance_m: float, output_file: Path) -> None:
    """Plot a choropleth map of the share of residents living near a park."""
    fig, ax = plt.subplots(figsize=(10, 8))
    result.plot(
        ax=ax,
        column="share_near_park",
        scheme="NaturalBreaks",
        k=5,
        cmap="Greens",
        edgecolor="white",
        legend=True,
        legend_kwds={"title": "Share of residents", "loc": "lower right"},
    )
    for _, row in result.iterrows():
        point = row.geometry.representative_point()
        ax.annotate(row["district"], xy=(point.x, point.y), ha="center", fontsize=8)
    ax.set_title(f"Share of residents living within {distance_m} m of a park")
    ax.set_axis_off()
    fig.savefig(output_file, dpi=200, bbox_inches="tight")
    plt.close(fig)
    logger.info("Map saved to %s", output_file)


def main(config: dict = CONFIG) -> gpd.GeoDataFrame:
    config["output_dir"].mkdir(parents=True, exist_ok=True)
    crs = config["metric_crs"]

    districts = load_districts(config["districts_file"]).to_crs(crs)
    population = load_population(config["population_layer"], config["cache_dir"]).to_crs(crs)
    parks = load_parks(config["place_name"]).to_crs(crs)

    population = residents_near_parks(population, parks, config["distance_m"])
    result = summarise_by_district(population, districts)
    run_checks(population, result)

    result.to_file(config["output_dir"] / "park_access_by_district.gpkg")
    plot_result(result, config["distance_m"], config["output_dir"] / "park_access_map.png")

    print(
        result[["district", "population", "share_near_park"]]
        .sort_values("share_near_park", ascending=False)
        .to_string(index=False, float_format="{:.1%}".format)
    )
    return result


if __name__ == "__main__":
    main()
