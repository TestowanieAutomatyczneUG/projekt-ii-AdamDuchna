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
        if self.connection_status:
            return 0
        return 1
