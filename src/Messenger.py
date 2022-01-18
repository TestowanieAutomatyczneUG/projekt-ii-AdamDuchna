import re


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
            if self.__validate_message__(message) and self.__validate_server__(server):
                return 0
            return 2
        return 1

    @staticmethod
    def __validate_message__(message):
        if type(message) is str:
            return True
        return False

    @staticmethod
    def __validate_server__(server):
        if type(server) is str:
            ip, port = server.rsplit(':', 1)
            if re.match('^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])([.](?!$)|$)){4}$',
                        ip) and port.isdigit() and int(port) <= 65525:
                return True
            return False
        return False
