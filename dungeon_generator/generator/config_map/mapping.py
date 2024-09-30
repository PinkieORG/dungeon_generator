import yaml
from hamingja_dungeon.utils.ascii_dungeon_generator.config.ascii_dungeon_config import \
    ASCIIDungeonConfig
from yaml import Loader


def map_form_data(data: dict, mapping: dict[str, str]):
    """Returns a dictionary where keys are the same as in mapping and values
    are values from data."""
    result = {}
    for key, data_key in mapping.items():
        result[key] = data.get(data_key)
    return result


def unflatten(dictionary: dict):
    result = dict()
    for key, value in dictionary.items():
        parts = key.split(".")
        d = result
        for part in parts[:-1]:
            if part not in d:
                if part == parts[-2] and parts[-1].isnumeric:
                    d[part] = []
                else:
                    d[part] = {}
            d = d[part]
        end = parts[-1]
        if end.isnumeric():
            index = int(end)
            last_index = len(d) - 1
            if last_index < index:
                d.extend([None] * (index - last_index))
            d[index] = value
        else:
            d[end] = value
    return result


def get_dungeon_generator_config(form_data: dict, mapping_file_path: str):
    with open(mapping_file_path, 'r') as file:
        mapping = yaml.load(file, Loader=Loader)
    mapped = map_form_data(form_data, mapping)
    dungeon_config_dict = {
        "dungeon_area": unflatten(mapped)
    }
    return ASCIIDungeonConfig(**dungeon_config_dict)
