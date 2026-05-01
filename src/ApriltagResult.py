
from typing import Any

import cv2
import numpy as np
from CameraFrame import CameraFrame
from cv2 import putText, line, FONT_HERSHEY_SIMPLEX, LINE_AA
from cv2.typing import MatLike


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
    
    def draw_apriltag_graphics(self, img: MatLike, cross_size: int = 6,cross_color=(0, 0, 255)):
        """ Draws an april tag result on an image

        Args:
            img (typing.MatLike): Image to draw the graphics in
            cross_size (int, optional): Length of the center cross mark. Defaults to 6.
            cross_color (tuple, optional): color of the cross mark. Defaults to (0, 0, 255).
        """

        id = self.detection['id']
        center = self.detection['center']
        corners = self.detection['lb-rb-rt-lt']  # pyright: ignore[reportGeneralTypeIssues]

        # Draw ID
        putText(
            img=img,
            text=str(id),
            org=(int(center[0]+10),
                 int(center[1]+10)),
            fontFace=FONT_HERSHEY_SIMPLEX,
            fontScale=float(1),
            color=cross_color,
            thickness=2,
            lineType=LINE_AA)

        # Draw Cross
        line(
            img=img,
            pt1=(int(center[0] - cross_size / 2),
                 int(center[1])),
            pt2=(int(center[0] + cross_size / 2),
                 int(center[1])),
            color=cross_color,
            thickness=1
        )

        line(
            img=img,
            pt1=(int(center[0]), int(
                center[1] - cross_size / 2)),
            pt2=(int(center[0]), int(
                center[1] + cross_size / 2)),
            color=cross_color,
            thickness=1
        )

        # Draw Outline
        line(
            img=img,
            pt1=(int(corners[0][0]), int(corners[0][1])),
            pt2=(int(corners[1][0]), int(corners[1][1])),
            color=(0, 0, 255),
            thickness=1
        )

        line(
            img=img,
            pt1=(int(corners[1][0]), int(corners[1][1])),
            pt2=(int(corners[2][0]), int(corners[2][1])),
            color=(0, 255, 0),
            thickness=1
        )

        line(
            img=img,
            pt1=(int(corners[2][0]), int(corners[2][1])),
            pt2=(int(corners[3][0]), int(corners[3][1])),
            color=(255, 0, 0),
            thickness=1
        )

        line(
            img=img,
            pt1=(int(corners[3][0]), int(corners[3][1])),
            pt2=(int(corners[0][0]), int(corners[0][1])),
            color=(0, 255, 255),
            thickness=1
        )


class ApriltagResult:
    """ Stores the results of an apriltag detection from a single frame"""
    def __init__(self, frame:CameraFrame, detections: list[ApriltagDetection], processing_time:float):
        """ Constructor

        Args:
            frame (Frame): Frame used to detect april tags
            detections (list[ApriltagDetection]): list of april tag detections
            processing_time (float): processing time in seconds
        """
        self.frame = frame
        self.detections = detections
        self.processing_time = processing_time

    
    def display(self, window:str="Result") -> int:
        """ Displays the AprilTag detection result in an OpenCV GUI window. Graphics are drawn on all april tags.

        Args:
            window (str): Name of the window in which to display the result

        Returns:
            int: 0 if no key was pressed, otherwise the key
        """

        # Copy buffer before destructively modifying it
        disp_buffer = cv2.cvtColor(self.frame.frame_as_np(), cv2.COLOR_YUV2BGR_YUYV)

        # Draw graphics for all detected april tags
        for detection in self.detections:
            detection.draw_apriltag_graphics(img=disp_buffer)

        # Show the image
        cv2.imshow(window, disp_buffer)
        return cv2.waitKey(1)