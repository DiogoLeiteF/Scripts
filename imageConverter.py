import sys
import os
from PIL import Image


# grad the firs and second argument
origin = sys.argv[1]
dest = sys.argv[2]


# check if folder exists, else create it

try:
	os.mkdir(f'{dest}')
except FileExistsError:
	print('folder already exists')


# loop images 
#convert images
#save images
images = os.listdir(f'{origin}')
for image_name in images:
	with Image.open(f'{origin}/{image_name}') as im:
		outname = os.path.splitext(image_name)
		if outname[0]+'.png' != image_name:
			im.save(f'{dest}/{outname[0]}.png' , 'png')
print('done')





