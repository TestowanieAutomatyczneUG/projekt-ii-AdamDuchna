class Messenger:
    def __init__(self, service, connect):
        self.service = service
        self.connect = connect
    def establish_service(self):
        try:
            return self.connect(self.service)
        except Exception:
            return 1

