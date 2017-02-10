#inkscape -z -e 0dbe4a064abea1a9a3bc0d2732643e6b.png -h 720 0dbe4a064abea1a9a3bc0d2732643e6b.svg
#convert -density 1200 -resize 200x200 source.svg target.png

import os
import subprocess as sp

img_list = os.listdir(".")

print(img_list)

for image in img_list:
	if image.endswith(".gif") or image.endswith(".jpg"):
		img = str(image)
		dest = img.split(".")
		dest = dest[0] + ".png"
		print(img)
		print(dest)
		#cmd = ["inkscape", "-z", "-e ", dest, "-h", "720", img]
		cmd = ["convert", "-density", "1200", "-resize", "x720", img, dest]
		print(cmd)
		sp.call(cmd)
		os.remove(image)
