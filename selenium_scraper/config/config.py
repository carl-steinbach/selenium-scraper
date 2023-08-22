from python_json_config import ConfigBuilder
import os

configdir = os.path.dirname(os.path.abspath(__file__))
builder = ConfigBuilder()
config = builder.parse_config(os.path.join(configdir, "config.json"))