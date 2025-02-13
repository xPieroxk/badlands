import os
import rasterio
import numpy as np
import config


# features
def compute_ndwi(b03, b08):
    return (b03 - b08) / (b03 + b08)


def compute_ndvi(b04, b08):
    return (b08 - b04) / (b08 + b04)


def compute_arvi(b02, b04, b08):
    return (b08 - (2 * b04 - b02)) / (b08 + (2 * b04 - b02))


def compute_evi2(b04, b08):
    return 2.5 * (b08 - b04) / (b08 + 2.4 * b04 + 1)


def compute_msi(b04, b08):
    return (b08 - b04) / (b08 + b04 + 0.5)


def compute_ngrdi(b03, b04):
    return (b03 - b04) / (b03 + b04)


def compute_bi(b02, b03, b04):
    return np.sqrt(b02 ** 2 + b03 ** 2 + b04 ** 2)


# masks
def mask_rgb(b02, b03, b04):
    # rescale values
    b02 = b02 / b02.max() * 255
    b03 = b03 / b03.max() * 255
    b04 = b04 / b04.max() * 255

    mask_b02 = (b02 >= 120) & (b02 <= 180)
    mask_b03 = (b03 >= 140) & (b03 <= 190)
    mask_b04 = (b04 >= 170) & (b04 <= 220)
    mask = mask_b02 & mask_b03 & mask_b04
    return mask.astype(np.uint8)


def mask_ndvi(b04, b08):
    ndvi_values = compute_ndvi(b04, b08)
    mask = (ndvi_values >= -0.15) & (ndvi_values <= 0.25)
    return mask.astype(np.uint8)


def mask_ndwi(b03, b08):
    ndwi_values = compute_ndwi(b03, b08)
    mask = (ndwi_values >= -0.25) & (ndwi_values <= 0.25)
    return mask.astype(np.uint8)


def mask_arvi(b02, b04, b08):
    arvi_values = compute_arvi(b02, b04, b08)
    mask = (arvi_values >= -0.2) & (arvi_values <= 0.2)
    return mask.astype(np.uint8)


def mask_evi2(b04, b08):
    evi2_values = compute_evi2(b04, b08)
    mask = (evi2_values >= 0.0) & (evi2_values <= 0.2)
    return mask.astype(np.uint8)


def mask_msi(b04, b08):
    msi_values = compute_msi(b04, b08)
    mask = (msi_values >= 0.6) & (msi_values <= 1.5)
    return mask.astype(np.uint8)


def mask_ngrdi(b03, b04):
    ngrdi_values = compute_ngrdi(b03, b04)
    mask = (ngrdi_values >= -0.1) & (ngrdi_values <= 0.0)
    return mask.astype(np.uint8)


def mask_bi(b02, b03, b04):
    bi_values = compute_bi(b02, b03, b04)
    mask = (bi_values >= 200) & (bi_values <= 350)
    return mask.astype(np.uint8)


def final_mask(b02, b03, b04, b08):
    mask = (
            mask_rgb(b02, b03, b04)
            & mask_ndvi(b03, b08)
            & mask_arvi(b02, b04, b08)
            & mask_evi2(b04, b08)
            & mask_msi(b04, b08)
            & mask_ngrdi(b03, b04)
            & mask_bi(b02, b03, b04)
    )
    return mask


def save_mask(mask, filename, reference_file):
    with rasterio.open(reference_file) as src:
        profile = src.profile
        profile.update(
            driver='GTiff',  # Explicitly set the driver to GeoTIFF
            dtype=rasterio.uint8,
            count=1
        )

        with rasterio.open(
                filename,
                'w',
                driver='GTiff',  # Ensure GeoTIFF format
                height=profile['height'],
                width=profile['width'],
                count=1,
                dtype=rasterio.uint8,
                crs=profile['crs'],
                transform=profile['transform']
        ) as dst:
            dst.write(mask.astype(np.uint8), 1)


def load_bands():
    with rasterio.open(config.B02_FILE) as b02, \
            rasterio.open(config.B03_FILE) as b03, \
            rasterio.open(config.B04_FILE) as b04, \
            rasterio.open(config.B08_FILE) as b08:
        return b02.read(1), b03.read(1), b04.read(1), b08.read(1)


b02, b03, b04, b08 = load_bands()
# Compute masks
mask_rgb_res = mask_rgb(b02, b03, b04)
mask_ndvi_res = mask_ndvi(b03, b08)
mask_arvi_res = mask_arvi(b02, b04, b08)
mask_evi2_res = mask_evi2(b04, b08)
mask_msi_res = mask_msi(b04, b08)
mask_ngrdi_res = mask_ngrdi(b03, b04)
mask_bi_res = mask_bi(b02, b03, b04)
final_mask_res = final_mask(b02, b03, b04, b08)

os.makedirs(config.FEATURES_FOLDER, exist_ok=True)

# Save individual masks
save_mask(mask_rgb_res, os.path.join(config.FEATURES_FOLDER, "mask_rgb.tif"), config.B02_FILE)
save_mask(mask_ndvi_res, os.path.join(config.FEATURES_FOLDER, "mask_ndvi.tif"), config.B02_FILE)
save_mask(mask_arvi_res, os.path.join(config.FEATURES_FOLDER, "mask_arvi.tif"), config.B02_FILE)
save_mask(mask_evi2_res, os.path.join(config.FEATURES_FOLDER, "mask_evi2.tif"), config.B02_FILE)
save_mask(mask_msi_res, os.path.join(config.FEATURES_FOLDER, "mask_msi.tif"), config.B02_FILE)
save_mask(mask_ngrdi_res, os.path.join(config.FEATURES_FOLDER, "mask_ngrdi.tif"), config.B02_FILE)
save_mask(mask_bi_res, os.path.join(config.FEATURES_FOLDER, "mask_bi.tif"), config.B02_FILE)
save_mask(final_mask_res, os.path.join(config.FEATURES_FOLDER, "final_mask.tif"), config.B02_FILE)
