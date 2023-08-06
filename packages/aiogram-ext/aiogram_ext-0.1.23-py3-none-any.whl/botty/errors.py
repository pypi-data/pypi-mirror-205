from .deps import BadRequest


class NoSendTextRights(BadRequest):
    msg = "Not enough rights to send text messages to the chat"

    def __str__(self):
        return self.msg


class NoSendPhotoRights(BadRequest):
    msg = "Not enough rights to send photos to the chat"

    def __str__(self):
        return self.msg
