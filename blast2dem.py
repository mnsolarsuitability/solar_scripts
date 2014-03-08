#
# blast2dem.py
# blast all MN Lidar to DEM
# walz0053@umn.edu
#

import sys, os, subprocess

def check_output(command,console):
    if console == True:
        process = subprocess.Popen(command)
    else:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    output,error = process.communicate()
    returncode = process.poll()
    return returncode,output 

def blast2dem(inlaz,outdem):
    
    ### complete the path to where the LAStools executables are
    lastools_path = r"C:\lastools\bin"

    ### create the full path to the blast2dem executable
    blast2dem_path = lastools_path+"\\blast2dem.exe"

    ### create the command string for blast2dem.exe
    command = ["blast2dem"] #['"'+blast2dem_path+'"']

    ### use '-verbose' option
    command.append("-v")

    ### add input LiDAR
    command.append('-i')
    ##wildcards = sys.argv[c+1].split()
    ##for wildcard in wildcards:
    ##    command.append("-i")
    ##    command.append('"' + sys.argv[c] + "\\" + wildcard + '"')
    #command.append('"' + "C:\\lidar_data\\hennepin\\laz\\test_blast\\q1110\\1110*.laz" + '"')
    command.append('"' + inlaz + '"')

    ### options
    command.append("-merged")
    command.append("-first_only")
    command.append("-elevation")
    command.append("-kill")
    command.append("50")
                   
    ##command.append("-drop_return")
    ##command.append("0")
    ##command.append("1")
    ##command.append("7")
    ##command.append("12")

    command.append("-oimg")

    ### maybe an output file name was selected
    command.append("-o")
    command.append('"'+ outdem +'"')

    ### maybe an output directory was selected
    command.append("-odir")
    command.append('"'+"C:\\lidar_data\\hennepin\\laz\\pyout\\"+'"')


    ### report command string
    print "LAStools command line:"
    command_length = len(command)
    command_string = str(command[0])
    command[0] = command[0].strip('"')
    for i in range(1, command_length):
        command_string = command_string + " " + str(command[i])
        command[i] = command[i].strip('"')
    print command_string

    ### run command
    returncode,output = check_output(command, False)

    ### report output of blast2dem
    print str(output)

    if returncode != 0:
        print "Error. blast2dem failed."
        sys.exit(1)

    print "Success. blast2dem done."



mypath = "F:\\MnLAZ\\"

#print glob.glob("C:\\lidar_data\\hennepin\\laz\\test_blast\\*.laz")

#print next(os.walk("C:\\lidar_data\\hennepin\\laz\\test_blast\\"))[2]


from os import listdir
from os.path import isfile, join
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

print onlyfiles

from os import walk

f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    print dirpath, dirnames
    
    for folder in dirnames:
        lazpath = mypath + folder + "laz\\"
        qnum = folder[1:]
        currfiles = lazpath + qnum + "*.laz"
        print "now blasting: ", currfiles, " to ", qnum+".img"
        #blast2dem(currfiles,qnum+".img")
        break
    
    break
