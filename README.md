# Parrot Sequoia image sorting
Program to sort the Parrot Sequoia images. Created by Gert Sterenborg.
Works for Parrot Sequoia version 1.2.0 (The sensor can be updated at: https://community.parrot.com/t5/Sequoia-Knowledge-Base/Software-Update-Process/ta-p/137709)
This project is in no way related to the products and services of Pix4D, Parrot or Micasense.

## Introduction
The Pix4D software has some set of requirements to be able to work with the Parrot Sequoia images in order to work propperly:
- Pix4D requires images to have a GPS-location. 
- The software can not process RGB images and multispectral images at the same time. 
- To generate indices, the software needs data from the sunshine sensor.

In my case, sometimes this data was not attached to all of the images. Thefefore I created this script to separate useable and not useable images.

## How to use
This script is only tested on macOS, but should work on Linux and Windows as well.
- Make sure you have python installed on your computer (on macOS and Linux Python is usually already present)
- Make sure you have pip installed, by opening the command line and use ```pip -V```, if you see no error, it is present.
- Install exifread, to be able to read data attached to the images. use ```pip install exifread```
- Download the script from this repository (the sequoia-sort.py file) put it somewhere on your computer.
- Make a copy of your images (to make sure that no images are going to be lost)
- In your Terminal/command line go to the folder where your images are stored by using ```cd /path/to/your/images/```
- Execute the script by: ```python /path/to/sequoia-sort.py```

Now it will create two folders in the images directory: msp and rgb. In the msp folder are the multispectral images wich are useable by Pix4D software. In the rgb folder are the JPG images with a geo-location. Invalid images stay in the original folder.
