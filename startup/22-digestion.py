# author: tmorris@bnl.gov
# June 2023
# as used at ALS


import scipy as sp
import numpy as np

# def get_beam_stats(im):

#     fim = sp.ndimage.median_filter(im, size=5)

#     threshold = 0.5 * (fim.min() + fim.max())

#     mask = fim > threshold

#     ny, nx = fim.shape

#     x, y = np.arange(nx), np.arange(ny)
#     X, Y = np.meshgrid(x, y)

#     x_mean = np.sum(mask * X) / mask.sum()
#     y_mean = np.sum(mask * Y) / mask.sum()

#     x_width =  np.sqrt(np.sum(mask * np.square(X - x_mean)) / mask.sum())
#     y_width =  np.sqrt(np.sum(mask * np.square(Y - y_mean)) / mask.sum())

#     return fim.max() - fim.min(), x_mean, y_mean, x_width, y_width


# def get_beam_stats(im):

#     x_min, x_max, y_min, y_max, sep = bloptools.utils.get_principal_component_bounds(im - im.mean(), beam_prop=0.5)

#     x_center = 0.5 * (x_min + x_max)
#     y_center = 0.5 * (y_min + y_max)

#     x_width = x_max - x_min
#     y_width = y_max - y_min

#     return im.max() - im.min(), x_center, y_center, x_width, y_width


# def digestion(db, uid):


#     table = db[uid].table(fill=True)

#     product_keys = ["rejected", "image", "peak", "x_center", "y_center", "x_width", "y_width"]
#     products = {key: [] for key in product_keys}

#     for row, entry in table.iterrows():

#         image = entry.basler_cam_image

#         ny, nx = image.shape

#         peak, x_mean, y_mean, x_width, y_width = get_beam_stats(image)

#         bad = False

#         bad |= (peak < 16)
#         bad |= (x_width < 1)
#         bad |= (y_width < 1)

#         OOB_buffer = 1/20

#         products["rejected"].append(bad)
#         products["image"].append(image)
#         products["peak"].append(peak)
#         products["x_center"].append(x_mean)
#         products["y_center"].append(y_mean)
#         products["x_width"].append(x_width)
#         products["y_width"].append(y_width)

#     #products["bend_over_pitch"] = table.m101_bend.values / table.m101_pitch.values

#     return products


print(f"Loading {__file__}")

# digesting photons from the photodiode 
### (may no longer work)
def current_digestion(db, uid):

    table = db[uid].table(fill=True)

    product_keys = ["current"]
    products = {key: [] for key in product_keys}

    for row, entry in table.iterrows():

        bad = False

        if bad:
            [products[key].append(np.nan) for key in product_keys]
            continue

        products["current"].append(entry.beamstop)

    return products



from dataclasses import dataclass


@dataclass
class BeamStats:
    
    x_center = np.nan
    x_width = np.nan
    y_center = np.nan
    y_width = np.nan
    eff_area = np.nan
    max = np.nan
    sum = np.nan
    raw_image = []
    image = []


def get_beam_stats(im, roi=None, threshold=0.2, method="rms", median_filter_size=3, gaussian_filter_sigma=2, downsample=1):

    if roi:
        imin, imax, jmin, jmax = roi
        # cropped image
        cim = im[jmin:jmax, imin:imax]
    else:
        cim = im

    print(cim.shape)

    if downsample > 1:
        cim = cim[::downsample, ::downsample]

    

    cfim = sp.ndimage.median_filter(cim, size=median_filter_size)
    cfim = sp.ndimage.gaussian_filter(cfim, sigma=gaussian_filter_sigma)

    # filtered cropped image
    cfim = np.where(cfim > (1 - threshold) * cfim.min() + threshold * cfim.max(), cfim, 0)

    stats = {}
    stats["raw_image"] = im
    stats["image"] = cfim 
    stats["max"] = cfim.max()
    stats["sum"] = cfim.sum()

    for iax, axis in enumerate(["x", "y"]):

        index = np.arange(cfim.shape[1-iax])
        profile  = cfim.sum(axis=iax)
        profile -= profile.min()
        profile /= profile.max()

        if method == "rms":
            center  = np.sum(profile * index) / np.sum(profile)
            width = 4 * np.sqrt(np.sum(profile * np.square(index - center)) / np.sum(profile))

        elif method == "fwhm":
            beam_index = index[profile > 0.5 * profile.max()]
            center = beam_index.mean()
            width = beam_index.ptp()
        
        elif method == "quantile":
            normed_cumsum = np.cumsum(profile) / np.sum(profile)
            lower, center, upper = np.interp([0.05, 0.5, 0.95], normed_cumsum, index)
            width = upper - lower
        else:
            raise ValueError(f"Invalid method '{method}'.")

        stats[f"center_{axis}"] = center
        stats[f"width_{axis}"] = width


    stats["area"] = (cfim > cfim.max() * threshold).sum()

    stats["eff_area"] = 0.5 * (stats["width_x"]**2 + stats["width_y"]**2)

    # bs = BeamStats(**stats)

    return stats



import matplotlib.pyplot as plt

def test_beam_digestion(image, f, **kwargs):

    stats = f(image, **kwargs)

    plt.imshow(stats["image"], cmap="magma")

    x0 = stats["center_x"] - 0.5 * stats["width_x"]
    x1 = stats["center_x"] + 0.5 * stats["width_x"]
    y0 = stats["center_y"] - 0.5 * stats["width_y"]
    y1 = stats["center_y"] + 0.5 * stats["width_y"]

    plt.plot([x0,x0,x1,x1,x0], [y0, y1, y1, y0, y0], c="r")



def exposure_digestion(db, uid):

    products = db[uid].table(fill=True)

    for index, entry in products.iterrows():

        roi = [500, 1000, 150, 600]
        stats = get_beam_stats(entry.basler_cam_image, roi=roi, method="rms")
        p99 = np.percentile(stats["image"].astype(float).ravel(), q=99)
        products.loc[index, f"beam_p99"] = p99

    return products



def basler_cam_digestion(db, uid):

    products = db[uid].table(fill=True)

    for index, entry in products.iterrows():

        bad = False

        roi = [500, 1000, 150, 600]
        roi = None

        stats = get_beam_stats(entry.basler_cam_image, roi=[4000, 5400, 1500, 2500], method="rms", downsample=2, threshold=0.25)

        for attr in ["center_x", "width_x", "center_y", "width_y", "eff_area", "area", "sum", "max"]:
            products.loc[index,f"beam_{attr}"] = stats[attr] if not bad else np.nan

    return products
