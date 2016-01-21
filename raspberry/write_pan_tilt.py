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
  old_x = 90
  old_y = 90
  handle_pos = open('lock_pos_file', 'a')
  fcntl.flock(handle_pos.fileno(), fcntl.LOCK_EX)
  with open('static/pos.json', 'r') as f:
    data = json.load(f)
    old_x = data.get('x', 90)
    old_y = data.get('y', 90)
  handle_pos.close()
  print old_x, old_y

  if pan and int(pan) >= lower_bound and int(pan) <= upper_bound:
    old_x = 180 - int(pan)
    handle = open('lock_servo', 'a')
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
    time.sleep(0.1)
    writeNumber(200)
    time.sleep(0.1)
    writeNumber(int(pan))
    handle.close()
    print 'pan "', pan
  if tilt and int(tilt) >= lower_bound and int(tilt) <= upper_bound:
    old_y = 180 - int(tilt)
    handle = open('lock_servo', 'a')
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
    time.sleep(0.1)
    writeNumber(210)
    time.sleep(0.1)
    writeNumber(int(tilt))
    handle.close()
    print 'tilt "', tilt

  handle_pos = open('lock_pos_file', 'a')
  fcntl.flock(handle_pos.fileno(), fcntl.LOCK_EX)
  with open('static/pos.json', 'w') as f:
    data = {'x': old_x, 'y': old_y}
    json.dump(data, f)
  handle_pos.close()


if __name__ == "__main__":
  main(sys.argv[1:])
