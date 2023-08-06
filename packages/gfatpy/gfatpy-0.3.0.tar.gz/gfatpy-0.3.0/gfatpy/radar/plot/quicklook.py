from pdb import set_trace
import pathlib
from typing import Literal

import matplotlib
import xarray as xr
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import matplotlib.dates as mdates
from matplotlib.figure import Figure

from gfatpy import DATA_DN
from gfatpy.lidar.utils import LIDAR_INFO, LIDAR_PLOT_INFO
from gfatpy.lidar.utils import signal_to_rcs
from gfatpy.lidar.preprocessing import preprocess
from gfatpy.utils import plot, utils

BoundsType = tuple[float, float] | Literal["auto", "limits"]

def get_norm(
    rcs: np.ndarray,
    scale_bounds: BoundsType,
    color_resolution: int = 128,
) -> tuple[float, float]:

    match scale_bounds:
        case "auto":
            vmin, vmax = 0., rcs.max()*0.6
        case "limits":
            vmin, vmax = rcs.min(), vmax = rcs.max()
        case _:            
            vmin, vmax = scale_bounds            

    return (vmin, vmax)


def apply_labels(ax: matplotlib.axes.Axes, data_array: xr.DataArray) -> None:  # type: ignore
    # TODO: Other titles will later be added with config param
    plot.title1(data_array.name, 2)
    # plot.title2(np.atleast_1d(data_array.time.mean().dt.date.values)[0].isoformat(), 2)
    # plot.title3(
    #     "{} ({:.1f}N, {:.1f}E)".format(
    #         data_array.attrs.get("site_location"),
    #         float(data_array.attrs["geospatial_lat_min"]),
    #         float(data_array.attrs["geospatial_lon_min"]),
    #     ),
    #     2,
    # )

    plot.watermark(ax, zoom=0.6, alpha=0.6)


def apply_gap_size(ax: matplotlib.axes.Axes, data_array) -> None:  # type: ignore
    diff = data_array.time[1:].values - data_array.time[0:-1].values
    gap_size = 2 * int(
        np.ceil(
            np.median(np.median(diff).astype("timedelta64[s]").astype("float") / 60)
        )
    )

    plot.gapsizer(
        ax,
        data_array.time.values.astype("M8[ms]").astype("O"),
        data_array.range.values,
        gap_size,
        "#c7c7c7",
    )

def quicklook_xarray(
    data_array: xr.DataArray,
    /,
    is_rcs: bool = True,
    scale_bounds: BoundsType = "auto",
    # color_resolution: int = 128,
    colormap: str | matplotlib.colors.Colormap = "jet",
) -> tuple[Figure, Axes]:

    if is_rcs:
        rcs = data_array.values
    else:
        rcs = data_array.values * data_array.range.values**2

    fig, ax = plt.subplots(figsize=(15, 5))
    vmin, vmax = get_norm(rcs, scale_bounds)

    q = ax.pcolormesh(
        data_array.time, data_array.range, rcs.T, cmap=colormap, vmin=vmin, vmax=vmax
    )    
    cbar = fig.colorbar(q, label = f'{data_array.attrs['long_name']}', f'{data_array.attrs['units']}')

    cbar.ax.yaxis.set_offset_position('right')
    cbar.update_ticks()    
    q.cmap.set_over("white")  # type: ignore

    ax.set_xlabel(r"Time, $[UTC]$")
    ax.set_ylabel(r"Height, $[km, \, agl]$")
    ax.set_ylim(0)

    apply_gap_size(ax, data_array=data_array)
    apply_labels(ax, data_array=data_array)
    
    return fig, ax
