# Get the format
def get_format(fmt_list = [], fmt = 'c'):
  for row in fmt_list:
    if row[0] == fmt:
      return row[1], row[2]

  return False, ''

# Check if a string can be converted to a number
def is_numeric(s):
  '''returns True if string s is numeric'''
  return all(c in '0123456789.+-' for c in s) and any(c in '0123456789' for c in s)

# Converts a Sexagesimal number to a Decimal number.
# Parameters: HH:MM:SS or DD:MM:SS
# Returns: float, a decimal number
def sexa2float(dms):

  hd, m, s = dms.split(':')
  # Strip spaces
  hd = hd.strip(' ')

  make_negative = False
  if hd[0] == '-':
    make_negative = True
    hd = abs(int(hd))

  r = float(hd) + float(m)/60.0 + float(s)/3600.0

  if make_negative == True:
    r *= -1

  return r

# Convert coordinates
def convert_coord(coord):
  sign = coord[0]
  if sign == '+' or sign == '-':
    c = coord[0:3] + ':' + coord[3:5] + ':' + coord[5:len(coord)]
  else:
    c = coord[0:2] + ':' + coord[2:4] + ':' + coord[4:len(coord)]

  return c, sexa2float(c)

