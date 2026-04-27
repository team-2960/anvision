
import cv2


class Camera:
    """ Contains the details for a camera """
    def __init__(self, name: str, path_index: int|str, x_res:int, y_res:int, fps:int, intrinsics:'Intrinsics'):
        self.name = name
        self.path_index = path_index
        self.x_res = x_res
        self.y_res = y_res
        self.fps = fps
        self.intrinsics = intrinsics

class Intrinsics:
    """ Contains a camera's intrinsic values """
    def __init__(self, fx:float, fy:float, cx:float, cy:float):
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy