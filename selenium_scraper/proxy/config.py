

class ProxyConfig():
    def __init__(self, host, port, scheme, locations, username, password, provider) -> None:
        self.host = host
        self.port = port
        self.scheme = scheme
        self.locations = locations
        self.username = username
        self.password = password
        self.provider = provider


def loadProxyConfig(proxyDict) -> ProxyConfig:
    return ProxyConfig(
            host=proxyDict["host"], 
            port=proxyDict["port"], 
            scheme=proxyDict["scheme"], 
            locations=proxyDict["locations"], 
            username=proxyDict["username"], 
            password=proxyDict["password"], 
            provider=proxyDict["provider"]
        )
