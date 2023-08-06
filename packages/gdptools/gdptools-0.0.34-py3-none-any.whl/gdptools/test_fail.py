"""test"""
import geopandas as gpd
import pandas as pd
import numpy as np
import xarray as xr
import pyproj
from pynhd import NLDI
from pynhd import WaterData
import pynhd
from pynhd import GeoConnex
import hvplot.xarray
import hvplot.pandas
from holoviews.element.tiles import EsriTerrain
from gdptools import WeightGen
from gdptools import AggGen
from gdptools import ClimRCatData
from gdptools import UserCatData
gridmet_URL = [
    "http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_met_tmmx_1979_CurrentYear_CONUS.nc#fillmismatch",
    "http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_met_tmmn_1979_CurrentYear_CONUS.nc#fillmismatch",
    "http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_met_pr_1979_CurrentYear_CONUS.nc#fillmismatch",
]
gm_data = xr.open_mfdataset(gridmet_URL, decode_cf=True)
gm_data

# In this case the crs can be extracted from the attributes of the crs coordinate.
crs = pyproj.CRS.from_user_input(gm_data.coords["crs"].attrs["spatial_ref"])

# Get EPSG code
print(crs.to_epsg())

# From visual inspection of the dataset in the previous tab
x_coord = "lon"
y_coord = "lat"
t_coord = "day"  # Note gridMet data uses day for it's time coordinate

# Here we extract the EPSG code, but UserCatData also accepts anything that pyproj.CRS.from_user_input() accepts.
data_crs = crs.to_epsg()

# USGS gage 01482100 Delaware River at Del Mem Bridge at Wilmington De


# hu14 = pynhd.geoconnex(item="hu02", query={"huc2": "14"})
# UC_huc12 = WaterData("wbd12_20201006").bygeom(hu14.geometry[0])
UC_huc12 = gpd.read_file("../blog-gdptools/UC_huc12.geojson")
UC = UC_huc12.hvplot(
    geo=True,
    alpha=0.2,
    c="r",
    frame_width=300,
    xlabel="longitude",
    ylabel="latitude",
    title="Upper Colorado River HUC12 basins",
    aspect="equal",
)
EsriTerrain() * UC



# metadata for calculating weights
# reminder these commented parameters were defined above
# data_crs = 4326
# x_coord = "lon"
# y_coord = "lat"
# t_coord = "day"
sdate = "1979-01-01"
edate = "1979-01-07"
var = ["daily_maximum_temperature", "daily_minimum_temperature", "precipitation_amount"]
shp_crs = 4326
shp_poly_idx = "huc12"
wght_gen_crs = 6931

user_data = UserCatData(
    ds=gm_data,
    proj_ds=data_crs,
    x_coord=x_coord,
    y_coord=y_coord,
    t_coord=t_coord,
    var=var,
    f_feature=UC_huc12,
    proj_feature=shp_crs,
    id_feature=shp_poly_idx,
    period=[sdate, edate],
)

wght_gen = WeightGen(
    user_data=user_data,
    method="parallel",
    output_file="example_weights.csv",
    weight_gen_crs=6931,
)

wdf = wght_gen.calculate_weights()
