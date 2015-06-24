#!/usr/bin/python
'''
Created on Jan 30, 2014
Get openni depthmap and convert it to numpy/opencv array for display

Requires:
    OpenNI1.54+
    PyOpenNI
    Python 2.7.3 + 
    OpenCV 2.4.5 +
    Numpy
    
@author: carlos torres <carlitos408@gmail.com>
'''

from openni import *
import numpy as np
import cv2

# -- Initialize
context = Context()
context.init()

# -- create the depth genrator to access the depth stream
depth_generator = DepthGenerator()
depth_generator.create(context)
depth_generator.set_resolution_preset(RES_VGA)
depth_generator.fps = 30
depth_map = None


def get_depth():
    """ 
    Create array from the raw depth map string.
    depth.get_raw_depth_map_8():= string
    Alternative to "update_depth_image" but doesn't provide floating point
    pixel intensities from depth_image. 
    () -> (1L uint16 ndarray, 3L uint8 ndarray)
    16-bits or two bytes:
        The 12 most signicant digits are used to represent the depth 
        The 4 least significant digits are the user id assigned to that pixel
        --> depth values range from 0 to 2**12-1
    """
    depth_frame = np.fromstring(depth_generator.get_raw_depth_map(), "uint16").reshape(480, 640) # 16bits per pixel
    # normalize and set to correct range and data type
    maxval = 2**12-1
    d4d = cv2.cvtColor(np.uint8(depth_frame.astype(float)*255 /maxval),cv2.COLOR_GRAY2RGB) # normalize the values
    return depth_frame, d4d
# get_depth



# -- start carmine
context.start_generating_all()
done = False
while not done:
    key =cv2.waitKey(10)
    if key == 27:
        done = True
    # depth capture
    depth_frame, depth4display = get_depth()
    cv2.imshow("depth image", depth4display)
    context.wait_any_update_all()
#while


# -- release resources
cv2.destroyAllWindows()
context.stop_generating_all()
