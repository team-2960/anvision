from ApriltagDef import ApriltagDef
from ApriltagDetector import ApriltagDetector
from FrameGrabber import FrameGrabber
from Camera import Camera, Intrinsics

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

def main():
    # Setup Inter

    frameGrabber = FrameGrabber(camera)
    detector = ApriltagDetector(tag_def)

    for frame in frameGrabber.capture():
        result = detector.detect(frame)
        print(f'Framerate: {frame.camera.fps} Hz')
        print(f'Processing Time: {result.processing_time:.2f} ms')


        # End capture if ESC is pressed
        if result.display() == 27:
            break


if __name__ == "__main__":
    main()
