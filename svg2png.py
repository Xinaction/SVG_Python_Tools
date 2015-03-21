import sys
import os

path = os.getcwd()
#print (path)

zoom = 2
if len(sys.argv) > 1:
	zoom = sys.argv[1]

if os.path.exists("png") == False : 
	os.mkdir("png") 
	

for dirpath, dirname, filenames in os.walk(path):
	for filename in filenames:
		if os.path.splitext(filename)[1] == '.svg':
			filepath = os.path.join(dirpath, filename)
			filesubname = filename.rstrip(".svg")
			print (filename + " ---> " + filesubname + '.png')
			#rsvg-convert -z 4 shape213.svg>shape213.png
			os.system("rsvg-convert -z %s %s>./png/%s.png" % (zoom, filepath, filesubname)) # 4 default zoom size.
