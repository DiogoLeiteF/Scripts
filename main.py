import os
from PIL import Image, ImageSequence


def resize_gif(file, min_size_side=250):
    """
    Resize gif to a minimum given side size.
    args:
    file a path to th gif
    min_size_side the side with minimum dimensions
    """

    try:
        with Image.open(f"./{file}") as im:
            if im.size[0] < min_size_side or im.size[1] < min_size_side:
                if im.size[0] < im.size[1]:
                    new_0 = min_size_side
                    new_1 = int(new_0 / im.size[0] * im.size[1])
                else:
                    new_1 = min_size_side
                    new_0 = int(new_1 / im.size[1] * im.size[0])

                new_size = (new_0, new_1)

                frames = []

                for frame in ImageSequence.Iterator(im):
                    # resize frames and append to list
                    frames.append(frame.resize(new_size))

                # save new image with same name
                im.save(file, save_all=True, append_images=frames)
                print(f"{file} => DONE")

                global to_change
                to_change -= 1
                print(f"{to_change} files missing")

    except Exception as e:
        print(file, e)


imfolder = input("enter folder location: ")
try:
    min_size = int((input("enter min size in px: ")).strip())
except Exception:
    print("default value 250px")
    min_size = 250


os.chdir(imfolder)


file_type = ['.gif']

all_gifs = 0
to_change = 0

for file in os.listdir(imfolder):
    for type in file_type:
        if type in file:
            with Image.open(f"./{file}") as im:
                all_gifs += 1
                if im.size[0] < min_size or im.size[1] < min_size:
                    print(f"{file} => ({im.size})")
                    to_change += 1
print(f"\n{to_change} files to change from {all_gifs}")

next = input("continue:  y / n  ")


if next.lower() == 'y':

    for file in os.listdir(imfolder):
        for type in file_type:
            if type in file:
                resize_gif(file, min_size_side=min_size)


else:
    exit()
