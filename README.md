# GEO450_GRASS
University Project (FSU Jena)

This tool aims to set up a multi-source space-time raster cube for Thuringia using GRASS GIS and further Python libraries. Automated workflows are foreseen including data download, data pre-processing and data processing to set up space-time raster cubes for other regions in the future. Based on Sentinel-1, different tools should enable researchers ans users to conduct time-series analysis. 

The following functionalty should be possible with this tool:
1) Data download based on i.sentinel.download including basic adjustments for Sentinel-1
2) Development of a SAR pre-processing add-on for GRASS GIS based in SNAP via pyroSAR (author: John Truckenbrodt)
3) Creation of a Sentinel-1 space-time cube
4) Analysis: Multitemporal analysis using t.rast.mapcalc or t.rast.algebra
5) Example PyWPS process to make multitemporal analysis available as web service
