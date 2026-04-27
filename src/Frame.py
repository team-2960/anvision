from multiprocessing import Queue

import cv2

from Camera import Camera


class Frame:

    """ Stores details of a single camera frame """

    def __init__(self, camera: Camera, buffer: cv2.typing.MatLike, timestamp: int):
        """ Constructor

        Args:
            camera (Camera): Camera source for the frame
            buffer (cv2.typing.MatLike): buffer storing the image
            timestamp (int): Epoch timestamp the image was captured in micro seconds
        """
        self.camera = camera
        self.buffer = buffer
        self.timestamp = timestamp
