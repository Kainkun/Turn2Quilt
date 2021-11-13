#By Kainkun
#Command line python tool to turn turntable animations into Looking Glass quilt holograms

import cv2
import numpy as np
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fileName', type=str, required=True, help="Name of the file to convert. ex: 'Turntable.mp4'")
parser.add_argument('-c', '--counterClockwise', action="store_true", required=False, help="Add this flag if the animation is counterclockwise from above.")
parser.add_argument('--qc', '--quiltColumns', type=int, required=False, default = 8, help="Number of columns in the final quilt. (Default is 8)")
parser.add_argument('--qr', '--quiltRows', type=int, required=False, default = 6, help="Number of rows in the final quilt. (Default is 6)")
parser.add_argument('--fps', '--frameRate', type=float, required=False, help="Frame rate of final quilt.")
parser.add_argument('--cs', '--cropStart', type=int, required=False, default = 0, help="How many frames to cut from the beginning of the animation.")
parser.add_argument('--ce', '--cropEnd', type=int, required=False, default = 0, help="How many frames to cut from the end of the animation.")
parser.add_argument('-s', '--scale', type=float, required=False, default = 0.25, help="Percentage to scale down the resolution before tiling into a quilt. (Default is 0.25)")
parser.add_argument('--nf', '--NthFrames', type=float, required=False, default = 1, help="Number of frames to skip between each frame. (Also speeds up the animation) ex: '3' will render every third frame")
parser.add_argument('--pnf', '--parallaxNthFrames', type=float, required=False, default = 1, help="Number of frames to skip between each quilt tile. (Also slows the animation) ex: '2' will create more parallax between frames and be more depthy")
parser.add_argument('-r', '--reverse', action="store_true", required=False, help="Renders the quilt in reverse")
parser.add_argument('-o', '--outputName', type=str, required=False, help="File name to use as output. ex: 'output.mp4'")
args = parser.parse_args()


counterClockwise = args.counterClockwise

quiltColumns = args.qc
quiltRows = args.qr

cropStart = args.cs
cropEnd = args.ce

scale = args.scale

skipFrames = args.nf
parallaxskipFrames = args.pnf

reverse = args.reverse

outputName = args.outputName

inputFile = args.fileName
inputFileBasename = os.path.splitext(os.path.basename(inputFile))[0]

cap = cv2.VideoCapture(inputFile)
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
if(args.fps): #more fps makes it slower but smoother
    fps = args.fps
else:
    fps = int(cap.get(cv2.CAP_PROP_FPS))


#Turn input video into numpy array
buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))
fc = 0
ret = True
while (fc < frameCount  and ret):
    ret, buf[fc] = cap.read()
    fc += 1
cap.release()

#numpy video post processing
if(cropStart != 0):
    buf = buf[cropStart:]
    frameCount -= cropStart

if(cropEnd != 0):
    buf = buf[:cropEnd]
    frameCount -= cropEnd

if(reverse):
    buf = np.flipud(buf)


#Quilt stitching
frames = [0 for x in range(frameCount)]
for f in range(frameCount):

    offset = f * skipFrames #multiply makes spin faster because it skips frames

    quiltArray = [[0 for x in range(quiltColumns)] for y in range(quiltRows)] 
    for y in range(quiltRows):
        for x in range(quiltColumns):
            index = y * quiltColumns + x
            frame = round(round(index * parallaxskipFrames) + offset) % frameCount #parallaxskipFrames makes it depthyer because of more parallax from skipping frames, also makes video slower
            if((counterClockwise and not reverse) or (not counterClockwise and reverse)):
                quiltArray[y][quiltColumns - x - 1] = cv2.resize(buf[frame], (0,0), None, scale, scale)
            else:
                quiltArray[quiltRows - y - 1][x] = cv2.resize(buf[frame], (0,0), None, scale, scale)


    hstacks = [0 for y in range(quiltRows)]
    for y in range(quiltRows):
        hstack = np.hstack(quiltArray[y])
        hstacks[y] = hstack

    stack = np.vstack(hstacks)
    frames[f] = stack


shape = np.shape(frames)

if(not outputName):
    outputName = inputFileBasename + "_qs" + str(quiltColumns) + "x" + str(quiltRows) + "a" + str(round(frameWidth/frameHeight,2)) + ".mp4"
out = cv2.VideoWriter(outputName, cv2.VideoWriter_fourcc(*'mp4v'), fps, (shape[2], shape[1]))
for f in range(frameCount):
    data = frames[f]
    out.write(data)
out.release()