
import numpy as np
from Frame import Frame


class ApriltagDetection:
    """ Stores a single april tag detection and pose pair
    """
    def __init__(self, detection, pose):

        self.detection = detection
        self.pose = pose

    def get_dist(self) -> float:
        """ Calculates the distance to the april tag from the camera

        Returns:
            float: distance to the april tag from the camera
        """
        return float(np.linalg.norm(self.pose['t']))

class ApriltagResult:
    """ Stores the results of an apriltag detection from a single frame"""
    def __init__(self, frame:Frame, detections: list[ApriltagDetection], proc_period:int):
        """ Constructor

        Args:
            frame (Frame): Frame used to detect april tags
            detections (list[ApriltagDetection]): list of april tag detections
            proc_period (float): processing time in nano seconds
        """
        self.frame = frame
        self.detections = detections
        self.proc_period = proc_period