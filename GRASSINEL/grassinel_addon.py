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
#% type: integer
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
#%flag
#% key: f
#% description: Terrain flattening
#% guisection: PyroSAR Settings
#%end
#%flag
#% key: n
#% description: Remove thermal noise from Sentinel-1 Scene
#% guisection: PyroSAR Settings
#%end
#%flag
#% key: i
#% description: Import processed Sentinel-1 Data in current GRASS location
#% guisection: Import Settings
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
import glob
import ntpath
from grass.script import parser
from GRASSINEL.S1_preprocessing import *


# Function for splitting paths and extracting filenames
def filenames(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def main(options, flags):
    # flag for enabling/disabling terrain flattening
    flag_f = flags["f"]
    if flag_f:
        terr_f_bool = True
    else:
        terr_f_bool = False
    # flag for enabling/disabling thermal noise removal
    flag_n = flags["n"]
    if flag_n:
        noise_bool = True
    else:
        noise_bool = False
    # pyroSAR Processing
    pyroSAR_processing(down_path=options["raster"], processed_path=options["output"], target_resolution=options["res"],
                       target_CRS=options["crs"], terrain_flat_bool=terr_f_bool,
                       remove_therm_noise_bool=noise_bool)

    # flag for enabling overwriting
    flag_o = flags["o"]
    if flag_o:
        overwrite_bool = True
    else:
        overwrite_bool = False
    # flag for enabling of the import functionality
    flag_i = flags["i"]
    # import of processed sentinel-1 scenes in the GRASS location
    if flag_i:
        file_list = [f for f in glob.glob(options["output"]+"/*.tif")]
        for j, tifs in enumerate(file_list):
            filename = filenames(tifs)
            Module("r.in.gdal",
                   input=tifs,
                   output=filename + "__processed",
                   memory=options["memory"],
                   offset=0,
                   num_digits=0,
                   overwrite=overwrite_bool)


if __name__ == "__main__":
    options, flags = parser()
    sys.exit(main(options, flags))
