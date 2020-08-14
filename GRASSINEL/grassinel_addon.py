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


def filenames(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def main(options, flags):
    pyroSAR_processing(down_path=options["raster"], processed_path=options["output"], target_resolution=options["res"],
                       target_CRS=options["crs"], terrain_flat_bool=options["t_flat"],
                       remove_therm_noise_bool=options["noise"])

    flag_o = flags["o"]
    flag_i = flags["i"]
    if flag_o:
        overwrite_bool = True
    else:
        overwrite_bool = False

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
