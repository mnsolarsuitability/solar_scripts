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

extensions = [
        '.img',
        '.img.aux.xml',
        '.rrd',
        '.img.xml'
        ]

#os.makedirs(solardir + r'\mytestdir')
#import pdb; pdb.set_trace()
for img in glob.glob(demdir + '\\*.img'):
    imgnumber = img.replace(demdir + '\\','').replace('.img','')
    print
    print imgnumber
    #imgnumber = '3330'
    q = """
        SELECT l.tile,l.q250k FROM dem_fishnets d,lidar_bbox l WHERE ST_WITHIN(ST_CENTROID(d.the_geom),l.the_geom) AND d.id=""" + imgnumber + """
    """
    
    t = dbconn.run_query(q)
    
    rec = t.fetchone()
    if rec == None:
        print "Centroid does not fall in a lidar tile"

        q = """
            SELECT l.tile,l.q250k FROM dem_fishnets d,lidar_bbox l WHERE ST_INTERSECTS(d.the_geom,l.the_geom) AND d.id=""" + imgnumber + """
        """
        t = dbconn.run_query(q)
        rec = t.fetchone()
        print rec

    laz = str(rec['tile']) + " - " + str(rec['q250k'])

    #if not os.path.exists(destdir + "\\q" + str(rec['q250k'])):
    #    os.mkdir(destdir + "\\q" + str(rec['q250k']))

##    for ext in extensions:
##        srcfile = demdir + "\\" + imgnumber + ext
##        dstfile = destdir + "\\q" + c + "\\" + str(rec['tile']) + "_" + imgnumber + ext
##            
##        try:
##            print srcfile
##            print dstfile
##            shutil.move(srcfile,dstfile)
##            
##            pass

    qq = """
    UPDATE dem_fishnets SET 
    filename = '""" + str(rec['tile']) + "_" + imgnumber + """.img',
    q250k = '""" + str(rec['q250k']) + """'
    WHERE q250k IS NULL and id = """ + imgnumber
    try:
        t = dbconn.run_query(qq)
        print 'SUCCESS', qq
    except:
        print 'FAILURE'
    
    
