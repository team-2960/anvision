from time import monotonic
from typing import Generator
import numpy as np

from Camera import Camera
from CameraFrame import CameraFrame

from linuxpy.video.device import PixelFormat, VideoCapture


class FrameGrabber:
    def __init__(self, camera: Camera):
        """ Manages capturing frames from a camera source

        Args:
            camera (Camera): Camera to grab frames from
        """
        self.camera = camera

    def capture(self) -> Generator[CameraFrame, None, None]:
        """ Frame grabber process worker method

        Yields:
            Generator[CameraFrame, None, None]: new frame from the camera
        """
        # Initialize capture device
        device = self.camera.get_device()


        with device:
            # Initialize video capture
            capture = VideoCapture(device)
            capture.set_fps(self.camera.fps)
            # TODO Allow configurable frame format
            capture.set_format(self.camera.x_res, self.camera.y_res, PixelFormat["YUYV"])
            

            # Initialize time stamping
            start = last = monotonic()

            # Start capturing frames
            with capture:

                # TODO Add logging

                # Wait for frames
                for frame in capture:
                    new = monotonic()
                    framerate = 1.0 / new - last
                    last = new 
                    yield CameraFrame(self.camera, frame, frame.timestamp, framerate)

