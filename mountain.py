from enums import Province, County, string_to_enum
from utils.string import sanitise_string


class Mountain:

    province: Province
    county: County
    name: str
    height: int
    hiked: list[str]

    def __init__(self, province: str, county: str, name: str, height: int, hiked: list = None) -> None:
        if hiked:
            hiked.sort()

        self.province = string_to_enum(province, Province)
        self.county = string_to_enum(county, County)
        self.name = sanitise_string(name)
        self.height = int(height)
        self.hiked = [] if hiked is None else hiked

    def __lt__(self, other):
        if self.province == other.province:
            return self.height < other.height
        else:
            return self.province < other.province

    def __repr__(self) -> str:
        if not self.hiked:
            return f"> * {self.name}, Co. {self.county.value}: {self.height}m."
        else:
            return f"> * {self.name}, Co. {self.county.value}: {self.height}m.\n>  * Hiked by {", ".join(self.hiked)}."

    def __dict__(self) -> dict:
        return {
            "province": self.province,
            "county": self.county,
            "name": self.name,
            "height": self.height,
            "hiked": self.hiked,
        }

    def set_province(self, province: str) -> None:
        self.province = string_to_enum(province, Province)

    def set_county(self, county: str) -> None:
        self.county = string_to_enum(county, County)

    def set_name(self, name: str) -> None:
        self.name = sanitise_string(name)

    def set_height(self, height: int or float) -> None:
        self.height = int(height)

    def set_hiked(self, hiked: list) -> None:
        hiked.sort()
        self.hiked = hiked

    def set_attrs(self,
                  province: str = "", county: str = "", name: str = "", height: int = 0, hiked: list = None) -> None:

        if province:
            self.set_province(province)
        if county:
            self.set_county(county)
        if name:
            self.set_name(name)
        if height:
            self.set_height(height)
        if hiked:
            self.set_hiked(hiked)

    def copy(self):
        """
        return [
            self.province.value,
            self.county.value,
            self.name,
            self.height,
            self.hiked
        ]"""
        return type(self)(self.province.value, self.county.value, self.name, self.height, self.hiked)


class MountainList:

    mountain_dict: dict

    def __init__(self, mountains: dict) -> None:
        self.mountain_dict = {}
        for key in mountains:
            self.mountain_dict[key] = []
            for mountain in mountains[key]:

                province: str = key
                county: str = mountains[key][mountain].get("county", "ERROR")
                name: str = mountain
                height: int = mountains[key][mountain]["height"]
                hiked: list[str] = mountains[key][mountain]["hiked"]

                mtn = Mountain(province, county, name, height, hiked)
                self.mountain_dict[key].append(mtn)

    def __repr__(self) -> str:
        if not self.mountain_dict:
            return "No mountains!"
        else:
            mountains: list[str] = []
            for key in self.mountain_dict:
                self.mountain_dict[key].sort()
                division = f"# {key}\n"
                division += f"\n".join(str(mountain) for mountain in self.mountain_dict[key])
                mountains.append(division)
            mountains.sort()
            mountains_str = f"\n".join(mnt for mnt in mountains)
            return mountains_str

    def push_back(self, mountain: Mountain) -> None:
        if mountain.province.value in self.mountain_dict:
            self.mountain_dict[mountain.province.value].append(mountain)
        else:
            self.mountain_dict[mountain.province.value] = [mountain]

    def erase(self, name: str) -> bool:
        removed: bool = False

        for key in self.mountain_dict:
            for i, mountain in enumerate(self.mountain_dict[key]):
                if mountain.name == name:
                    self.mountain_dict[key].remove(mountain)
                    removed = True
            if not self.mountain_dict[key]:
                self.mountain_dict.pop(key)
                break

        return removed

    def find(self, name: str) -> Mountain:
        for key in self.mountain_dict:
            for mountain in self.mountain_dict[key]:
                if mountain.name == name:
                    return mountain
        return Mountain("ERROR", "ERROR", "", 0)

    def get_dict(self) -> dict:
        return self.mountain_dict
