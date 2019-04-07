#!/bin/sh

# c = C header file, sql = SQL script
FORMAT="c"
# Use h for C headers, or sql for SQL
SUFFIX="h"

N="ngc.${SUFFIX}"
I="ic.${SUFFIX}"
S="stars.${SUFFIX}"
M="messier.${SUFFIX}"
C="caldwell.${SUFFIX}"
H="herschel.${SUFFIX}"
# This file is used only when the format is C
CONST="constants.${SUFFIX}"

FILES="$N $I $S $M $C $H $CONST"

# Cleanup the files
for F in $FILES
do
  rm -f $F
done

# Run the extract
# Stars
./stars.py 3.85 $FORMAT
# Messier
./dso.py M  100 $FORMAT
# Caldwell
./dso.py C  100 $FORMAT
# Herschel
./dso.py H  100 $FORMAT

#./dso.py NGC 100 $FORMAT
#./dso.py IC  100 $FORMAT
