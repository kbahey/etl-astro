#!/usr/bin/env python3
import csv
import sys
import operator
import utils
import lookups

def usage():
  print('ERROR: Usage: ' + sys.argv[0] + ' catalog magnitude format')
  sys.exit(1)

if len(sys.argv) != 4:
  usage()
 
fmt_list = [
  ('c',   'h',   '  { %2.2s, %2.2s, %4s, %5.5s, %8.8s, %8.8s }, // %s %4.4s, %s, %5.5s, %6.6s, %8.8s, %8.8s, %s'),
  ('sql', 'sql', 'INSERT INTO dso VALUES( %2.2s, %2.2s, %4s, %5.5s, %8.8s, %8.8s ); -- %s %4.4s, %s, %5.5s, %6.6s, %8.8s, %8.8s, %s'),
  ]

# This is to generate the code around the data catalog itself. It needs
# to be edited manually after the extract program is run, and the output
# is sorted (by object ID for DSO catalogs
preamble = '''// This data is machine generated from the Open NGC database.
// Do NOT edit this data manually. Rather, fix the import programs and rerun.
dso_t Cat_#NAME#[#NUM#] = {'''

# We extract data from the main NGC file, as well as the addendum for 
# a few Messier and Caldwell objects that don't have NGC numbers
DATA_FILES    = ( 'OpenNGC/NGC.csv', 'OpenNGC/addendum/addendum.csv' )
CATALOG       = sys.argv[1]
MAG_THRESHOLD = sys.argv[2]
FORMAT        = sys.argv[3]

suffix, fmt = utils.get_format(fmt_list, FORMAT)

if suffix == False:
  print('ERROR: Unknown format. Use c for C, or sql for SQL')
  sys.exit(1)

# In order to save storage, we use a multiplier for the magnitude
MAG_MULTIPLIER = 100
RA_MULTIPLIER  = 1
DE_MULTIPLIER  = 1

l = []

if CATALOG == 'H':
  cat_name = 'Herschel'
  file_name = 'herschel.' + suffix
  num  = 'NUM_HERSCHEL'
elif CATALOG == 'M':
  cat_name = 'Messier'
  file_name = 'messier.' + suffix
  num  = 'NUM_MESSIER'
elif CATALOG == 'N':
  cat_name = 'NGC'
  file_name = 'ngc.' + suffix
  num  = 'NUM_NGC'
elif CATALOG == 'I':
  cat_name = 'IC'
  file_name = 'ic.' + suffix
  num  = 'NUM_IC'
elif CATALOG == 'C':
  cat_name = 'Caldwell'
  file_name = 'caldwell.' + suffix
  num = 'NUM_CALDWELL'
else:
  print('ERROR: This program extracts only (M)essier, (H)erschel, (C)aldwell, (NGC), or (IC) objects')
  sys.exit(1)

for FILE in DATA_FILES:
  with open(FILE, newline='') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:

      if CATALOG == 'M':
        obj_id = row[18]
      elif CATALOG == 'NGC' or CATALOG == 'H':
        obj_id = row[19]
      elif CATALOG == 'IC':
        obj_id = row[20]
      elif CATALOG == 'C':
        pass

      name          = row[0]
      obj_type      = row[1]
      ra            = row[2]
      de            = row[3]
      constellation = row[4]
      magnitude     = row[9]

      # Skip the header line
      if name == 'Name':
        continue

      # Skip duplicate objects
      #if obj_type  == 'Dup':
        #continue

      # For Herschel 400, we need to lookup a list
      if CATALOG == 'H':
        obj_id = lookups.herschel(name)
        if obj_id == False:
          # Not in the list, skip the row
          continue
      # For Caldwell, we need to lookup a list
      elif CATALOG == 'C':
        obj_id = lookups.caldwell(name)
        if obj_id == False:
          # Not in the list, skip the row
          continue
      elif CATALOG == 'NGC':
        if CATALOG in name:
          obj_id = name.replace('NGC', '')
        else:
          continue
      elif CATALOG == 'M':
        if obj_id == '':
          continue

      # Make up a fake magnitude for objects that don't have one
      if utils.is_numeric(magnitude) == False:
        magnitude = 99.9

      # Only list objects above a certain threshold
      if float(magnitude) >= float(MAG_THRESHOLD):
        continue

      # All done, create the row
      l.append(
        (
          lookups.get_constellation(constellation),
          lookups.get_obj_type(obj_type),
          int(obj_id),
          round(float(magnitude) * MAG_MULTIPLIER),
          str(round(utils.sexa2float(ra), 4)),
          str(round(utils.sexa2float(de), 4)),

          CATALOG,
          obj_id,
          constellation,
          obj_type,
          magnitude,
          str(ra),
          str(de),
          name,
        )
      )

f.close()

# Sort the list on the 2nd column (Object ID)
l.sort(key = operator.itemgetter(2))

# Get the total number of objects in this catalog
total = len(l)

f = open(file_name, 'w')

if FORMAT == 'c':
  # Now for the defines for number of objects
  pre = preamble.replace('#NAME#', cat_name)
  pre = pre.replace('#NUM#', num)

  f.write(pre + '\n') 

# Write the sorted list to the file
for row in l:
  s = fmt % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13])

  f.write(s + '\n')

if FORMAT == 'c':
  f.write('};\n')

f.close()

if FORMAT == 'c':
  # We are done, append the count to the constants file
  f = open('constants.h', 'a')
  f.write('#define ' + num + ' ' + str(total) + '\n')
  f.close()
