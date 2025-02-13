import os.path

import rasterio
from rasterio.features import rasterize
import geopandas as gpd
import numpy as np
import config

with rasterio.open(config.B02_FILE) as b02:
    band_height, band_width = b02.shape
    band_transform = b02.transform
    band_crs = b02.crs

    # Load the shapefile
    shapefile = gpd.read_file(config.SHP_FILE)

    # Reproject the shapefile to match the band's CRS
    shapefile_reprojected = shapefile.to_crs(band_crs)

    # Rasterize the shapefile into a binary mask
    shapes = [(geom, 1) for geom in shapefile_reprojected.geometry]
    shapefile_mask = rasterize(
        shapes,
        out_shape=(band_height, band_width),
        transform=band_transform,
        fill=0,
        dtype=np.uint8
    )

    out_tif = os.path.join(config.FEATURES_FOLDER,'mask_arvi.tif')
    with rasterio.open(
            out_tif,
            'w',
            driver='GTiff',
            height=band_height,
            width=band_width,
            count=1,
            dtype=np.uint8,
            crs=band_crs,
            transform=band_transform
    ) as dst:
        dst.write(shapefile_mask, 1)
