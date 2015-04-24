#!/usr/bin/env python

# Usage: C:\Users\geodesign>C:\Python27\ArcGIS10.2\python.exe Y:\solar_scripts\exportSolarByCounty.py C:\Users\geodesign\Desktop\tmp ('Watonwan','Ramsey') both

import os,subprocess
import glob,dbconn_quick
import os.path
from config import *
import shutil, sys


###### SETUP THESE PARAMETERS ACCORDINGLY ############
solardir = 'P:\\MN_Solar\\Solar_Tiles\\'
demdir = 'P:\\MN_DSM\\MN_DSM_Tiles\\'

destdir = "C:\\Users\\geodesign\\Desktop\\tmp\\" # Path to users hard drive

county = "('Watonwan','Ramsey')"  # SQL format list of counties you want
dem_or_solar = "both"  # dsm, solar, both
######################################################


args = False # ignore

if(len(sys.argv) < 4 and args):
    print "Usage is exportSolarByCounty <destination_path> <SQL list of counties e.g. ('Watonwan','Ramsey')> <dsm or solar or both>"
else:

    #destdir = sys.argv[1]
    #county = sys.argv[2]
    #dem_or_solar = sys.argv[3]

    county_to_demid = "SELECT countyname AS county, d.id AS demid FROM county c, dem_fishnets d WHERE ST_INTERSECTS(c.the_geom,d.the_geom) AND c.countyname IN " + county + " ORDER BY demid ASC"


    countyres = dbconn_quick.run_query(county_to_demid)

    cur_county = ""
    cur_dem = -1
    for county in countyres:

        if cur_county != county['county']:
            print "Working on county: " + county['county']
            cur_county = county['county']

        try: 
            os.makedirs(destdir + county['county'])
            os.makedirs(destdir + county['county'] + '\\Solar')
            os.makedirs(destdir + county['county'] + '\\DSM')
        except OSError as err:
            if err.errno != 17:
                raise

        try:
            os.makedirs(destdir + county['county'] + '\\Solar\\' + str(county['demid']))
        except OSError as err:
            if err.errno != 17:
                raise

        if cur_dem != county['demid']:
            print "\tWorking on DEM tile " + str(county['demid'])
            cur_dem = county['demid']
            if dem_or_solar == "dsm" or dem_or_solar == "both":
                try: 
                    shutil.copy2(demdir + str(cur_dem) + '.img', destdir + county['county'] + '\\DSM\\' + str(cur_dem) + '.img')
                except: 
                    print "Unable to copy dsm tile: " + demdir + str(cur_dem) + '.img', destdir + county['county'] + '\\DSM\\' + str(cur_dem) + '.img'
            
        if dem_or_solar == "solar" or dem_or_solar == "both":
            demid_to_said = """
                SELECT s.id FROM dem_fishnets d,sa_fishnets s WHERE ST_WITHIN(s.the_geom,d.the_geom) AND d.id=""" + str(county['demid']) + """
            """

            satileres = dbconn_quick.run_query(demid_to_said)

            for satile in satileres:
                print "\t\t" + str(satile['id']) + '.img'
                q = """
                    SELECT d.id FROM dem_fishnets d,sa_fishnets s WHERE ST_WITHIN(s.the_geom,d.the_geom) AND s.id=""" + str(satile['id']) + """
                """
                t = dbconn_quick.run_query(q)
                for s in t:
                    demno = str(s['id'])
                
                try: 
                    shutil.copy2(solardir + demno + '\\' + str(satile['id']) + '.img', destdir + county['county'] + '\\Solar\\' + demno + '\\' + str(satile['id']) + '.img')
                except: 
                    print "Unable to copy file: " + solardir + demno + '\\' + str(satile['id']) + '.img'

            


