from Camera import Camera


class Frame:

    """ Stores details of a single camera frame """

    def __init__(self, camera: Camera, buffer_name: str, timestamp: int):
        """ Constructor

        Args:
            camera (Camera): Camera source for the frame
            buffer_name (str): name of the buffer storing the image
            timestamp (int): Epoch timestamp the image was captured in micro seconds
        """
        self.camera = camera
        self.buffer_name = buffer_name
        self.timestamp = timestamp

        
