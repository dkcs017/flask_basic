class BrokerConfig():
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @property
    def host(self):
        return self.host

    @host.setter
    def host(self, value):
        self.host = value

    @property
    def port(self):
        return self.port

    @port.setter
    def port(self, value):
        self.port = value
