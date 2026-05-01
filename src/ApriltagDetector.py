

from multiprocessing import Event, Process, Queue
import queue
from time import time_ns
from typing import Any, Optional

import apriltag
import cv2
import numpy as np

from ApriltagDef import ApriltagDef
from CameraFrame import CameraFrame
from ApriltagResult import ApriltagDetection, ApriltagResult


class ApriltagDetector:

    def __init__(self, tag_def: ApriltagDef, decimate:int=2, threads: int = 4):
        """ Constructor

        Args:
            tag_def (ApriltagDef): Definition of the apriltag to detect
            threads (int, optional): Number of threads to use for detection. Defaults to 4.
        """
        self.tag_def = tag_def
        self.threads = threads

        self.detector = apriltag.apriltag(self.tag_def.family, threads=self.threads,decimate=decimate) # pyright: ignore[reportArgumentType]

    def __del__(self):

        # Close all opencv windows
        cv2.destroyAllWindows()

    def detect(self, frame: CameraFrame) -> ApriltagResult:
        """ Runs AprilTag detection on a frame

        Args:
            frame (Frame): Frame in which to detect AprilTags

        Returns:
            ApriltagResult: AprilTag detection result
        """
        start_time = time_ns()

        # Convert frame to grayscale
        working_buffer: np.ndarray = cv2.cvtColor(frame.frame_as_np(), cv2.COLOR_YUV2GRAY_YUNV)
        # TODO Move this to the frame capture step

        # Detect Apriltags
        results: list[ApriltagDetection] = [
            ApriltagDetection(det, self.detector.estimate_tag_pose(
                det,
                self.tag_def.tagsize,
                frame.camera.intrinsics.fx,
                frame.camera.intrinsics.fy,
                frame.camera.intrinsics.cx,
                frame.camera.intrinsics.cy))
            for det in self.detector.detect(working_buffer)]

        return ApriltagResult(frame, results, (time_ns() - start_time) * 1e-9)
    

