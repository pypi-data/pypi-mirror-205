import yaml

Key = int | str


class Texts:
    def __init__(self, path: str) -> None:
        with open(path, encoding="utf8") as stream:
            raw_dict: dict = yaml.unsafe_load(stream)
        self.dict = {k: str(v) for k, v in raw_dict.items()}

    def get_words(self, key: Key) -> list[str]:
        text = self[key]
        return text.split()

    def __getitem__(self, item: Key) -> str:
        if item in self.dict:
            return str(self.dict[item])
        raise TextsKeyError(item)


class TextsKeyError(KeyError):
    def __init__(self, key: Key) -> None:
        self.key = key

    def __str__(self) -> str:
        return f"No text with key `{self.key}`"
