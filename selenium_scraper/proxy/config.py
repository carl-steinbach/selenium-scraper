class ProxyConfig:
    def __init__(self, host, port, scheme, locations, username, password, provider) -> None:
        self.host = host
        self.port = port
        self.scheme = scheme
        self.locations = locations
        self.username = username
        self.password = password
        self.provider = provider


def load_proxy_config(proxy_dict) -> ProxyConfig:
    return ProxyConfig(
        host=proxy_dict["host"],
        port=proxy_dict["port"],
        scheme=proxy_dict["scheme"],
        locations=proxy_dict["locations"],
        username=proxy_dict["username"],
        password=proxy_dict["password"],
        provider=proxy_dict["provider"]
    )
