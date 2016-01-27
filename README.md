# raspicam_servo

Project for the raspi camera to move in two dimensions.
Controlled via a web interface.

## Command run
```
./motion -c motion-mmalcam-both.conf
python web_server.py
```

## Pictures


## Wiring


## Requirements
### Raspberry
* Raspian
* Python (flask, smbus, json)
* Motion-mmal [Install guide](https://rhasbury.wordpress.com/2015/12/23/raspberry-pi-b-with-camera-module-and-motion/)

### Arduino
* Code reading orders from the Rasberry and controlling servos [Here on codebender] (https://codebender.cc/sketch:145093)

### 3D Printing
* [Thingiverse project](http://www.thingiverse.com/thing:504196) (I made some minor adjustement, reinforcement of certain parts)
