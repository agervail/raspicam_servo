#!/usr/bin/python

import sys
import smbus
import time
import picamera
from PIL import Image
import math

bus = smbus.SMBus(1)
# This is the address we setup in the Arduino Program
address = 0x04

def writeNumber(value):
  bus.write_byte(address, value)
  return -1

def writeServoPos(pan=None, tilt=None):
  if pan:
    time.sleep(0.1)
    writeNumber(200)
    time.sleep(0.1)
    writeNumber(int(pan))
    print 'pan "', pan
  if tilt:
    time.sleep(0.1)
    writeNumber(210)
    time.sleep(0.1)
    writeNumber(int(tilt))
    print 'tilt "', tilt

def detectLaser(imgName):
  print 'open'
  im = Image.open(imgName)
  box = (986,672,1606,972)
  region = im.crop(box)
  print 'loading'
  pix = region.load()
  width, height = (2592,1944)
  boxWidth, boxHeight = (620,300)

  xSum = 0
  totalNum = 0
  print 'loop'
  for x in range(boxWidth):
    for y in range(boxHeight):
      if pix[x,y][0] >= 220:
        xSum += x
        totalNum += 1.
  if totalNum == 0:
    return 0
  cx = xSum / float(totalNum) + box[0]
  print 'cx', cx
  return cx / float(width) * 2 - 1

def findDistance(imgName):
  raspicamFov = math.radians(53.5)
  laserAngle = math.radians(86.73)
  laserDistToCam = 8
  x = detectLaser(imgName)
  alpha = math.pi / 2.0 - math.asin(x) * raspicamFov / 2.0
  c = math.radians(180) - alpha
  a = math.radians(180) - laserAngle - c
  dist = laserDistToCam / math.sin(a) * math.sin(c)
  print 'x ', x, 'alpha ', alpha, 'c ', c, 'a ', a
  return dist

def convertDistToXY(x, y, dist):
  pointZ = math.sin(math.radians(y)) * dist
  zHor = math.cos(math.radians(y)) * dist
  pointX = math.cos(math.radians(x)) * zHor
  pointY = math.sin(math.radians(x)) * zHor
  return (pointX, pointY, pointZ)

def main(argv):
  camera = picamera.PiCamera()
  camera.hflip = True
  camera.vflip = True
  camera.ISO = 800
  camera.shutter_speed = 100000
  camera.resolution = (2592,1944)
  lowerBound = 30
  upperBound = 160
  step = 20
  laserMap = []
  for y in range(lowerBound, upperBound, step):
    writeServoPos(tilt=y)
    for x in range(lowerBound, upperBound, step):
      writeServoPos(pan=x)
      imgName = 'pos_x' + str(x) + '_y' + str(y) + '.jpg'
      camera.capture(imgName)
      print 'compute distance'
      dist = findDistance(imgName)
      #dist = 279.11
      print 'end compute distance'
      point = convertDistToXY(x-90, y-90, dist)
      laserMap.append(point)
      print dist

  import json
  with open('out.json','w') as f:
    f.write(json.dumps(laserMap))
  writeServoPos(90,90)

if __name__ == "__main__":
  main(sys.argv[1:])
