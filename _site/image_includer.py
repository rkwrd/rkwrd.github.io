import glob
import re
import string
import os.path
import PIL
from PIL import Image

DIR_POSTS = "/Users/arne/rkwrd.github.io/_posts/"
DIR_THUMBS = "/Users/arne/rkwrd.github.io/pics/"
DIR_IMAGES = "/Users/arne/rkwrd.github.io/pics/fullsize/"
DIR_IMGSRC = "/Users/arne/ownCloud/Camera Uploads/"

def includeIMG():
    posts = glob.glob(str(DIR_POSTS) + '*.md')
    print "Including images..."
    for elem in posts:
        findIMGname(elem)
    print "Image inclusion complete."
    
def findIMGname(post):
	print "Checking: " + str(post)
	postfile = open(post, "r")
	text = postfile.read()
	postfile.close()

	#refs = re.findall(r'(IMG.{1,}\.jpg)', text)
	refs = re.findall(r'(?=\@\@\@)(.{1,}IMG.{1,}\.jpg)', text)
	names = []

	for ref in refs:
	    #print "--------Reference-------------"
	    #print "REF: " + str(ref)
	    img = re.search(r'(IMG.{1,}\.jpg)', str(ref))
	    img = img.group(0)
	    
	    print "\tIMG: " + str(img)
	    if "_scaled.jpg" in img:
	        print "\tSkip existing image."
	        continue
	    
	    tag = copy_and_scale(img)
	    print "\tTAG: " + str(tag)
	    text = string.replace(text, ref, tag)
	    names.append(ref)
	#print "----------------TEXT---------------------"
	#print text

	postfile = open(post, "w")
	postfile.write(text)
	postfile.close()

def copy_and_scale(filename):
	print ">>> " + str(filename)
	images = glob.glob(DIR_IMAGES + "*")
	reference = ""

	if os.path.exists(str(DIR_THUMBS + filename[:-4] + "_scaled.jpg")):
	    print "\t\tThumbnail: Exists"
	else:
	    print "\t\tThumbnail: Creating..."
	    basewidth = 500
	    #print "-----------"
	    #print "VAL: " + str(DIR_IMGSRC + filename)
	    #print "-----------"
	    
	    img = Image.open(str(DIR_IMGSRC + filename))
	    wpercent = (basewidth / float(img.size[0]))
	    hsize = int((float(img.size[1]) * float(wpercent)))
	    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
	    img.save(str(DIR_THUMBS + filename[:-4] + "_scaled.jpg"))

	if os.path.exists(str(DIR_IMAGES + filename)):
		print "\t\tFullsize: Exists"
	else:
	    print "\t\tFullsize: Creating..."
	    # Create that thumbnail
	    basewidth = 1000
	    img = Image.open(str(DIR_IMGSRC + filename))
	    wpercent = (basewidth / float(img.size[0]))
	    hsize = int((float(img.size[1]) * float(wpercent)))
	    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
	    img.save(str(DIR_IMAGES + filename))
	    
	reference = '{% include image.html img="pics/' + str(filename[:-4] + "_scaled.jpg") + '" title="Image" caption="" url="http://www.escapingsloth.com/pics/fullsize/' + str(filename) + '" %}'
	return reference

includeIMG()


