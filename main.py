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


moves = ['U', 'L', 'D', 'R', 'F', 'B', 'B', 'B', 'U', 'U', 'U', 'L', 'L', 'L']

for l in moves:
    if l == 'U':
        fullCube.U()
    elif l == 'D':
        fullCube.D()
    elif l == 'F':
        fullCube.F()
    elif l == 'B':
        fullCube.B()
    elif l == 'R':
        fullCube.R()
    elif l == 'L':
        fullCube.L()
    else:
        print("Wrong letter")

newArray = iP.makeCubicCut(fullCube.elements)
cv2.namedWindow('myCube', cv2.WINDOW_NORMAL)
iP.showImage("myCube", newArray)


cv2.waitKey(0)