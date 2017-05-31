from __future__ import print_function
import os
import sys
from PIL import Image
from pathlib import Path
from colors import colors

class BedPart:
	def __init__(self, name, y1, y2, cap, whiten_ratio=0.0):
		self.name = name
		self.y1   = y1
		self.y2   = y2
		self.cap  = cap
		self.wratio = whiten_ratio  # 0.0 .. 1.0

	def whiten(self, code):
		return tuple(map(lambda c: int(c + (255 - c) * self.wratio), code))

def main():
	frame = Image.open("bed-frame.png")
	mask  = Image.open("bed-mask.png")
	mask_avg = 0x43 # (0x434343)

	bed_parts = (
		#       name        , y1, y2, cap, whiten
		BedPart('pillow'    ,  0, 13, 250, 0.8),
		BedPart('cover-head', 13, 17, 255),
		BedPart('cover-sep' , 17, 18, 220),
		BedPart('cover-body', 18, 64, 250),
	)

	for color in colors:
		im = Image.new(mask.mode, mask.size)
		for part in bed_parts:
			px_max = 0
			memo = {}
			part_color = part.whiten(color.code)
			for y in range(part.y1, part.y2):
				for x in range(im.width):
					mask_px = mask.getpixel((x,y))
					if len(mask_px) == 4 and mask_px[3] == 0:
						# not in color mask.
						im.putpixel((x,y), frame.getpixel((x,y)))
						continue

					px = tuple(map(
						lambda x: x[0] + x[1] - mask_avg,
						zip(part_color, mask_px)
					))
					im.putpixel((x,y), px)

					memo[(x,y)] = px
					px_max = max(px_max, *px)

			if px_max > part.cap:
				over = px_max - part.cap
				print("%s.%s: overflow (+%d)" % (color.name, part.name, over))
				for y in range(part.y1, part.y2):
					for x in range(64):
						if (x,y) in memo:
							px = [c - over for c in memo[(x,y)]]
							im.putpixel((x,y), tuple(px))

		im.save("%s.png" % color.name)

if __name__ == '__main__':
	main()
