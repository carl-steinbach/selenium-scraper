class ProxyConfig:
    """information about a proxy,
    `locations` should be a list of country or location names
    `provider` is used to select the algorithm for creating the ZIP file, only packetstream is implemented
    """
    def __init__(self, host, port, scheme, locations, username, password, provider) -> None:
        self.host = host
        self.port = port
        self.scheme = scheme
        self.locations = locations
        self.username = username
        self.password = password
        self.provider = provider
