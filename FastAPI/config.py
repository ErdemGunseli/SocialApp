import json
from typing import Any


def read_config(key: str, path: str = "config.json") -> Any:
    # 'r' means read-only:
    with open(path, 'r') as file:
        return json.load(file).get(key)


def write_config(key: str, value: Any, path: str = "config.json") -> None:
    with open(path, 'r+') as file:
        config = json.load(file)
        config[key] = value
        file.seek(0)
        json.dump(config, file, indent=4)
        file.truncate()
