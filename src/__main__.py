from threading import Thread

from ApriltagDef import ApriltagDef
from ApriltagDetector import ApriltagDetector
from FrameGrabber import FrameGrabber
from Camera import Camera, Intrinsics

import web


camera = Camera(
    name="Webcam",
    path_id=0,
    x_res=1280,
    y_res=960,
    fps=30,
    intrinsics=Intrinsics(
        fx=1405.0193204446784,
        fy=1414.9276311038998,
        cx=621.6754139679053,
        cy=469.8431794550814
    ))

tag_def = ApriltagDef(family="tag36h11", tagsize=0.2667)

def process(camera: Camera, tag_def:ApriltagDef):
    frameGrabber = FrameGrabber(camera)
    detector = ApriltagDetector(tag_def)

    for frame in frameGrabber.capture():
        result = detector.detect(frame)
        web.add_result(result)
    

def main():
    thread = Thread(target=process, args=(camera, tag_def))
    thread.start()

    web.start_web_ui()

    thread.join()


if __name__ == "__main__":
    main()
