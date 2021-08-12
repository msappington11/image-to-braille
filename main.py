from PIL import Image
from numpy import asarray
import numpy as np
import numpy
import cv2

# converts the image into braille so it retains as much detail as possible
def convertToBraille(imarr):
    compressed = compress(imarr, 'braille')
    height = len(compressed)
    width = len(compressed[0])
    average = np.average(compressed)
    braille = []
    #loops through the new compressed image in blocks of 2x3 and adds a list of the bright pixels to the braille list
    for i in range(0, height, 3):
        for j in range(0, width, 2):
            try:
                bright = []
                for a in range(i, i+3, 1):
                    for u in range(j, j+2, 1):
                        if(compressed[a][u] > average):
                            bright.append((a-i)*2 + u-j+1)
                braille.append(bright)
            except:
                continue
        braille.append('NEXT')

    #all 64 braille characters
    characters = [u'⠀', u'⠁', u'⠂', u'⠃', u'⠄', u'⠅', u'⠆', u'⠇', u'⠈', u'⠉', u'⠊', u'⠋', u'⠌', u'⠍', u'⠎', u'⠏',
                  u'⠐', u'⠑', u'⠒', u'⠓', u'⠔', u'⠕', u'⠖', u'⠗', u'⠘', u'⠙', u'⠚', u'⠛', u'⠜', u'⠝', u'⠞', u'⠟',
                  u'⠠', u'⠡', u'⠢', u'⠣', u'⠤', u'⠥', u'⠦', u'⠧', u'⠨', u'⠩', u'⠪', u'⠫', u'⠬', u'⠭', u'⠮', u'⠯',
                  u'⠰', u'⠱', u'⠲', u'⠳', u'⠴', u'⠵', u'⠶', u'⠷', u'⠸', u'⠹', u'⠺', u'⠻', u'⠼', u'⠽', u'⠾', u'⠿',
                  '\n']

    #all 64 braille characters represented as an array of indexes of dots
    representation = [[], [1], [3], [1, 3], [5], [1, 5], [3, 5], [1, 3, 5], [2], [1, 2], [2, 3], [1, 2, 3], [2, 5], [1, 2, 5], [2, 3, 5], [1, 2, 3, 5],
                      [4], [1, 4], [3, 4], [1, 3, 4], [4, 5], [1, 4, 5], [3, 4, 5], [1, 3, 4, 5], [2, 4], [1, 2, 4], [2, 3, 4], [1, 2, 3, 4], [2, 4, 5], [1, 2, 4, 5], [2, 3, 4, 5], [1, 2, 3, 4, 5],
                      [6], [1, 6], [3, 6], [1, 3, 6], [5, 6], [1, 5, 6], [3, 5, 6], [1, 3, 5, 6], [2, 6], [1, 2, 6], [2, 3, 6], [1, 2, 3, 6], [2, 5, 6], [1, 2, 5, 6], [2, 3, 5, 6], [1, 2, 3, 5, 6],
                      [4, 6], [1, 4, 6], [3, 4, 6], [1, 3, 4, 6], [4, 5, 6], [1, 4, 5, 6], [3, 4, 5, 6], [1, 3, 4, 5, 6], [2, 4, 6], [1, 2, 4, 6], [2, 3, 4, 6], [1, 2, 3, 4, 6], [2, 4, 5, 6], [1, 2, 4, 5, 6], [2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6],
                      'NEXT']

    #matches the bright pixels to the braille characters and writes them to a file
    endStr = u""
    for i in range(len(braille)):
        for j in range(len(representation)):
            if(braille[i] == representation[j]):
                endStr += characters[j]
    f = open("final.txt", "w", encoding="utf-8")
    f.write(endStr)
    f.close()

# uses edge detection to find a simple version of the image
def convertToEdges(imarr):
    compressed = np.uint8(compress(imarr, 'edges'))
    edges = cv2.Canny(compressed, 150, 200)
    endStr = ''
    f = open('final.txt', 'w')
    for i in range(len(edges)):
        for j in range(len(edges[0])):
            if(edges[i][j] == (255)):
                endStr += '#'
            else:
                endStr += ' '
        endStr += '\n'
    f.write(endStr)
    f.close()


#compressed the image so the end result wont be larger than 2000 characters
def compress(imarr, purpose):
    hdiv = 3 if purpose == 'braille' else 1
    wdiv = 2 if purpose == 'braille' else 1
    height = len(imarr)
    width = len(imarr[0])
    originalHeight = height
    originalWidth = width
    currSize = height/hdiv * width/wdiv
    while(currSize > 2000):
        height /= 1.1
        width /= 1.1
        currSize = height/hdiv * width/wdiv
    compression = int(originalHeight/height + 1) #the amount of pixels that must be grouped together into 1

    #nightmare loop that makes the image smaller so the final product is less than 2000 characters
    compressed = numpy.zeros((int(originalHeight/compression), int(originalWidth/compression)));
    for i in range(0, originalHeight, compression):
        for j in range(0, originalWidth, compression):
            average = 0.0;
            try:
                for a in range(i, i+compression, 1):
                    for u in range(j, j+compression, 1):
                        average += imarr[a][u][0]
                average /= compression**2
                compressed[int(i/compression)][int(j/compression)] = int(average);
            except:
                continue
    return compressed

im = Image.open(r"C:\Users\Scot\Desktop\Nerd Stuff\Braille\image.png").convert("LA")
imarr = asarray(im)
convertToEdges(imarr)
#convertToBraille(imarr)

