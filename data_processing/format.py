import netCDF4 as nc
import os
import datetime
import numpy as np

path_to_nc = '/Users/rchales/data/spatialdata/jhudata'

# open a netcdf to copy
nc_to_copy = nc.Dataset(os.path.join(path_to_nc, 'Shigella_Probability_2018_Jan.nc'))

# create new netcdf
new_nc = nc.Dataset(os.path.join(path_to_nc, 'Shigella_2018.nc4'), mode='w')

# create lat
new_nc.createDimension('lat', nc_to_copy['latitude'].size)
new_nc.createVariable('lat', 'f', ('lat', ))
new_nc['lat'][:] = nc_to_copy['latitude'][:]

# create lon
new_nc.createDimension('lon', nc_to_copy['longitude'].size)
new_nc.createVariable('lon', 'f', ('lon', ))
new_nc['lon'][:] = nc_to_copy['longitude'][:]

# finished copying from template file
nc_to_copy.close()

# create time
new_nc.createDimension('time', 12)
new_nc.createVariable('time', 'i', ('time', ))
new_nc['time'].units = 'seconds since 1970-01-01 00:00:00'
new_nc['time'][:] = [
    int(datetime.datetime(year=2018, month=i, day=1, hour=0, minute=0, second=0).timestamp()) for i in range(1, 13)
]

# create probability
new_nc.createVariable('probability', 'f', ('time', 'lat', 'lon', ), fill_value=-9999)
array_to_copy = []
for month in ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', ):
    nc_to_copy = nc.Dataset(os.path.join(path_to_nc, f'Shigella_Probability_2018_{month}.nc'))
    array_to_copy.append(nc_to_copy[month][:])
    nc_to_copy.close()
array_to_copy = np.array(array_to_copy)
array_to_copy[array_to_copy < -1000] = np.nan
new_nc['probability'][:] = array_to_copy
new_nc.sync()

# create symptomatic
new_nc.createVariable('sympt', 'f', ('lat', 'lon', ), fill_value=-9999)
nc_to_copy = nc.Dataset(os.path.join(path_to_nc, 'Shigella_Probability_LTM_Symptomatic.nc'))
array_to_copy = nc_to_copy['Symptomatic'][:]
array_to_copy[array_to_copy < -1000] = np.nan
new_nc['sympt'][:] = array_to_copy
nc_to_copy.close()
new_nc.sync()

# create asymptomatic
new_nc.createVariable('asympt', 'f', ('lat', 'lon', ), fill_value=-9999)
nc_to_copy = nc.Dataset(os.path.join(path_to_nc, 'Shigella_Probability_LTM_Asymptomatic.nc'))
array_to_copy = nc_to_copy['Asymptomatic'][:]
array_to_copy[array_to_copy < -1000] = np.nan
new_nc['asympt'][:] = array_to_copy
nc_to_copy.close()
new_nc.sync()

new_nc.close()
