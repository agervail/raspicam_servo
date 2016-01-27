#!/usr/bin/python

import sys, getopt
import smbus
import time
import fcntl
import json

bus = smbus.SMBus(1)
# This is the address we setup in the Arduino Program
address = 0x04

def writeNumber(value):
  bus.write_byte(address, value)
  return -1

def main(argv):
  pan = ''
  tilt = ''
  try:
    opts, args = getopt.getopt(argv,"hp:t:",["pan=","tilt="])
  except getopt.GetoptError:
    print 'write_pan_tilt.py --pan <pan_value> --tilt <tilt_value>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'write_pan_tilt.py --pan <pan_value> --tilt <tilt_value>'
      sys.exit()
    elif opt in ("-p", "--pan"):
      pan = arg
    elif opt in ("-t", "--tilt"):
      tilt = arg

  lower_bound = 30
  upper_bound = 150

  if pan and int(pan) >= lower_bound and int(pan) <= upper_bound:
    time.sleep(0.1)
    writeNumber(200)
    time.sleep(0.1)
    writeNumber(int(pan))
    print 'pan "', pan
  if tilt and int(tilt) >= lower_bound and int(tilt) <= upper_bound:
    time.sleep(0.1)
    writeNumber(210)
    time.sleep(0.1)
    writeNumber(int(tilt))
    print 'tilt "', tilt

if __name__ == "__main__":
  main(sys.argv[1:])
