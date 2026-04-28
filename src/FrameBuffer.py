

from multiprocessing.sharedctypes import RawArray

import numpy as np

from Camera import Camera


class FrameBuffer:
    """ Manages a camera buffer in shared memory for inter-process communication"""

    def __init__(self, camera: Camera):
        """Constructor

        Args:
            camera (Camera): Camera object that the buffer is for
        """
        self.camera = camera
        self.buffer_size = camera.x_res * camera.y_res
        self.__buffer = RawArray('B', camera.x_res * camera.y_res * 3)

    def asNumpy(self) -> np.ndarray:
        """ Generates a Numpy buffer backed by the shared memory of the buffer

        Returns:
            np.ndarray: new numpy array backed by the shared memory of the buffer
        """
        return np.ndarray(
            shape=(self.camera.y_res, self.camera.x_res, 3),
            dtype=np.uint8,
            buffer=self.__buffer)
