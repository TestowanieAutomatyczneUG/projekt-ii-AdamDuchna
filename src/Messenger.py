class Messenger:
    def __init__(self, service, connect):
        self.service = service
        self.connect = connect
        self.connection_status = False

    def establish_service(self):
        try:
            state = self.connect(self.service)
            self.connection_status = not bool(state)
            return state
        except Exception:
            return 1

    def send_data(self, message, server):
        if self.connection_status and self.__validate_message__(message):
            return 0
        return 2

    @staticmethod
    def __validate_message__(message):
        if type(message) is str:
            return True
        return False