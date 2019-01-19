incidents = []


class Incident:
    """This class contains all incident objects"""

    def __init__(self, *args):
        self._id = args[0]
        self.createdBy = args[1]
        self._type = args[2]
        self.title = args[3]
        self.location = args[4]
        self.comment = args[5]
        self.status = args[6]
        self.createdOn = args[7]
        self.images = args[8]
        self.videos = args[9]