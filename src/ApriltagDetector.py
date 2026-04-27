

from multiprocessing import Event, Process, Queue
import queue
from time import time_ns
from typing import Any, Optional

import apriltag
import cv2
import numpy as np

from ApriltagDef import ApriltagDef
from Frame import Frame


class ApriltagDetector:

    def __init__(self, tag_def: ApriltagDef, frame_queue: Queue, threads:int=4):
        """ Constructor

        Args:
            tag_def (ApriltagDef): Definition of the apriltag to detect
            frame_queue (Queue): Capture Frame queue
            threads (int, optional): Number of threads to use for detection. Defaults to 4.
        """
        self.tag_def = tag_def
        self.frame_queue = frame_queue
        self.threads = threads

        self.process = Process(target=self.__worker)
        self.event = Event()

    def draw_apriltag_graphics(
        self,
        img: cv2.typing.MatLike,
        detection: Any,  # apriltag.Detection,
        cross_size: int = 6,
        cross_color=(0, 0, 255)):

        id = detection['id']
        center = detection['center']
        corners = detection['lb-rb-rt-lt']

        # Draw ID
        cv2.putText(
            img=img,
            text=str(id),
            org=(int(center[0]+10),
                int(center[1]+10)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=float(1),
            color=cross_color,
            thickness=2,
            lineType=cv2.LINE_AA)

        # Draw Cross
        cv2.line(
            img=img,
            pt1=(int(center[0] - cross_size / 2),
                int(center[1])),
            pt2=(int(center[0] + cross_size / 2),
                int(center[1])),
            color=cross_color,
            thickness=1
        )

        cv2.line(
            img=img,
            pt1=(int(center[0]), int(
                center[1] - cross_size / 2)),
            pt2=(int(center[0]), int(
                center[1] + cross_size / 2)),
            color=cross_color,
            thickness=1
        )

        # Draw Outline
        cv2.line(
            img=img,
            pt1=(int(corners[0][0]), int(corners[0][1])),
            pt2=(int(corners[1][0]), int(corners[1][1])),
            color=(0, 0, 255),
            thickness=1
        )

        cv2.line(
            img=img,
            pt1=(int(corners[1][0]), int(corners[1][1])),
            pt2=(int(corners[2][0]), int(corners[2][1])),
            color=(0, 255, 0),
            thickness=1
        )

        cv2.line(
            img=img,
            pt1=(int(corners[2][0]), int(corners[2][1])),
            pt2=(int(corners[3][0]), int(corners[3][1])),
            color=(255, 0, 0),
            thickness=1
        )

        cv2.line(
            img=img,
            pt1=(int(corners[3][0]), int(corners[3][1])),
            pt2=(int(corners[0][0]), int(corners[0][1])),
            color=(0, 255, 255),
            thickness=1
        )

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

    def __worker(self):
        
        detector = apriltag.apriltag(self.tag_def.family, threads=self.threads) # pyright: ignore[reportArgumentType]

        prev_frame_ts = 0
        proc_start = time_ns()
        proc_end = time_ns()

        while not self.event.is_set():
            try:
                frame:Frame = self.frame_queue.get(timeout=1)
            except queue.Empty as e:
                print(f"Frame queue timed out")
            else:
                proc_start = time_ns()
                # Detect Apriltags
                detections = detector.detect(frame.buffer) # pyright: ignore[reportArgumentType]

                # Parse Apriltag detections
                for det in detections:
                    pose = detector.estimate_tag_pose(
                        detection=det, 
                        tagsize=self.tag_def.tagsize, 
                        fx=frame.camera.intrinsics.fx, 
                        fy=frame.camera.intrinsics.fy, 
                        cx=frame.camera.intrinsics.cx, 
                        cy=frame.camera.intrinsics.cy)
                    
                    dist = np.linalg.norm(pose['t'])

                    print(f"Tag {det['id']} Distance: {dist:.2f}m ", flush=True)

                # TODO Add AprilTag Results queue

                proc_end = time_ns()
                

                frame_period = (frame.timestamp - prev_frame_ts) * 1e-6
                prev_frame_ts = frame.timestamp
                frame_rate = 1.0 / frame_period 
                proc_period = (proc_end - proc_start) * 1e-9

                print(f"Frame Period: {frame_period:.6f} s", flush=True)
                print(f"Frame Rate: {frame_rate:.2f} hz", flush=True)
                print(f"Proc Period: {proc_period:.6f} s", flush=True)
                print(f"Overrun: {proc_period > frame_period}", flush=True) 
                print(f"Queue Len: {self.frame_queue.qsize()}", flush=True)


                



            
