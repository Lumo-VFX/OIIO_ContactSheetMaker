import OpenImageIO
from OpenImageIO import ImageInput, ImageOutput
from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo, ROI

import re
import math
from pprint import pprint

paths = ["./Resources/4x4_ContactSheet/1.exr",
	"./Resources/4x4_ContactSheet/2.exr",
	"./Resources/4x4_ContactSheet/3.exr",
	"./Resources/4x4_ContactSheet/4.exr",
	]
resolution = (1920,1080)

images = []

for path in paths:
	image= ImageBuf(path)
	images.append(image)



# Create a new 3-channel, 512x512 float image filled with 0.0 values.
zero = ImageBufAlgo.zero (ROI(0,resolution[0],0,resolution[1],0,1,0,3))

resize = ImageBufAlgo.fit(images[0],roi=ROI(0,int(resolution[0]/2),0,int(resolution[1]/2),0,1,0,3))

result = ImageBufAlgo.add(zero,resize)

result.write("./result.exr")

'''
# Zero out an existing buffer, keeping it the same size and data type
A = ImageBuf(...)
...
ImageBufAlgo.zero (A)

# Zero out just the green channel, leave everything else the same
roi = A.roi
roi.chbegin = 1 # green
roi.chend = 2   # one past the end of the channel region
ImageBufAlgo.zero (A, roi)

# Zero out a rectangular region of an existing buffer
ImageBufAlgo.zero (A, ROI (0, 100, 0, 100))
'''