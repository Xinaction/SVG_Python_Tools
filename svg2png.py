import sys
import os

sizes = [64, 96, 128]

def print_usage(program_name):
    print ("Usage: %s file1.svg ... fileN.svg") % (program_name)

if len(sys.argv) < 2:
    print_usage(sys.argv[0])
    sys.exit(-1)

svg_files = sys.argv[1:]
for svg_file in svg_files:
    if svg_file.endswith(".svg") == False:
        print (svg_file, " is not a svg file, continuing!")
        continue

    new_filename = svg_file.rstrip(".svg")
    for size in sizes:
        os.system("rsvg-convert -w %s -h %s %s -o %s-%sx%s.png" % (size, size, svg_file, new_filename, size, size) )



