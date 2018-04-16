#!/usr/bin/python

import sys
import random
from PIL import Image


im = Image.open('./yay.png')
width, height = im.size
width = (int(width + 99) / 100) * 100
height = (int(height + 99) / 100) * 100

im = im.crop((0, 0, width, height))

im2 = Image.new("RGB", (width, height), "black")

blocks = []
for x in range(width / 100):
    for y in range(height / 100):
        blocks.append(im.crop((x * 100, y * 100, (x + 1) * 100, (y + 1) * 100)))

random.shuffle(blocks)

for x in range(width / 100):
    for y in range(height / 100):
        im2.paste(blocks.pop().rotate(90 * random.randint(0,3)), (x * 100, y * 100))

im2.save("shuf" + origname)
