import json

from mountain import MountainList


def serialise_mountain_list(saved_mtns: dict) -> dict:
    mtns_to_save: dict = {}

    for (key, value) in saved_mtns.items():
        mtns_to_save[key] = {}
        for mountain in value:
            mtns_to_save[key][mountain.name] = {
                "height": mountain.height,
                "hiked": mountain.hiked,
                "county": mountain.county.value
            }

    return mtns_to_save


def load_mountains_from_json(path: str) -> MountainList:
    with open(path, 'r') as f:
        try:
            file: dict = json.load(f)
        except json.decoder.JSONDecodeError:
            file: dict = {}

    if not file.get("mountains"):
        saved_mtns: dict = {}
    else:
        saved_mtns: dict = file["mountains"]

    mtns = MountainList(saved_mtns)

    return mtns


def save_mountains_to_json(path: str, mountains: dict) -> None:
    provinces: dict = serialise_mountain_list(mountains)
    data: dict = {"mountains": provinces}

    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
