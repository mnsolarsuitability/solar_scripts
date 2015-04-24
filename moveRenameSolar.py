#!/usr/bin/env python

# Usage: C:\Users\geodesign>C:\Python27\ArcGIS10.2\python.exe Y:\solar_scripts\exportSolarByCounty.py C:\Users\geodesign\Desktop\tmp ('Watonwan','Ramsey') both

import os,subprocess
import glob,dbconn_quick
import os.path
from config import *
import shutil, sys


###### SETUP THESE PARAMETERS ACCORDINGLY ############
#solardir = 'P:\\MN_Solar\\Solar_Tiles\\'
solardir = r'\\files.umn.edu\US\GIS\U-Spatial\SolarResourceData\MN_Solar'
demdir = 'P:\\MN_DSM\\MN_DSM_Tiles\\'

destdir = "C:\\Users\\geodesign\\Desktop\\tmp\\" # Path to users hard drive

county = "('Watonwan','Ramsey')"  # SQL format list of counties you want
dem_or_solar = "both"  # dsm, solar, both
######################################################

os.makedirs(solardir + r'\mytestdir')

