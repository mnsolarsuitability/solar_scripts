#!/usr/bin/env python

# Usage: C:\Users\geodesign>C:\Python27\ArcGIS10.2\python.exe Y:\solar_scripts\exportSolarByCounty.py C:\Users\geodesign\Desktop\tmp ('Watonwan','Ramsey') both

import os,subprocess
import glob,dbconn,dbconn_quick
import os.path
from config import *
import shutil, sys


solardir = r'\\files.umn.edu\US\GIS\U-Spatial\SolarResourceData\MN_Solar\Solar_Tiles'
#demdir = r'\\files.umn.edu\US\GIS\U-Spatial\SolarResourceData\MN_DSM\MN_DSM_Tiles'

destdir = r'\\files.umn.edu\US\GIS\U-Spatial\SolarResourceData\MN_Solar\q250k'

######################################################

extensions = [
        '.img',
        '.img.aux.xml',
        '.rrd',
        '.img.xml'
        ]

#os.makedirs(solardir + r'\mytestdir')
#import pdb; pdb.set_trace()

# Loop through each directory
for dirname in glob.glob(solardir + "\\*"):
    print "Processing " + dirname

    dirno = dirname.replace(solardir + "\\",'')

    # Loop through each unique set of .img and related files
    updatewhere = []
    for img in glob.glob(dirname + '\\*.img'):
        imgnumber = img.replace(dirname + '\\','').replace('.img','')
        
        # 1) Query source lidar tile that centroid of solar tile falls within
        q = """
            SELECT l.tile,l.q250k FROM sa_fishnets s,lidar_bbox l
            WHERE ST_WITHIN(ST_CENTROID(s.the_geom),l.the_geom) AND s.id=""" + imgnumber + """
        """
    
        t = dbconn.run_query(q)
        rec = t.fetchone()
        if rec == None:
            print "Centroid does not fall in a lidar tile"

            # 2) Centroid not in laz tile so next query first tile that intersects solar tile
            q = """
                SELECT l.tile,l.q250k FROM sa_fishnets s,lidar_bbox l
                WHERE ST_INTERSECTS(s.the_geom,l.the_geom) AND s.id=""" + imgnumber + """
            """
            t = dbconn.run_query(q)
            rec = t.fetchone()
            if rec == None:

                # 3) Finally, catch stray tiles by querying the nearest laz tile if none intersect (there was a handful of these due to how we created the solar fishnet)
                q = """
                    SELECT l.tile,l.q250k FROM sa_fishnets s,lidar_bbox l
                    WHERE ST_INTERSECTS(ST_BUFFER(s.the_geom,500),l.the_geom) AND s.id=""" + imgnumber + """
                """
                t = dbconn.run_query(q)
                rec = t.fetchone()

        if rec == None:
            # Handle errors (there were none when I ran this)
            qq = """
                UPDATE sa_fishnets SET 
                solarfile = 'error'
                WHERE id = """ + imgnumber
            try:
                t = dbconn.run_query(qq)
                print 'SUCCESS', qq
            except:
                print 'FAILURE'
        else:
            print rec
        
            fn = str(rec['tile']) + "_" + dirno + "_" + imgnumber

            if not os.path.exists(destdir + "\\q" + str(rec['q250k'])):
                os.mkdir(destdir + "\\q" + str(rec['q250k']))

            for ext in extensions:
                srcfile = solardir + "\\" + dirno + "\\" + imgnumber + ext
                dstfile = "q" + str(rec['q250k']) + "\\" + fn + ext
                    
                try:
                    print srcfile
                    print destdir + "\\" + dstfile
                    shutil.copy2(srcfile, destdir + "\\" + dstfile)
                    print

                    # 4) Write the filename, q250k index, and path back to the database
                    qq = """
                    UPDATE sa_fishnets SET 
                    filename = '""" + fn + """.img',
                    q250k = '""" + str(rec['q250k']) + """',
                    solarfile = '""" + dstfile + """'
                    WHERE id = """ + imgnumber
                    try:
                        t = dbconn.run_query(qq)
                        print 'SUCCESS', qq
                    except:
                        print 'FAILURE'
                except:
                    pass
