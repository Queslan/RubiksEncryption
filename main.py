import cv2
from fullCube import FullCube as fC
import imageProcessing as iP


image = iP.getImage('cubesNumbered.png')
fullCube = fC(iP.makeCubes(image))
#fullCube.U()
#fullCube.D()
#fullCube.F()
#fullCube.B()
#fullCube.R()
#fullCube.L()

for i in range(4):
    fullCube.L()

newArray = iP.getFullImage(fullCube.elements)
iP.showImage("myCube", newArray)


cv2.waitKey(0)