from multiprocessing import Event, Process, Queue
from typing import Optional

import cscore
from cscore import CameraServer
import numpy as np

from Camera import Camera
from Frame import Frame


class FrameGrabber:
    def __init__(self, camera: Camera, frame_queue: Queue, buffer_count: int = 10):
        """ Manages capturing frames from a camera source

        Args:
            camera (Camera): Camera to grab frames from
            frame_queue (Queue): Frame processing queue
            buffer_count (int, optional): Capture buffer count. Defaults to 10.
        """
        self.camera = camera
        self.frame_queue = frame_queue
        self.buffer_count = buffer_count
        self.process = Process(target=self._worker)
        self.event = Event()

    def start(self):
        """ Starts the camera capture process
        """
        self.event.clear()
        self.process.start()

    def stop(self, wait: bool = False, timeout: Optional[float] = None):
        """ Signals the camera process to stop capturing 

        Args:
            wait (bool, optional): If true, method will stall until camera capture process ends. If ommited or False, returns immediately.
            timeout (Optional[float], optional): Timeout in seconds. If None or omitted, timeout will be infinite. Ignored if wait is False or omitted.
        """

        self.event.set()

        if wait:
            self.wait_on_stop(timeout)

    def wait_on_stop(self, timeout: Optional[float] = None):
        """ Waits until the camera capture process stops.

        Args:
            timeout (Optional[float], optional): Timeout in seconds. If None or omitted, timeout will be infinite.
        """
        self.process.join(timeout)

    def _worker(self) -> None:
        """ Frame grabber process worker method """
        source = cscore.UsbCamera(self.camera.name, self.camera.path_index)
        source.setVideoMode(
            pixelFormat=cscore.VideoMode.PixelFormat.kGray,
            width=self.camera.x_res,
            height=self.camera.y_res,
            fps=self.camera.fps)
        CameraServer.startAutomaticCapture(source)
        
        cvSink = CameraServer.getVideo(source)

        # TODO Move buffers to shared memory {https://superfastpython.com/numpy-share-array-processes/} Method 7
        buffers = [np.zeros((self.camera.x_res, self.camera.y_res),
                                 dtype="uint8") for i in range(self.buffer_count)]

        buffer_idx = 0

        while not self.event.is_set():
            buffer = buffers[buffer_idx]
            timestamp, _ = cvSink.grabFrame(buffer)
            if timestamp != 0:
                self.frame_queue.put(Frame(self.camera, buffer, timestamp))
                
                buffer_idx += 1 
                if buffer_idx >= len(buffers):
                    buffer_idx = 0