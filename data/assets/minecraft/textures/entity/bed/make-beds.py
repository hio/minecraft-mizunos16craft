from __future__ import print_function
import os
import sys
from PIL import Image
from pathlib import Path
from wool_colors import colors

class BedPart:
	def __init__(self, name, y1, y2, cap):
		self.name = name
		self.y1   = y1
		self.y2   = y2
		self.cap  = cap

def main():
	frame = Image.open("bed-frame.png")
	mask  = Image.open("bed-mask.png")
	mask_avg = 0x43 # (0x434343)

	bed_parts = (
		#       name        , y1, y2, cap.
		BedPart('pillow'    ,  0, 13, 250),
		BedPart('cover-head', 13, 17, 255),
		BedPart('cover-sep' , 17, 18, 220),
		BedPart('cover-body', 18, 64, 250),
	)
	for color in colors:
		im = Image.new(mask.mode, mask.size)
		for part in bed_parts:
			px_max = 0
			for y in range(part.y1, part.y2):
				for x in range(im.width):
					mask_px = mask.getpixel((x,y))
					if len(mask_px) == 4 and mask_px[3] == 0:
						px = frame.getpixel((x,y))
					else:
						px = [0,0,0]
						px[0] = color.code[0] + mask_px[0] - mask_avg
						px[1] = color.code[1] + mask_px[1] - mask_avg
						px[2] = color.code[2] + mask_px[2] - mask_avg
						px_max = max(px_max, *px)
					im.putpixel((x,y), tuple(px))

			if px_max > part.cap:
				over = px_max - part.cap
				print("%s.%s: overflow (+%d)" % (color.name, part.name, over))
				for y in range(part.y1, part.y2):
					for x in range(64):
						px = mask.getpixel((x,y))
						if not (len(px) == 4 and px[3] == 0):
							px = list(px)
							px[0] = color.code[0] + px[0] - mask_avg - over
							px[1] = color.code[1] + px[1] - mask_avg - over
							px[2] = color.code[2] + px[2] - mask_avg - over
							im.putpixel((x,y), tuple(px))

		im.save("%s.png" % color.name)

if __name__ == '__main__':
	main()
