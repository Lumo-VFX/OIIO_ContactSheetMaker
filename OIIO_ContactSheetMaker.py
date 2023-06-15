import OpenImageIO
from OpenImageIO import ImageInput, ImageOutput
from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo, ROI

import re
import math
from pprint import pprint
import os

paths = []
folder_path = "./Resources/9_ContactSheet"
files = os.listdir(folder_path)
files.sort()
for file in files:
	if file[0] != ".":
		paths.append(os.path.join(folder_path,file))

print(paths)

paths = ["/Users/lumo/Documents/Projects/Current/OIIO_ContactSheetMaker/Resources/Checkered_Frame_1001-1100/Checkered_Frame.####.exr",
	"/Users/lumo/Documents/Projects/Current/OIIO_ContactSheetMaker/Resources/2_Checkered_Frame_1001-1100/Checkered_Frame.####.exr",
	"/Users/lumo/Documents/Projects/Current/OIIO_ContactSheetMaker/Resources/3_Checkered_Frame_1001-1100/Checkered_Frame.####.exr",
	"/Users/lumo/Documents/Projects/Current/OIIO_ContactSheetMaker/Resources/4_Checkered_Frame_1001-1100/Checkered_Frame.####.exr"]
resolution = (1920,1080)

def path_to_frames(path):
	# expects a file path or a %04d or #### path
	# returns the path to the frames
	frames = {}
	if re.search(r"#+|%\d*d",str(path)):
		folder,file_name = os.path.split(path)
		re_pattern = re.sub(r"#+|%\d*d", "([0-9]+)", file_name)
		folder = os.path.abspath(folder)
		for f in os.listdir(folder):
			re_match = re.match(re_pattern,f)
			if re_match:
				frames[re_match[1]] = os.path.join(folder,f)
				#print(os.path.join(folder,f))
	else:
		frames['0001'] = str(path)
	return(frames)

def get_frame_range(path):
	# expects a file path or a %04d or #### path
	# returns the available frame range
	frames = []
	if re.search(r"#+|%\d*d",str(path)):
		folder,file_name = os.path.split(path)
		re_pattern = re.sub(r"#+|%\d*d", "([0-9]+)", file_name)
		folder = os.path.abspath(folder)
		for f in os.listdir(folder):
			re_match = re.match(re_pattern,f)
			if re_match:
				frames.append(int(re_match.group(1)))
		frames.sort()
	return((frames[0],frames[-1]))

def generate_coord(resolution, amount):
	sqrroot = math.ceil(math.sqrt(amount))
	square_amount = sqrroot ** 2
	coords = [[0,0]]
	chunk = [int(resolution[0]/sqrroot),int(resolution[1]/sqrroot)]
	for _ in range(amount-1):
		if coords[-1][1]<sqrroot:
			if coords[-1][0] < sqrroot-1:
				coords.append([coords[-1][0]+1,coords[-1][1]])
			else:
				coords.append([0,coords[-1][1]+1])

	for coord in coords:
		coord[0] = coord[0] * chunk[0]
		coord[1] = coord[1] * chunk[1]

	return(coords)

def generate_contact_sheet(paths, resolution = (3840,2160), image_sequence = True):
	sqrroot = math.ceil(math.sqrt(len(paths)))
	square_amount = sqrroot ** 2
	chunk = [int(resolution[0]/sqrroot),int(resolution[1]/sqrroot)]
	result = ImageBufAlgo.zero (ROI(0,resolution[0],0,resolution[1],0,1,0,3))
	master_list = []
	first_frames = []
	last_frames = []
	for path in paths:
		frames = get_frame_range(path)
		master_list.append(path_to_frames(path))
		first_frames.append(frames[0])
		last_frames.append(frames[1])

	first_frames.sort()
	last_frames.sort()

	frame_range = (first_frames[0],last_frames[-1])

	for f in range(frame_range[0],frame_range[1]+1):

		images = []
		frame = str(f).ljust(4,"0")
		print(frame)

		for frame_list in master_list:
			frames = list(frame_list.keys())
			frames.sort()
			if f < int(frames[0]):
				image= ImageBuf(frame_list[frames[0]])
				images.append(image)
			elif f > int(frames[-1]):
				image= ImageBuf(frame_list[frames[-1]])
				images.append(image)
			else:
				image= ImageBuf(frame_list[frame])
				images.append(image)

		# for path in paths:
		# 	image= ImageBuf(path)
		# 	images.append(image)

		coords = generate_coord(resolution,len(paths))

		for i,image in enumerate(images):
			resize = ImageBufAlgo.fit(image,roi=ROI(coords[i][0],coords[i][0]+chunk[0],coords[i][1],coords[i][1]+chunk[1],0,1,0,4))
			ImageBufAlgo.paste(result, coords[i][0], coords[i][1], 0, 0, resize)


		result_path = os.path.abspath("result/result.{}.exr".format(frame))
		print(result_path)
		result.write(result_path)

def run():
	generate_contact_sheet(paths,resolution)

run()
