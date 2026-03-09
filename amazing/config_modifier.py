from typing import Dict, Any
from copy import deepcopy
from maze.parsing import parsing, convert_type, validate_data


def modify_config(k: str, v: str) -> None:
    '''Get new value and update the dictionary'''
    actual_config = parsing()
    old_config = deepcopy(actual_config)
    k = k.upper().strip()
    v = v.strip()
    actual_config[k] = v
    new_config = convert_type(actual_config)
    try:
        validate_data(new_config)
        save_config(actual_config)
    except Exception as e:
        actual_config = old_config
        print(e)


def save_config(datas: Dict[str, Any]) -> None:
    '''Save new config into the file'''
    with open("config.txt", "w") as f:
        for k, v in datas.items():
            f.write(f"{k}={v}\n")
