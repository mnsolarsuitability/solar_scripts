#!/usr/bin/env python

# Usage: C:\Users\geodesign>C:\Python27\ArcGIS10.2\python.exe Y:\solar_scripts\exportSolarByCounty.py C:\Users\geodesign\Desktop\tmp ('Watonwan','Ramsey') both

import os,subprocess
import glob,dbconn_quick,dbconn
import os.path
from config import *
import shutil, sys


###### SETUP THESE PARAMETERS ACCORDINGLY ############
#solardir = 'P:\\MN_Solar\\Solar_Tiles\\'
solardir = r'\\files.umn.edu\US\GIS\U-Spatial\SolarResourceData\MN_Solar'
demdir = r'\\files.umn.edu\US\GIS\U-Spatial\SolarResourceData\MN_DSM\MN_DSM_Tiles'

destdir = r'\\files.umn.edu\US\GIS\U-Spatial\SolarResourceData\MN_DSM\q250k'

######################################################

#os.makedirs(solardir + r'\mytestdir')

for img in glob.glob(demdir + '\\*.img'):
    imgnumber = img.replace(demdir + '\\','').replace('.img','')
    print
    print imgnumber

    q = """
            SELECT l.lasfile FROM dem_fishnets d,lidar_bbox l WHERE ST_WITHIN(ST_CENTROID(d.the_geom),l.the_geom) AND d.id=""" + imgnumber + """
        """
    t = dbconn.run_query(q)
    for s in t:
        demno = str(s['lasfile'])
        print s

        if s == None:
            break
