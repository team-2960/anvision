import fastapi.responses
import uvicorn
import cv2

from threading import Lock, Event

from ApriltagResult import ApriltagResult

VIDEO_PREFIX = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
VIDEO_SUFFIX = b"\r\n"

INDEX = """\
<!doctype html>
<html lang="en">
<head>
  <link rel="icon" href="data:;base64,iVBORw0KGgo=">
</head>
<body><img src="/stream" /></body>
</html>
"""

app = fastapi.FastAPI()

class ResultMonitor:
    def __init__(self):
        self.result:Optional[ApriltagResult] = None
        self.lock = Lock()
        self.event = Event()

    def set_result(self, result:ApriltagResult):
        with self.lock:
            self.result = result
            self.event.set()

    async def gen_result_frames(self):
        while True:
            self.event.wait()

            with self.lock:
                ret, buffer = cv2.imencode('.jpg', self.result.gen_result_image())
                frame = buffer.tobytes()
                stream = b"".join((VIDEO_PREFIX, bytes(frame), VIDEO_SUFFIX))
                
                yield stream 


result_monitor = ResultMonitor()

def add_result(result:ApriltagResult):
    result_monitor.set_result(result)

@app.get("/")
async def index():
    return fastapi.responses.HTMLResponse(INDEX)

@app.get("/stream")
async def serve_video_result():
    return fastapi.responses.StreamingResponse(result_monitor.gen_result_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


def start_web_ui():
    uvicorn.run(app,  host="0.0.0.0",port=8080)