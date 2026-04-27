from multiprocessing import Queue
from time import time_ns

import numpy as np
import cv2
import apriltag
import cscore
from cscore import CameraServer

from ApriltagDef import ApriltagDef
from ApriltagDetector import ApriltagDetector
from FrameGrabber import FrameGrabber
from Camera import Camera, Intrinsics

camera = Camera(
    name="Webcam",
    path_index=0,
    x_res=1280,
    y_res=960,
    fps=30,
    intrinsics=Intrinsics(
        fx=1405.0193204446784,
        fy=1414.9276311038998,
        cx=621.6754139679053,
        cy=469.8431794550814
    ))

tag_def = ApriltagDef(family="tag36h11", tagsize=0.2667)

def main():

    frame_queue = Queue()

    frameGrabber = FrameGrabber(camera, frame_queue)
    detector = ApriltagDetector(tag_def, frame_queue)

    frameGrabber.start()
    detector.start()


if __name__ == "__main__":
    main()
