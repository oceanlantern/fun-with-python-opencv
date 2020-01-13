"""Fun With Python OpenCV - Computer Vision
author: Tim Adams - oceanlantern@gmail.com

Draw processed image within selected mouse rectangle.
Alternates drawing with different image processing functions: threshold,
GaussianBlur, medianBlur.

Python Versions:
Tested with Python 2.7.14 and 3.7.4

pylint:
Run pylint with flag --extension-pkg-whitelist=cv2

"""
import sys
import datetime
from random import seed
from random import randint
import numpy as np
import cv2

PY36 = sys.version_info[0] == 3 and sys.version_info[1] >= 6
FUN_WITH_PYTHON_CV = "fun_with_python_cv"
WIN_WIDTH = 512
WIN_HEIGHT = 512
LINE_THICKNESS = 2

def zero_image():
    """zero_image
    """
    return np.zeros((512, 512, 3), np.uint8)

class RectInfo:
    """RectInfo
    """

    def __init__(self, x, y):
        self.offset_x = x
        self.offset_y = y
        self.width = 0
        self.height = 0
        self.tracking = False

    def __str__(self):
        # if PY36:
        #    return f" {self.offset_x} offset_y {self.offset_y} width {self.width} height {self.height}" #pylint: disable=line-too-long
        # else:
        return "offset_x {} offset_y {} width {} height {}".format(self.offset_x, self.offset_y, self.width, self.height)

    def valid_dim(self):
        """valid_dim
        """
        return self.width and self.height

    def get_right(self):
        """get_right
        """
        return self.offset_x + self.width

    def get_bottom(self):
        """get_bottom
        """
        return self.offset_y + self.height

    def get_width(self):
        """get_width
        """
        return self.width

    def get_height(self):
        """get_height
        """
        return self.height

    def get_offset_x(self):
        """get_offset_x
        """
        return self.offset_x

    def get_offset_y(self):
        """get_offset_y
        """
        return self.offset_y


# pylint - the following are globals not constants so disabling
# C0103: Constant name "" doesn't conform to UPPER_CASE
# pylint: disable=C0103
rcinfo = RectInfo(0, 0)
img_main = zero_image()
first_button_down = False
draw_with_effect = False

def draw_rect(event, x, y, flags, param):
    #  Disable Using the global statement (global-statement)
    # pylint: disable=W0603
    """ draw_rect
    Draws a rectangle in response to mouse movement with left button down
    When left button is released image is drawn in rectabgle location
    """
    global rcinfo
    global first_button_down
    global img_main
    global draw_with_effect

    if event == cv2.EVENT_LBUTTONDOWN:
        first_button_down = True
        rcinfo = RectInfo(x, y)
        rcinfo.tracking = True
        img_main = zero_image()

    elif event == cv2.EVENT_MOUSEMOVE:
        if rcinfo.tracking:
            # Erase previous rectangle
            if rcinfo.valid_dim():
                cv2.rectangle(img_main, (rcinfo.offset_x, rcinfo.offset_y), (rcinfo.get_right(
                ), rcinfo.get_bottom()), (0, 0, 0), thickness=LINE_THICKNESS)

            new_width = x - rcinfo.offset_x
            new_height = y - rcinfo.offset_y

            print('new_width {} new_height {}'.format(new_width, new_height))

            # Draw new rect
            if new_width and new_height:
                rcinfo.width = new_width
                rcinfo.height = new_height
                cv2.rectangle(img_main, (rcinfo.offset_x, rcinfo.offset_y), (rcinfo.get_right(
                ), rcinfo.get_bottom()), (0, 255, 0), thickness=LINE_THICKNESS)

    elif event == cv2.EVENT_LBUTTONUP:

        # Erase final rectangle
        if rcinfo.valid_dim():
            cv2.rectangle(img_main, (rcinfo.offset_x, rcinfo.offset_y), (rcinfo.get_right(
            ), rcinfo.get_bottom()), (0, 0, 0), thickness=LINE_THICKNESS)

            img_lena = cv2.imread('images\lena.png')
            img_lena = cv2.resize(
                img_lena, (abs(rcinfo.get_width()), abs(rcinfo.get_height())), None, 0, 0)
            #img_lena = cv2.cvtColor(img_lena, cv2.COLOR_BGR2RGB)

            img_lena_arr = np.asarray(img_lena)
            height, width, color = img_lena_arr.shape

            if x >= rcinfo.get_offset_x():
                x = rcinfo.get_offset_x()

            if y >= rcinfo.get_offset_y():
                y = rcinfo.get_offset_y()

            print(
                "broadcasting img_lena->img_main {} {} - {} {}".format(y, y+height, x, x+width))
            img_main = zero_image()

            if draw_with_effect:
                if datetime.datetime.now().second % 2:
                    ret, img_lena = cv2.threshold(
                        img_lena, 127, 255, cv2.THRESH_BINARY_INV)
                    print("ret {}".format(ret))
                else:
                    img_lena = cv2.GaussianBlur(img_lena, (5, 5), 10)
                    #img_lena = cv2.medianBlur(img_lena,5)
            draw_with_effect = not draw_with_effect

            try:
                # Copy processed lena image to main image using array slicing
                img_main[y:y+height, x:x+width] = img_lena
            except Exception as exc:
                # print(
                #    "Exception: Invalid dimension {} {} - {} {}".format(y, y+height, x, x+width))
                print(exc)

        rcinfo.tracking = False

        print(rcinfo)

    elif event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(img_main, (x, y), 100, (255, 0, 0), thickness=-1)

def main():
    #  Disable Using the global statement (global-statement)
    # pylint: disable=w0603
    """
    Main entry point and processing loop
    """
    global first_button_down
    global rcinfo
    global img_main

    cv2.namedWindow(FUN_WITH_PYTHON_CV, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(FUN_WITH_PYTHON_CV, WIN_WIDTH, WIN_HEIGHT)
    cv2.setMouseCallback(FUN_WITH_PYTHON_CV, draw_rect)

    seed(1)
    time_check = datetime.datetime.now()
    pos = (50, 256)
    img_text = zero_image()
    show_text = False

    while cv2.getWindowProperty(FUN_WITH_PYTHON_CV, 0) >= 0:

         # Every second switch between showing title and instructions
         # until left button pressed

        if first_button_down:
            cv2.imshow(FUN_WITH_PYTHON_CV, img_main)
        else:
            timde_delta = datetime.datetime.now() - time_check

            if timde_delta.seconds >= 1:
                time_check = datetime.datetime.now()
                img_text = zero_image()
                pos = (randint(20, 300), randint(20, 400))
                show_text = not show_text

            if not show_text:
                img_text = cv2.putText(img_text, 'Fun with Python - OpenCV', pos,
                                       cv2.FONT_HERSHEY_SIMPLEX, 1,
                                       (0, 255, 0), 2, cv2.LINE_AA, False)
            else:
                img_text = cv2.putText(
                    img_text, 'Select Rect', pos,
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), 2, cv2.LINE_AA, False)
            cv2.imshow(FUN_WITH_PYTHON_CV, img_text)

        # in addition to Close button monitor for esc key to exit
        if cv2.waitKey(20) & 0xff == 27:
            break

if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()
