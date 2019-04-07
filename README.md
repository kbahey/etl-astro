# Extract/Transform/Load for Astronomical Catalogs

This is a set of Python programs that are used as Extract/Transform/Load (ETL) tools
to create high precision astronomical catalogs from inclusion in planetarium programs,
firmware for telescope controllers, ...etc. 

# Stars:
  Can extract stars up to a certain magnitude.
  Data includes the Constellation, Bayer designation (Greek letter),
  Right Ascension, Declination (both J2000), magnitude, and common name.

# Messier:
  All 109 objects are included.
  The identity of M102 is uncertain and therefore not included. See more [here](http://www.messier.seds.org/m/m102d.html) and [here](https://en.wikipedia.org/wiki/Messier_102)

# Caldwell Objects:
  All 109 objects are included.

# Herschel 400
  All objects are effectively included (398 out of 400 objects)

  Two objects are 'missing', but they are actually included under a different number:
    NGC 2372 is the same object as 2371, which is already in the catalog
    NGC 6885 is the same object as 6882, which is already in the catalog

  Ten other objects were replaced by what they are duplicates of, per the OpenNGC database.
    NGC  651 Duplicate of 650
    NGC 2244 Duplicate of 2239
    NGC 2527 Duplicate of 2520
    NGC 3190 Duplicate of 3189
    NGC 3384 Duplicate of 3371
    NGC 3912 Duplicate of 3899
    NGC 4665 Duplicate of 4624
    NGC 5364 Duplicate of 5317
    NGC 5907 Duplicate of 5906
    NGC 7296 Duplicate of 7295

# Output Formats
  The output will be to one or more files. The file name is the catalog (e.g. messier, ngc, ...),
  and with an extension that depends on the format used.

  Currently, there are two output formats

  c = For C header format, where the catalog will be stored in a struct. The extension is '.h'.
      This was used for the [OnStep Telescope Controller Smart Hand Controller](https://github.com/hjd1964/OnStep/blob/Alpha/addons/St4Serial/SmartHandController/Catalog.cpp), and the
      goal was to provide precise coordinates in a reduced storage space. Note that there is
      a constants.h file generated that contains #defines that can be used by other C files.
      This file must be included in your C source program, to avoid repeating the number of
      items in the catalog, and fully automate the process of extraction.

  sql = For outputing SQL scripts that can be used to populate a database. The extension is '.sql'.

# Requirements
  You need Python 3.x to run these programs

# Installation
  Clone or download this respository

  Then, in the same directory, do the following:
  - Download the OpenNGC data from Github to the directory ./OpenNGC
  - Download the stars.data file from KStars to the directory ./kstars

# How To Run
  1. To extract stars up to magnitude 3.85, and in C header format, use:

    python3 stars.py 3.85 c

  2. To extract all Messier objects, in C header format, use:
  
    python3 dso.py 100 c 
    
  3. To extract all Stars, Messier, Caldwell and Herschel objects, you can run the following script:

     ./extract.sh

  On Windows, you can run the individual scripts that are in the above shell script, or create
  an equivalent .BAT file. 

# Known Issues
  The NGC and IC catalogs have some object IDs that contain non-numeric characters (e.g. 3333A). These
  cause issues for the current C header format used in OnStep's Smart Hand Controller, because the object
  ID is stored as a long data type. Therefore, at present, attempting to extract the NGC or IC catalogs
  will result in the program aborting with a data conversion error. 

# Data Sources
  The extraction programs use the following data sources:
  - [OpenNGC](https://github.com/mattiaverga/OpenNGC) for the Messier and Herschel catalogs.
  - [KStars](https://git.launchpad.net/kstars-bleeding/plain/kstars/data/stars.dat) for bright alignment stars.
