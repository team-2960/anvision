
from linuxpy.video.device import Capability, Device, PixelFormat, VideoCapture

class Camera:
    """ Contains the details for a camera """
    def __init__(self, name: str, path_id: int|str, x_res:int, y_res:int, fps:int, intrinsics:'Intrinsics'):
        self.name = name
        self.path_id = path_id
        self.x_res = x_res
        self.y_res = y_res
        self.fps = fps
        self.intrinsics = intrinsics

    def get_frame_shape(self) -> tuple[int, int, int]:
        return (self.x_res, self.y_res, 3)

    def get_device(self) -> Device:
        if isinstance(self.path_id, int):
            return Device.from_id(self.path_id)
        else:
            return Device(self.path_id)

class Intrinsics:
    """ Contains a camera's intrinsic values """
    def __init__(self, fx:float, fy:float, cx:float, cy:float):
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy