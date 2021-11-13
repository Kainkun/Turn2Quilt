# Turn2Quilt
Hello! This is a short command line script I made to try to convert looping turntable style 3D animations into "quilt" holograms that can be displayed on a [Looking Glass](https://lookingglassfactory.com/).
This was made in Python version 3.9.2 but I think it should work on most Python versions.<br />
This uses **OpenCV** and **NumPy** to calculate the quilts

Here's an example of a command you would run to use this tool.
The first argument refers to the original mp4 of the turntable animation, and the second argument/flag tells the tool that the character in the animation rotates counterclockwise when looking from above.
If the mp4 file is not in the same folder as the py file, make sure to include the mp4's full path. 
```
Turn2Quilt.py --fileName Witness.mp4 --counterClockwise
```
The tool needs to know the rotation direction in order to create the correct parallax. If the depth of the hologram looks inverted, try turning on the `--counterClockwise` flag, or turning it off.
<br />
<br />
<br />
This example animation is from [Jean Zoudi's Artstation](https://www.artstation.com/artwork/0ndYq8)<br />
Left is the input, Right is the output.<br />
<img src="https://github.com/Kainkun/Turn2Quilt/blob/main/readme/Witness.gif" width="296" height="250" /> <img src="https://github.com/Kainkun/Turn2Quilt/blob/main/readme/Quilt.gif" width="395" height="250" />

Notice that each tile on the right is slight more rotated than the one next to it. That's because each tile represents a different viewing angle on the Looking Glass display
<br />
<br />
<br />
There are several optional arguments you use in this tool. Type `Turn2Quilt.py -h` to see the full list and their descriptions, or just scroll down some more.

Here's an example that uses a bunch of arguments.<br />
If you have an animation going counterclockwise and want a quilt that has 6x5 tiles, cuts off the first 4 frames of the animation, is 24 fps, and where each tile is 30% the resolution of the original file, you could type `Turn2Quilt.py -f Witness.mp4 -c --qc 6 --qr 5 --cs 4 --fps 24 --s 0.30`
```
optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --fileName FILENAME
                        Name of the file to convert. ex: 'Turntable.mp4'
  -c, --counterClockwise
                        Add this flag if the animation is counterclockwise from above.
  --qc QC, --quiltColumns QC
                        Number of columns in the final quilt. (Default is 8)
  --qr QR, --quiltRows QR
                        Number of rows in the final quilt. (Default is 6)
  --fps FPS, --frameRate FPS
                        Frame rate of final quilt.
  --cs CS, --cropStart CS
                        How many frames to cut from the beginning of the animation.
  --ce CE, --cropEnd CE
                        How many frames to cut from the end of the animation.
  -s SCALE, --scale SCALE
                        Percentage to scale down the resolution before tiling into a quilt. (Default is 0.25)
  --nf NF, --NthFrames NF
                        Number of frames to skip between each frame. (Also speeds up the animation) ex: '3' will
                        render every third frame
  --pnf PNF, --parallaxNthFrames PNF
                        Number of frames to skip between each quilt tile. (Also slows the animation) ex: '2' will
                        create more parallax between frames and be more depthy
  -r, --reverse         Renders the quilt in reverse
  -o OUTPUTNAME, --outputName OUTPUTNAME
                        File name to use as output. ex: 'output.mp4'
```

Beware, I just made this in a day so it isn't tested much and might be buggy or unintuitive.
I also don't know how well this works for animations that aren’t steady looping animations. But try it out!
