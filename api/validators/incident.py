from api.models.incident import Incident


class Validators(Incident):
    def validate_inputs(self):
        if not self.title or self.title.isspace():
            return 'Please fill in title field!'
        elif not self.location or self.location.isspace():
            return'Please fill in location field!'
        elif not self._type or self._type.isspace():
            return'Please select incident type!'
        elif not self.createdBy or self.createdBy.isspace():
            return'Please fill in reporter field!'
        elif not self.comment or self.comment.isspace():
            return'Please fill in the comments field!'

    def validate_media(self):
        if not self.images or self.images.isspace():
            return 'Please add images for proof!'
        elif not self.videos or self.videos.isspace():
            return'Please add videos for proof!'
        else:
            return None
