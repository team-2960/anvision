

from multiprocessing import Event, Process, Queue
import queue
from time import time_ns
from typing import Any, Optional

import apriltag
import cv2
import numpy as np

from ApriltagDef import ApriltagDef
from Frame import Frame
from FrameBuffer import FrameBuffer
from ApriltagResult import ApriltagDetection, ApriltagResult


class ApriltagDetector:

    def __init__(self, tag_def: ApriltagDef, frame_queue: Queue, results_queue: Queue, frame_buffers:dict[str, FrameBuffer], threads:int=4):
        """ Constructor

        Args:
            tag_def (ApriltagDef): Definition of the apriltag to detect
            frame_queue (Queue): Capture Frame queue
            results_queue (Queue): Result queue
            frame_buffers (dict[str, FrameBuffer]): Dictionary of named frame buffers
            threads (int, optional): Number of threads to use for detection. Defaults to 4.
        """
        self.tag_def = tag_def
        self.frame_queue = frame_queue
        self.results_queue = results_queue
        self.frame_buffers = frame_buffers
        self.threads = threads

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

    def _worker(self):
        
        detector = apriltag.apriltag(self.tag_def.family, threads=self.threads) # pyright: ignore[reportArgumentType]

        proc_start = time_ns()
        proc_end = time_ns()

        buffers:dict[str, np.ndarray] = {name:value.asNumpy() for name, value in self.frame_buffers.items()}
        
        while not self.event.is_set():
            try:
                frame:Frame = self.frame_queue.get(timeout=1)
            except queue.Empty as e:
                print(f"Frame queue timed out")
            else:
                proc_start = time_ns()

                if frame.buffer_name in buffers:
                    buffer = buffers[frame.buffer_name]

                    working_buffer = cv2.cvtColor(buffer, cv2.COLOR_BGR2GRAY)

                    # Detect Apriltags
                    results:list[ApriltagDetection] = []

                    for det in detector.detect(working_buffer):
                        pose = detector.estimate_tag_pose(
                            det, 
                            self.tag_def.tagsize, 
                            frame.camera.intrinsics.fx, 
                            frame.camera.intrinsics.fy, 
                            frame.camera.intrinsics.cx, 
                            frame.camera.intrinsics.cy)
                        results.append(ApriltagDetection(det, pose))

                    proc_end = time_ns()

                    self.results_queue.put(ApriltagResult(frame, results, proc_end - proc_start))
                else:
                    print(f"Unknown buffer '{frame.buffer_name}' provided")


                



            
