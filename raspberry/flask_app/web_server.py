from flask import Flask, render_template, url_for, request, redirect
import subprocess
import time
app = Flask(__name__)

@app.route("/")
def index():
  return "Hello You"

@app.route("/move_servo")
def move_servo():
  if 'x' in request.args and 'y' in request.args:
    try:
      x = 180 - int(request.args['x'])
      y = 180 - int(request.args['y'])
      subprocess.Popen(["python", "script/write_pan_tilt.py", "-p", str(x), "-t", str(y)])
    except:
      pass
  return redirect(url_for('cam'))

@app.route("/cam")
def cam():
  url_for('static', filename='current.jpg')
  url_for('static', filename='pos.json')
  return render_template('cam.html', img_src='static/current.jpg?' + str(int(time.time())))

@app.route("/laser_map")
def laser_map():
  return render_template('visu_laser.html')

if __name__ == "__main__":
  #app.debug = True
  app.run(host='0.0.0.0')
  #app.run()
