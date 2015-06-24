'''
Created on Jun 20, 2014
Stream RGB from Carmine/Kinect Device.
author: carlos torres <carlitos408@gmail.com>
'''
import cv2
import cv2.cv as cv
from openni import *
import numpy as np


# Initialize
context = Context()
context.init()

# Create the rgb image generator
image_generator = ImageGenerator()
image_generator.create(context)
image_generator.set_resolution_preset(RES_VGA)
image_generator.fps = 30


def get_rgb():
    """
    Get rgb stream from primesense and convert it to an rgb numpy array
    """
    bgr_frame = np.fromstring(image_generator.get_raw_image_map_bgr(), dtype=np.uint8).reshape(480, 640, 3)
    image = cv.fromarray(bgr_frame)
    cv.CvtColor(cv.fromarray(bgr_frame), image, cv.CV_BGR2RGB)
    # this generates a standard np array -- uncomment to test
    rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
    return rgb
# capture_rgb


# start carmine
context.start_generating_all()

done = False
while not done:
    key = cv2.waitKey(1) & 255
    if key == 27:
        print "Terminating code and closing all windows."
        done = True
    #read current stream
    rgb = get_rgb()
    cv2.imshow('rgb', rgb)
    context.wait_any_update_all() # refresh
#endwhile

cv2.destroyAllWindows()
# close carmine context and stop device
context.stop_generating_all()
