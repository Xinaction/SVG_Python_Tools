import sys
import os
from PIL import Image

class GraphicObject:
	def __init__(self,fname):
		self.fileName = fname
		self.image = Image.open(fname)

	def width(self):
		return self.image.size[0]

	def height(self):
		return self.image.size[1]

	def render(self,atlas,x,y):
		atlas.paste(self.image,(x,y))

	def getName(self):
		return os.path.basename(self.fileName)[:-4]

class GraphicPacker:
	def __init__(self,width = 512):
		self.imageWidth = width 														# width of atlas sheet.
		self.imageList = []																# list of images.

	def append(self,graphicObject):
		self.imageList.append({ "object":graphicObject, "area":graphicObject.width()*graphicObject.height() })

	def pack(self,packStep = 4):

		self.atlasHeight = 0
		iList = sorted(self.imageList,key=lambda k: k['area'],reverse = True)			# list sorted largest first.
		for i in range(0,len(iList)):													# for every element.
			x = 0																		# suggested position.
			y = 0	
			isOk = False 																# set true when done.
			while not isOk:																# keep going until found.
				iList[i]["left"] = x													# save position
				iList[i]["top"] = y
				iList[i]["right"] = x + iList[i]["object"].width() 
				iList[i]["bottom"] = y + iList[i]["object"].height() 
				isOk = self.canPlace(iList[i],iList,0,i-1)								# check if it can go there
				if not isOk:															# it can't.
					x = x + packStep															# try slightly to right.
					if x + iList[i]["object"].width() >= self.imageWidth: 				# if it can't fit on this line
						x = 0															# move down.
						y = y + packStep

			self.atlasHeight = max(self.atlasHeight,iList[i]["bottom"]+2)				# update the bottom size

	def render(self,baseName):
		baseName = baseName.lower()														# all file names l/c
		atlas = Image.new("RGBA",(self.imageWidth,self.atlasHeight),(0,0,0,0))			# transparent background
		for image in self.imageList:													# render all images
			image["object"].render(atlas,image["left"],image["top"])	
		atlas.save(baseName+".png",optimize=True)										# save atlas image				
		subText = open(baseName+" subimages.txt","w")									# create text
		for image in self.imageList:
			subText.write(image["object"].getName()+":")
			subText.write(str(image["left"])+":")
			subText.write(str(image["top"])+":")
			subText.write(str(image["right"]-image["left"])+":")
			subText.write(str(image["bottom"]-image["top"])+"\n")
		subText.close()

	def canPlace(self,item,iList,first,last):
		for i in range(first,last+1):													# work through all.
			if self.collides(iList[i],item):											# if collision found return False
				return False
		return True 																	# No collisions return true

	def collides(self,r1,r2):															# Check two items collide.
		separate = 	r1["right"] < r2["left"] or \
					r1["left"] > r2["right"] or \
					r1["top"] > r2["bottom"] or \
					r1["bottom"] < r2["top"]
		return not separate


#print (cur_file_dir())
path = os.getcwd()
#print (path)

nPos = path.rfind(os.sep)
pngname = path[nPos+1:]
#print(pngname)

if os.path.exists("png"): 
	print("Tmp png folder exist...")
	exit()
else:
	os.mkdir("png") 

for dirpath, dirname, filenames in os.walk(path):
	for filename in filenames:
		if os.path.splitext(filename)[1] == '.svg':
			filepath = os.path.join(dirpath, filename)
			filesubname = filename.rstrip(".svg")
			print (filename + " ---> " + filesubname + '.png')
			#rsvg-convert -z 4 shape213.svg>shape213.png
			os.system("rsvg-convert -z %s %s>./png/%s.png" % (4, filepath, filesubname)) # 4 default zoom size.


print ("Making texture atlas......")
gpack = GraphicPacker()
for root,dirs,files in os.walk("png"):
	for f in files:
		fName = root + os.sep + f
		gob = GraphicObject(fName)
		gpack.append(gob)
gpack.pack()
gpack.render(pngname)
print ("Done.")
