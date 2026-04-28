from multiprocessing import Event, Process, Queue
from time import time_ns
from typing import Optional

import cscore
from cscore import CameraServer
import cv2
import numpy as np

from Camera import Camera
from Frame import Frame
from FrameBuffer import FrameBuffer


class FrameGrabber:
    def __init__(self, camera: Camera, frame_queue: Queue, frame_buffers: dict[str, FrameBuffer]):
        """ Manages capturing frames from a camera source

        Args:
            camera (Camera): Camera to grab frames from
            frame_queue (Queue): Frame processing queue
            frame_buffers (dict[str, FrameBuffer]): List of named frame buffers.
        """
        self.camera = camera
        self.frame_queue = frame_queue
        self.frame_buffers = frame_buffers
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
            wait (bool, optional): If true, method will stall until camera capture process ends. If omitted or False, returns immediately.
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
            pixelFormat=cscore.VideoMode.PixelFormat.kMJPEG,
            width=self.camera.x_res,
            height=self.camera.y_res,
            fps=self.camera.fps)
        
        CameraServer.startAutomaticCapture(source)

        cvSink = CameraServer.getVideo(source)

        buffer_list = [(name, value.asNumpy())
                       for name, value in self.frame_buffers.items()]

        buffer_idx = 0

        test_buffer = np.zeros((self.camera.y_res, self.camera.x_res, 3), np.uint8)

        put_start = time_ns()
        put_end = time_ns()
        grab_start = time_ns()
        grab_end = time_ns()
        last_grab = time_ns()

        while not self.event.is_set():
            buffer_name, buffer_np = buffer_list[buffer_idx]
            grab_start = time_ns()
            grab_delay = (grab_start - grab_end) * 1e-9
            print(f"Grab Delay: {grab_delay:.6f} s", flush=True)
            timestamp, _ = cvSink.grabFrame(buffer_np)
            last_grab = grab_end
            grab_end = time_ns()
            if timestamp != 0:
                put_start = time_ns()
                self.frame_queue.put(
                    Frame(self.camera, buffer_name, timestamp))
                put_end = time_ns()

                put_period = (put_end - put_start) * 1e-9
                grab_period = (grab_end - last_grab) * 1e-9
                grab_rate = 1 / grab_period

                print(f"Put Period: {put_period:.6f} s", flush=True)
                print(f"Grab Period: {grab_period:.6f} s", flush=True)
                print(f"Grab Rate: {grab_rate:.6f} s", flush=True)

                buffer_idx += 1
                if buffer_idx >= len(buffer_list):
                    buffer_idx = 0
