import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import DriftMLP.plotting.general as gtplot
import cartopy.crs as ccrs
import matplotlib as mpl


def ll_to_180(z):
    if z > 180:
        return z+(-360)
    elif z > 360:
        return ll_to_180(z+(-360))
    else:
        return z


f_name = '/home/omalley3/Downloads/drifter_annualmeans.nc'
vel_arrays = xr.open_dataset(f_name)
vel_arrays['longitude'] = vel_arrays['Lon']
vel_arrays['latitude'] = vel_arrays['Lat']
vel_arrays.transpose('longitude', 'latitude')
vel_arrays['mag'] = np.sqrt(
    np.square(vel_arrays['U'])+np.square(vel_arrays['V']))
vel_arrays['mag'].attrs['long_name'] = 'Velocity Magnitude (m/s)'


def langeroff_arrows(data_array, lon_range=[-50, 20], lat_range=[-50, 0],
                     res=[10, 5], *args, **kwargs):

    lon_linspace = np.arange(lon_range[0], lon_range[1], res[0])
    lat_linspace = np.arange(lat_range[0], lat_range[1], res[1])
    #data_interp = data_array.sel(longitude=slice(lon_range[0], lon_range[1]))
    #data_interp = data_interp.sel(latitude=slice(lat_range[0], lat_range[1]))
    data_interp = data_array.interp(
        longitude=lon_linspace,
        latitude=lat_linspace, method='nearest')

    return data_interp


def cartopy_quiver(data_array, ax):
    X, Y = np.meshgrid(data_array['longitude'].values,
                       data_array['latitude'].values)
    U = data_array['U'].values.T
    V = data_array['V'].values.T
    assert(X.shape == U.shape)
    assert(V.shape == U.shape)
    ax.quiver(X, Y, U, V, transform=ccrs.PlateCarree(), units='dots')


def plot_magnitude(extent, ax, **kwargs):
    filt_arr = vel_arrays.sel(longitude=slice(
        extent[0]-5, extent[1]+5), latitude=slice(extent[2]-5, extent[3]+20))
    return filt_arr['mag'].plot(x='longitude', y='latitude', ax=ax, vmin=0, vmax=1.2, cmap='OrRd', **kwargs)


stations = np.loadtxt("locations.txt", delimiter=',')
stations = pd.DataFrame(stations, index=range(1, stations.shape[0]+1))
stations.columns = ['Longitude', 'Latitude']


res = [3, 3]
fig = plt.figure(figsize=(8, 3.5))
ax = plt.subplot(1, 2, 1, projection=ccrs.PlateCarree())
extent = [-50, 20, -50, 0]
plot_magnitude(extent, ax=ax, add_colorbar=False, rasterized=True)
plot_data = langeroff_arrows(vel_arrays, axes=ax, res=res)
cartopy_quiver(plot_data, ax)
gtplot.plot_stations(stations.iloc[[0, 1, 2]], ax=ax, names=list(range(1, 4)))
# gtplot.add_standard_gridlines(ax)
gl = gtplot.add_standard_gridlines(ax)
gl.left_labels = True
gl.right_labels = False

ax.set_title('South Atlantic')
ax.axis('auto')
ax.set_extent(extent, crs=ccrs.PlateCarree())


ax = plt.subplot(1, 2, 2, projection=ccrs.PlateCarree())
extent = [-95, 10, 0, 50]

plot_magnitude(extent, ax, rasterized=True, add_colorbar=False)
plot_data = langeroff_arrows(vel_arrays, lon_range=[-95, 10],
                             lat_range=[0, 50], axes=ax, res=res)
cartopy_quiver(plot_data, ax)
ax.set_title('North Atlantic')
gtplot.plot_stations(
    stations.iloc[[3, 4, 5, 6]], ax=ax, names=list(range(4, 8)))
gl = gtplot.add_standard_gridlines(ax)
gl.left_labels = True
gl.right_labels = False


ax.axis('auto')
ax.set_extent(extent, crs=ccrs.PlateCarree())

fig.subplots_adjust(right=0.9)
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = mpl.cm.OrRd
cb1 = mpl.colorbar.ColorbarBase(cbar_ax, cmap=cbar,
                                norm=mpl.colors.Normalize(vmin=0, vmax=1.2),
                                orientation='vertical', extend='max')
cb1.set_label('Velocity Magnitude (m/s)')


fig.savefig("Images/locations_laurindo.png", bbox_inches='tight')
fig.savefig("Images/locations_laurindo.pdf", bbox_inches='tight')
