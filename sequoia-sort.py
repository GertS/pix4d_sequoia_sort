# script for putting correct Parrot Sequoia images in a sub-folder.
# tiff images need to have a geolocation and sunshine correction need to be present.
# Created by Gert Sterenborg: gertsterenborg@gmail.com
#
# Never execute this script onto the original images. Always make sure to have a back-up of the images.
# This script may corrupt your images, use with caution.

import os,sys
import optparse
import exifread

class OptionParser (optparse.OptionParser):

    def check_required (self, opt):
        option = self.get_option(opt)

        # Assumes the option's 'default' is set to None!
        if getattr(self.values, option.dest) is None:
            self.error("%s option not supplied" % option)

#================
#image processing
#================

def check_images(options,path,output_rgb,output_msp):
    if options.verbose:
        print "[verbose] processing image: %s" % path
    if path.endswith(".JPG"):
        is_rgb = True
    else:
        is_rgb = False
    file_valid = True
    # print "====================="
    if is_rgb:
        f = open(path, 'rb')
        tags = exifread.process_file(f)
        f.close()
        found_gps_tag = False
        latitude_is_0 = True
        longitude_is_0 = True
        for tag in tags.keys():

            if tag == 'GPS GPSLatitude':
                found_gps_tag = True
                if tags[tag].values[0] != 0:
                    latitude_is_0 = False
            if tag == 'GPS GPSLongitude':
                if tags[tag].values[0] != 0:
                    longitude_is_0 = False

        if (latitude_is_0 and longitude_is_0) or not found_gps_tag:
            file_valid = False
    else:
        sunshine_readings = False
        found_gps_tag = False
        f = open(path,'rb')
        img = str(f.read())
        f.close()
        start_values = img.find("Camera:GPSXYAccuracy")
        end_values = img.find("Camera:GPSZAccuracy")
        if start_values != end_values:
            GPSXYAccuracy = img[start_values+22:end_values-3]
            if int(float(GPSXYAccuracy)) != 0:
                found_gps_tag = True
        start_values = img.find("<Camera:IrradianceList>")
        end_values = img.find("</Camera:IrradianceList>")
        if end_values != start_values:
            IrradianceList = img[start_values+24:end_values-1]
            if len(IrradianceList)>2:
                sunshine_readings = True
        else:
            file_valid = False
        if all([sunshine_readings,found_gps_tag]):
            file_valid = True
    if file_valid:
        filename = os.path.basename(path)
        if is_rgb:
            os.rename(path, rgb_dir + "/" + filename)
        else:
            os.rename(path, msp_dir + "/" + filename)

    elif options.verbose:
        print "[verbose] file invalid:\n%s" % path


#==================
#parse command line
#==================

usage = "usage: %prog [options] "
parser = OptionParser(usage=usage)
parser.add_option("--verbose", dest="verbose", action="store_true", \
        help="print everything in console",default=False)
parser.add_option("-i", "--input", dest="input_dir", action="store", type="string", \
        help="full path of input directory",default=None)
parser.add_option("-o","--output", dest="output_dir", action="store", type="string", \
        help="full path of destination directory",default=None)

(options, args) = parser.parse_args()

if options.input_dir == None:
    options.input_dir = os.getcwd()
if options.output_dir == None:
    options.output_dir = os.getcwd()

if options.verbose:
    print "[verbose] input directory is:\n%s" % options.input_dir
    print "[verbose] output directory is:\n%s" % options.output_dir

if not os.path.isdir(options.input_dir):
    sys.exit( "input directory not found %s" % options.input_dir)
if not os.path.isdir(options.output_dir):
    sys.exit( "output directory not found %s" % options.output_dir)

## prepare output directory
msp_dir = os.path.join(options.output_dir,"msp")
rgb_dir = os.path.join(options.output_dir, "rgb")

if not os.path.isdir(msp_dir):
    os.makedirs(msp_dir)
    print "[verbose] creating multispectral folder"
print "mutlistpectral images directory directory is:\n%s" % msp_dir
if not os.path.isdir(rgb_dir):
    os.makedirs(rgb_dir)
    print "[verbose] creating RGB folder"
print "RGB images directory directory is:\n%s" % msp_dir

for root, dirs, files in os.walk(options.input_dir):
    for file in files:
        if file.endswith(".JPG") or file.endswith(".TIF"):
            check_images(options, os.path.join(root,file),rgb_dir,msp_dir)
print "Process finished"
