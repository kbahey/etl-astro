#!/usr/bin/env python3

import csv
import sys
import operator
import utils
import lookups

fmt_list = [
  ('c',     'h', '  { %2s, %2s, %5s, %9.9s, %9.9s, "%-15s" }, // %s %s, %6.6s, %11.11s, %11.11s, %s'), # C
  ('sql', 'sql', 'INSERT INTO stars VALUES( %2s, %2s, %5s, %9.9s, %9.9s, "%-15s" ); -- %s %s, %6.6s, %11.11s, %11.11s, %s'), # SQL
  ]

preamble = '''// This data is machine generated from the KStars Star database.
// Do NOT edit this data manually. Rather, fix the import programs and rerun.
star_t Cat_Stars[NUM_STARS] = {'''

DATA_FILE = 'kstars/stars.dat'

MAG_MULTIPLIER = 100
RA_MULTIPLIER  = 1
DE_MULTIPLIER  = 1

# This is to generate the code around the data catalog itself. It needs
# to be edited manually after the extract program is run, and the output
# is sorted (by constellation then Bayer designation in case of stars)

if len(sys.argv) != 3:
  print('ERROR: Usage: ' + sys.argv[0] + ' magnitude format')
  sys.exit(1)

MAG_THRESHOLD = float(sys.argv[1])
FORMAT        = sys.argv[2]

suffix, fmt = utils.get_format(fmt_list, FORMAT)

if suffix == False:
  print('ERROR: Unknown format. Use c for C, or sql for SQL')
  sys.exit(1)

total = 0

l = []

with open(DATA_FILE, newline='') as f:
  for row in f:
   
    row = row.strip('\n')

    ra            = row[0:9]
    de            = row[10:20]
    magnitude     = row[45:51]
    bayer         = row[74:77]
    constellation = row[78:81]
    name          = row[83:len(row)]

    first         = row[0]

    # Skip the header line
    if first == '#':
      continue

    # Ignore records with no Bayer designation
    if bayer == '':
      continue

    magnitude = float(magnitude)
    # Only include stars with the magnitude threshold
    if magnitude >= MAG_THRESHOLD:
      continue

    # Multiply the magnitude by a factor, so it can be stored as a signed short int
    mag = int((magnitude) * MAG_MULTIPLIER)

    # Get the Bayer designation, as a char
    ret, bayer_num = lookups.get_bayer(bayer)
    if ret == False:
      continue

    # Get the DD:MM:SS or HH:MM:SS, as well as the float representation of the RA and DE
    ra_s, ra_f = utils.convert_coord(ra)
    de_s, de_f = utils.convert_coord(de)

    # Increment the counter
    total = total + 1 

    const_num = lookups.get_constellation(constellation)
    l.append(
       (
        const_num,
        bayer_num,
        mag,
        # Arduino's precision is 6 digits total, so we round to 4 places
        str(round(ra_f, 4)),
        str(round(de_f, 4)),
        name[:15], 

        bayer,
        constellation,
        magnitude,
        ra_s,
        de_s,
        name,
      )
    )

f.close()

# Sort the list by Constellation, then Bayer designation
l.sort(key = operator.itemgetter(0,1))
total = len(l)

f = open('stars.' + suffix, 'w')

if FORMAT == 'c':
  f.write(preamble + '\n')

# Write the sorted list to the file
for row in l:
  s = fmt % (
    row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])

  f.write(s + '\n')

if FORMAT == 'c':
  f.write('};\n')

f.close()

# We are done, append the count
if FORMAT == 'c':
  f = open('constants.h', 'a')
  f.write('#define NUM_STARS ' + str(total) + '\n')
  f.close()
