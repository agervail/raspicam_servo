import json
k = json.load(open('out.json'))
print '<html>		<head><!-- Plotly.js -->		<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>		</head>		<body>		<!-- Plotly chart will be drawn inside this DIV -->		<div id="myDiv" style="width:100%;height:100%"></div>		<script>'

nb_l = 21
print len(k)
for i in range(0,len(k),nb_l):
  print 'var trace' + str(i/nb_l) + '= {'
  print 'x : ['
  for j in range(nb_l):
    print k[i + j][0], ',',
  print '],'
  print 'y : ['
  for j in range(nb_l):
    print k[i + j][1], ',',
  print '],'
  print 'z : ['
  for j in range(nb_l):
    print k[i + j][2], ',',
  print '],'

  print "mode: 'lines',"
  print "marker: {"
  print "    color: '#1f77b4',"
  print "    size: 12,"
  print "    symbol: 'circle',"
  print "    line: {"
  print "     color: 'rgb(0,0,0)',"
  print "      width: 0"
  print "    }"
  print "  },"
  print "  line: {"
  print "    color: '#1f77b4',"
  print "    width: 1"
  print "  },"
  print "  type: 'scatter3d'"
  print "};"

print "var data = [",
for i in range(0,len(k),nb_l):
  print "trace" + str(i/nb_l) + ', ',
print "];",
print "var layout = {"
print "  autosize: false,"
print "  width: 500,"
print "  height: 500,"
print "  margin: {"
print "    l: 0,"
print "    r: 0,"
print "    b: 0,"
print "    t: 65"
print "  }"
print "};"
print "Plotly.newPlot('myDiv', data, layout);"
print "		</script>		</body></html>"
