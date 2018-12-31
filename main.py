import time
import cv2
from FullCube import FullCube as fC
import ImageProcessing as iP


def measure_time(file_path):
    start_time = time.time()
    image = iP.get_image(file_path)
    full_cube = fC(iP.make_cubes(image))

    #scramble
    #moves = ['R', 'U', 'LI', 'U', 'D', 'D', 'R', 'R', 'UI', 'DI', 'L', 'U', 'R', 'F', 'B', 'B']
    #full_cube.move_cube(moves)

    #full_cube.solve_cube()
    newArray = iP.make_cubic_cut(full_cube.elements)
    elapsed_time = time.time() - start_time
    #newArray = iP.reassembly_image(full_cube.elements)
    cv2.namedWindow('myCube', cv2.WINDOW_NORMAL)
    cv2.imwrite('cube_start.png', newArray)
    iP.show_image("myCube", newArray)
    print(file_path)
    print(elapsed_time)

##### Linear files don't work without solving, problem with reassembly_image function
#measureTIme('gray8bit.pgm')
#measureTIme('gray16bit.pgm')
#measureTIme('gray16bitL.pgm')
#measureTIme('rgb8bit.ppm')
#measureTIme('rgb16bit.ppm')
#measureTIme('rgb16bitL.ppm')


measure_time("rubik_colors.png")
cv2.waitKey(0)
