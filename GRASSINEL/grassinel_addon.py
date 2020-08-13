#!/usr/bin/env python3
#
##############################################################################
#
# MODULE:       grassinel_addon
#
# AUTHOR(S):    Patrick Fischer, Marlin Müller, Jonas Ziemer
#
# PURPOSE:      Preprocessing of Sentinel-1 Scenes with PyroSAR
#
# DATE:         Thursday Aug  13 13:15:00 2020
#
##############################################################################

#%module
#% description: Preprocessing with PyroSAR
#%end
#%option G_OPT_M_DIR
#% key: raster
#% description: Name of input raster
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
#% label: Target CRS
#% description: Target CRS
#% answer: 32632
#% required: yes
#%end
#%option
#% key: terr_flat
#% type: string
#% label: Terrain flattening ("FALSE" to disable or "TRUE" to enable)
#% description: terrain flattening
#% answer: FALSE
#% required: yes
#%end
#%option
#% key: noise_rem
#% type: string
#% label: Thermal Noise Removal ("FALSE" to disable or "TRUE" to enable)
#% description: Thermal Noise Removal
#% answer: FALSE
#% required: yes
#%end
#%option G_OPT_M_DIR
#% description: Output of the preprocessing
#% key: output
#% type: string
#% description: location of output folder for processed S1-data
#%end

import sys
import os
import atexit

from subprocess import PIPE

from grass.script import parser, parse_key_val
from grass.pygrass.modules import Module
from pyroSAR.snap.util import geocode
from GRASSINEL.S1_preprocessing import *
from GRASSINEL.grass_functionality import *

# def cleanup():
#     Module('g.remove', flags='f', name='region_mask', type='vector')
#     Module('g.remove', flags='f', name='ndvi', type='raster')
#     Module('g.remove', flags='f', name='ndvi_class', type='raster')
#     Module('g.remove', flags='f', name='ndvi_class', type='vector')


def main(options, flags):
    # Module("g.region",
    #        overwrite=True,
    #        vector="jena_boundary",
    #        align=options["raster"])

    # Module("r.info",
    #        map=options["raster"])

    pyroSAR_processing(down_path=options["raster"], processed_path=options["output"], target_resolution=options["res"], target_CRS=options["crs"],
                       terrain_flat_bool=options["terr_flat"], remove_therm_noise_bool=options["noise_rem"])
    # subset_import(overwrite_bool=True, output="raster", polarization_type=["VH", "VV"])
    # geocode(
    #     infile=options["raster"],
    #     outdir="/media/user/2nd_disk/sen_processed_dir",
    #     tr=options["res"],
    #     t_srs=options["crs"],
    #     terrainFlattening=options["terr_flat"],
    #     removeS1ThermalNoise=options["noise_rem"])

        # interval_time = datetime.now()
        # print("file " + str(l + 1) + " of " + str(len(sentinel_file_list) + 1) + " processed in " + str(
        #     interval_time - start_time) + " Hr:min:sec")


if __name__ == "__main__":
    options, flags = parser()
#   atexit.register(cleanup)
    sys.exit(main(options, flags))
