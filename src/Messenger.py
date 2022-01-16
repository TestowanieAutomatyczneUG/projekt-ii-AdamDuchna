class Messenger:
    def __init__(self, service, connect):
        self.service = service
        self.connect = connect
    def establish_service(self):
        return self.connect(self.service)
