import numpy as np

from Camera import Camera

from linuxpy.video.device import Frame


class CameraFrame:

    """ Stores details of a single camera frame """

    def __init__(self, camera: Camera, frame: Frame, timestamp: float, framerate: float):
        """ Constructor

        Args:
            camera (Camera): Camera source for the frame
            frame (Frame): V4L2 Frame from the camera
            timestamp (float): Epoch timestamp the image was captured in seconds
            framerate (float): Frame rate of the capture in hz
        """
        self.camera = camera
        self.frame = frame
        self.timestamp = timestamp
        self.framerate = framerate

    def frame_as_np(self) -> np.ndarray:
        """ Generates a new np object for the frame with the same shape as the camera buffer

        Returns:
            np.ndarray: new np object for the frame with the same shape as the camera buffer
        """
        return np.ndarray(
            shape=(self.frame.width, self.frame.height, 2),
            dtype=np.uint8,
            buffer=self.frame.data
        )
