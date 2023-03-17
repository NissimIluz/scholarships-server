from server.constants.database_constants import database_responses


class DatabaseResponse:
    def __init__(self, status: bool = True, message=database_responses.Responses.Succeeded, information=None):
        self.status = status
        self.message = message
        self.information = information
