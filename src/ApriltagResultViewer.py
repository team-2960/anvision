

from multiprocessing import Queue
from typing import Any

import cv2

import numpy as np

from FrameBuffer import FrameBuffer
from ApriltagResult import ApriltagResult


class ApriltagResultViewer:

    def __init__(self, results_queue: Queue, frame_buffers: dict[str, FrameBuffer]):
        self.results_queue = results_queue
        self.frame_buffers = frame_buffers

    def view_results(self):
        key = 0

        buffers: dict[str, np.ndarray] = {
            name: value.asNumpy() for name, value in self.frame_buffers.items()}

        while key != 27:

            result = None

            while not self.results_queue.empty():
                result = self.results_queue.get()

            if result is not None:

                buffer = None
                if result.frame.buffer_name in buffers:
                    input_buffer = buffers[result.frame.buffer_name]
                    disp_buffer = np.copy(input_buffer)

                    for detection in result.detections:
                        self.draw_apriltag_graphics(
                            disp_buffer, detection.detection)

                    cv2.imshow("Result", disp_buffer)

            key = cv2.waitKey(1)

    def draw_apriltag_graphics(
            self,
            img: cv2.typing.MatLike,
            detection: Any,
            cross_size: int = 6,
            cross_color=(0, 0, 255)):

        id = detection['id']
        center = detection['center']
        corners = detection['lb-rb-rt-lt']  # pyright: ignore[reportGeneralTypeIssues]

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
