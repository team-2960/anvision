from multiprocessing import Queue

from ApriltagDef import ApriltagDef
from ApriltagDetector import ApriltagDetector
from FrameGrabber import FrameGrabber
from Camera import Camera, Intrinsics
from FrameBuffer import FrameBuffer
from ApriltagResultViewer import ApriltagResultViewer
from Frame import Frame
from ApriltagResult import ApriltagResult

camera = Camera(
    name="Webcam",
    path_index=0,
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

def main():
    # Setup Inter
    frame_queue:Queue = Queue()
    result_queue:Queue = Queue()

    buffers = {f"{camera.name} buffer {i}":FrameBuffer(camera) for i in range(10)}

    frameGrabber = FrameGrabber(camera, frame_queue, buffers)
    detector = ApriltagDetector(tag_def, frame_queue, result_queue, buffers)
    viewer = ApriltagResultViewer(result_queue, buffers)

    frameGrabber.start()
    detector.start()

    viewer.view_results()

    frameGrabber.stop()
    detector.stop()

    frameGrabber.wait_on_stop()
    detector.wait_on_stop()


if __name__ == "__main__":
    main()
