import re


class Messenger:
    def __init__(self, service, connect):
        self.service = service
        self.connect = connect
        self.connection_status = False
        self.ipv4_regex = '^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])([.](?!$)|$)){4}$'
        self.ipv6_regex = '(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1' \
                          ',4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([' \
                          '0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA' \
                          '-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4' \
                          '}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2' \
                          '}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F' \
                          ']{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a' \
                          '-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:' \
                          '){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])[.]){3,3}' \
                          '(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,' \
                          '4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])[.]){' \
                          '3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'

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
                self.message, self.server = message, server
                return 0
            return 2
        return 1

    @staticmethod
    def __validate_message__(message):
        if type(message) is str:
            return True
        return False

    def __validate_server__(self, server):
        if type(server) is str:
            ip, port = server.rsplit(':', 1)
            if (re.match(self.ipv4_regex, ip) or re.match(self.ipv6_regex, ip)) and port.isdigit() and int(
                    port) <= 65525:
                return True
        return False

    def establish_http_and_send(self, http):
        conn = http.HTTPSConnection(self.server)
        conn.request("POST", "/message", self.message)
        response = conn.getresponse()
        print(response)
        conn.close()
        if response != 200:
            return 1
        return 0
