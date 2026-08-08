from api.custom_requester import CustomRequester


class BaseService:
    def __init__(self, requester: CustomRequester):
        self.requester = requester
