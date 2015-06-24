#!/usr/bin/python
'''
Created on Jun 30, 2014
Stream RGB from Carmine/Kinect device

Requires: 
    OpenNI1.54+
    PyOpenNI
    Python 2.7.3 + 
    OpenCV 2.4.5 +
    Numpy
    
@author: carlos torres <carlitos408@gmail.com>
'''
import cv2
from openni import *
import numpy as np

# Initialize
context = Context()
context.init()

# create the ir genrator to access the infra-red stream
ir = IRGenerator()
ir.create(context)
ir.set_resolution_preset(RES_VGA)
ir.fps = 30



def get_ir():
    """ 
    Create array from the raw depth map string.
    depth.get_raw_depth_map_8():= string
    Alternative to "update_depth_image" but doesn't provide floating point
    pixel intensities from depth_image. 
    () -> (1L uint16 ndarray, 3L uint8 ndarray)
    """
    ir_frame = np.asarray(ir.get_tuple_ir_map()).reshape(480, 640)
    # normalize and set to correct range and data type
    maxval = 2**12 -1
    ir4d = cv2.cvtColor(np.uint8(ir_frame.astype(float)*255 /maxval),cv2.COLOR_GRAY2RGB) # normalize the values
    return ir_frame, ir4d
# get_ir

# start carmine
context.start_generating_all()
done = False

while not done:
    key =cv2.waitKey(10)
    if key == 27:
        done = True
    ir_frame, ir4d= get_ir()
    cv2.imshow("depth image", ir4d)
    context.wait_any_update_all()    
#while

cv2.destroyAllWindows()
# close carmine context and stop device
context.stop_generating_all()
