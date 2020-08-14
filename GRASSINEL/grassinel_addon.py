#!/usr/bin/env python3
#
##############################################################################
#
# MODULE:       grassinel_addon
#
# AUTHOR(S):    Patrick Fischer, Marlin Müller, Jonas Ziemer
#
# PURPOSE:      Preprocessing of downloaded Sentinel-1 Scenes with PyroSAR (Copyright by John Truckenbrodt).
#
#
# DATE:         Thursday Aug  13 13:15:00 2020
#
##############################################################################

#%module
#% description: Preprocessing of downloaded Sentinel-1 Data with pyroSAR (Copyright by John Truckenbrodt)
#%end
#%option G_OPT_M_DIR
#% key: raster
#% description: Folder of unprocessed Sentinel-1 Data
#%end
#%option G_OPT_M_DIR
#% key: output
#% description: Folder for the processed Sentinel-1 Data to be stored
#%end
#%option
#% key: res
#% type: string
#% label: Target Resolution
#% description: Target Resolution
#% answer: 50
#% required: yes
#%end
#%option
#% key: crs
#% type: string
#% label: Target coordinate system in EPSG
#% description: Target CRS
#% answer: 32632
#% required: yes
#%end
#%option
#% key: t_flat
#% type: string
#% label: Terrain flattening ("FALSE" to disable or "TRUE" to enable)
#% description: terrain flattening
#% answer: FALSE
#% required: yes
#%end
#%option
#% key: noise
#% type: string
#% label: Thermal Noise Removal ("FALSE" to disable or "TRUE" to enable)
#% description: Thermal Noise Removal
#% answer: FALSE
#% required: yes
#%end
#%option G_OPT_R_OUTPUT
#% key: out_name
#%end
#%flag
#% key: o
#% description: Override projection check (use current location's projection)
#% guisection: Import Settings
#%end
#%option
#% key: memory
#% type: integer
#% multiple: no
#% label: Maximum memory to be used (in MB)
#% description: Cache size for raster rows
#% answer: 500
#% guisection: Import Settings
#%end


import sys

from grass.script import parser
from GRASSINEL.S1_preprocessing import *
from GRASSINEL.support_functions import *


def main(options, flags):
    pyroSAR_processing(down_path=options["raster"], processed_path=options["output"], target_resolution=options["res"],
                       target_CRS=options["crs"], terrain_flat_bool=options["t_flat"],
                       remove_therm_noise_bool=options["noise"])

    flag_o = flags['o']
    if flag_o:
        overwrite_bool = True
    else:
        overwrite_bool = False

    file_list = extract_files_to_list(path_to_folder=options["output"], datatype=".tif")
    for i, tifs in enumerate(file_list):
        print(tifs)
        Module("r.in.gdal",
               input=tifs,
               output=options["out_name"] + str(i),
               memory=options["memory"],
               offset=0,
               num_digits=0,
               overwrite=overwrite_bool)


if __name__ == "__main__":
    options, flags = parser()
    sys.exit(main(options, flags))
