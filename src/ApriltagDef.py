

class ApriltagDef:
    """ Defines an AprilTag """

    def __init__(self, tagsize: float, family:str="tag36h11"):
        """ Constructor

        Args:
            tagsize (float): size of the apriltag in meters
            family (str): Apriltag family name
        """

        self.family = family
        self.tagsize = tagsize
