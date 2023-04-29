import os
from PIL import Image
from time import sleep


extensions_to_move = ['.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi', '.png', '.gif', 
'.webp', '.tiff', '.tif', '.psd', '.raw', '.arw', '.cr2', '.nrw', '.k25', '.bmp', 
'.dib', '.heif', '.heic', '.ind', '.indd', '.indt', '.jp2', '.j2k', '.jpf', 
'.jpx', '.jpm', '.mj2', '.svg', '.svgz', '.ai', '.eps']

goodbye = """

 ██████   ██████   ██████  ██████  ██████  ██    ██ ███████ 
██       ██    ██ ██    ██ ██   ██ ██   ██  ██  ██  ██      
██   ███ ██    ██ ██    ██ ██   ██ ██████    ████   █████   
██    ██ ██    ██ ██    ██ ██   ██ ██   ██    ██    ██      
 ██████   ██████   ██████  ██████  ██████     ██    ███████ 
                                                     
"""


intro = """

██   ██  ██████  ██████  ██ ███████  ██████  ███    ██ ████████  █████  ██                                      
██   ██ ██    ██ ██   ██ ██    ███  ██    ██ ████   ██    ██    ██   ██ ██                                      
███████ ██    ██ ██████  ██   ███   ██    ██ ██ ██  ██    ██    ███████ ██                                      
██   ██ ██    ██ ██   ██ ██  ███    ██    ██ ██  ██ ██    ██    ██   ██ ██                                      
██   ██  ██████  ██   ██ ██ ███████  ██████  ██   ████    ██    ██   ██ ███████                                 
                                                                                                                
                                        ██    ██ ███████ ██████  ████████ ██  ██████  █████  ██                 
                                        ██    ██ ██      ██   ██    ██    ██ ██      ██   ██ ██                 
                                        ██    ██ █████   ██████     ██    ██ ██      ███████ ██                 
                                         ██  ██  ██      ██   ██    ██    ██ ██      ██   ██ ██                 
                                          ████   ███████ ██   ██    ██    ██  ██████ ██   ██ ███████            
                                                                                                                                                                                                                               
                                                                            ███████ ██████  ██      ██ ████████ 
                                                                            ██      ██   ██ ██      ██    ██    
                                                                            ███████ ██████  ██      ██    ██    
                                                                                 ██ ██      ██      ██    ██    
                                                                            ███████ ██      ███████ ██    ██    

"""

print(intro)
sleep(1)



folder = input('Enter folder: ')

while not os.path.exists(folder):
	print('Folder does not exists, try again or type "x" to exit the program.')
	folder = input('Enter folder: ')
	if folder.lower() == 'x':
		print(goodbye)
		sleep(1.5)
		exit()



if not os.path.exists(f'{folder}/Horizontal'):
	os.mkdir(f'{folder}/Horizontal')

if not os.path.exists(f'{folder}/Vertical'):
	os.mkdir(f'{folder}/Vertical')


cnt = 0
for item in os.listdir(folder):
	for i in extensions_to_move:
		if item.endswith(i):
			try:	
				with Image.open(f'{folder}/{item}', 'r') as im:
					height = im.height
					width = im.width
			except:
				print(f'cannot open file: {item}')
			try:	
				outname_v = f'{folder}/Vertical/{item}'
				outname_h = f'{folder}/Horizontal/{item}'
				
				if height > width:
					if not os.path.exists(outname_v):
						os.rename(f'{folder}/{item}', outname_v)
					else:
						while os.path.exists(outname_v):
							out_split = list(os.path.splitext(outname_v))
							out_split[0] += ' - (copy)'
							outname_v = "".join(out_split)
						else:
							os.rename(f'{folder}/{item}', outname_v)
					cnt += 1

				elif height < width:
					if not os.path.exists(outname_h):
						os.rename(f'{folder}/{item}', outname_h)
					else:
						while os.path.exists(outname_h):
							out_split = list(os.path.splitext(outname_h))
							out_split[0] += '(copy)'
							outname_h = "".join(out_split)
						else:
							os.rename(f'{folder}/{item}', outname_h)
					cnt += 1
				else:
					continue

			except Exception as e:
				print(f'could not move file: {item}', e)

print(f'\nAll done, {cnt} files were moved.\n')
exit = input('type "x" to exit.')
if exit.lower() == 'x':
	sleep(1)
	print(goodbye)

