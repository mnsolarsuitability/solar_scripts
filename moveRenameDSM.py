#!/usr/bin/env python
import os,subprocess
import glob,dbconn_quick,dbconn
import os.path
from config import *
import shutil, sys


###### SETUP THESE PARAMETERS ACCORDINGLY ############
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

# Enable debugging:
#import pdb; pdb.set_trace()

# Loop through unique .img files in each directory
for img in glob.glob(demdir + '\\*.img'):
    imgnumber = img.replace(demdir + '\\','').replace('.img','')
    print
    print imgnumber

    # 1) Query source lidar tile that centroid of DSM tile falls within
    q = """
        SELECT l.tile,l.q250k FROM dem_fishnets d,lidar_bbox l WHERE ST_WITHIN(ST_CENTROID(d.the_geom),l.the_geom) AND d.id=""" + imgnumber + """
    """
    
    t = dbconn.run_query(q)
    
    rec = t.fetchone()
    if rec == None:
        print "Centroid does not fall in a lidar tile"

        # 2) Centroid not in laz tile so next query first tile that intersects
        q = """
            SELECT l.tile,l.q250k FROM dem_fishnets d,lidar_bbox l WHERE ST_INTERSECTS(d.the_geom,l.the_geom) AND d.id=""" + imgnumber + """
        """
        t = dbconn.run_query(q)
        rec = t.fetchone()
        print rec

    laz = str(rec['tile']) + " - " + str(rec['q250k'])

    # Create the q250k directory if it doesn't exist yet
    if not os.path.exists(destdir + "\\q" + str(rec['q250k'])):
        os.mkdir(destdir + "\\q" + str(rec['q250k']))

    # 4) Write the filename, q250k index, and path back to the database
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

    for ext in extensions:
        srcfile = demdir + "\\" + imgnumber + ext
        dstfile = destdir + "\\q" + str(rec['q250k']) + "\\" + str(rec['tile']) + "_" + imgnumber + ext
            
        try:
            print srcfile
            print dstfile
            shutil.copy2(srcfile,dstfile)
            print
        except:
            pass
