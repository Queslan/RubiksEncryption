import cv2
from FullCube import FullCube as fC
import ImageProcessing as iP


image = iP.get_image('bpg_part.png')
full_cube = fC(iP.make_cubes(image))

#moves = ['U', 'L', 'D', 'R', 'F', 'B', 'B', 'B', 'U', 'U', 'U', 'L', 'L', 'L']
moves = ['L', 'R', 'F', 'R', 'B', 'B']
#moves = ['L', 'D', 'D', 'B', 'L', 'R', 'U', 'U', 'LI', 'DI', 'U', 'R', 'F', 'F']
full_cube.move_cube(moves)

full_cube.solve_cube()
#newArray = iP.make_cubic_cut(full_cube.elements)
newArray = iP.reassembly_image(full_cube.elements)
cv2.namedWindow('myCube', cv2.WINDOW_NORMAL)
iP.show_image("myCube", newArray)

cv2.waitKey(0)
