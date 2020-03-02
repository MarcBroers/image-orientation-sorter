import glob
import os
from os import path, DirEntry
from progressbar import Counter, Timer, ProgressBar
import time
from PIL import Image
from enum import Enum
import shutil


class Orientation(Enum):
    UNDEFINED = 0
    HORIZONTAL = 1
    VERTICAL = 2
    SQUARE = 3


class ImageAndOrientation(object):
    file = object
    orientation = Orientation.UNDEFINED


# Get Directory
dir = input("Path to images directory: ")
while not path.exists(dir) and not os.path.isdir(dir):
    dir = input("Invalid Path, try again: ")

# Scan directory for files and images
print()
print('Scanning the directory for files...')

images = []
files = os.scandir(dir)
for file in os.scandir(dir):
    if file.name.lower().endswith(tuple(['.jpg', '.jpeg', '.png', '.gif', '.raw'])):
        image = ImageAndOrientation()
        image.file = file
        images.append(image)

# Processing and sorting images
print()
print("{} images found".format(len(images)))
widgets = ['Processed: ', Counter(), ' images (', Timer(), ')']
pbar = ProgressBar(widgets=widgets)
for i in pbar((i for i in range(len(images)+1))):
    with Image.open(images[i-1].file.path) as img:
        width, height = img.size
        if height > width:
            images[i-1].orientation = Orientation.HORIZONTAL
        elif height < width:
            images[i-1].orientation = Orientation.VERTICAL
        elif height == width:
            images[i-1].orientation = Orientation.SQUARE

if not os.path.exists(os.path.join(dir, Orientation.HORIZONTAL.name)):
    os.makedirs(os.path.join(dir, Orientation.HORIZONTAL.name))
if not os.path.exists(os.path.join(dir, Orientation.VERTICAL.name)):
    os.makedirs(os.path.join(dir, Orientation.VERTICAL.name))
if not os.path.exists(os.path.join(dir, Orientation.SQUARE.name)):
    os.makedirs(os.path.join(dir, Orientation.SQUARE.name))

for image in images:
    shutil.copyfile(image.file.path, os.path.join(
        dir, image.orientation.name, image.file.name))

print()
print("Finished! The images are copied in separate folders based on their orientation.")
print("These folders can be found in: \"{}\"".format(dir))
input()
