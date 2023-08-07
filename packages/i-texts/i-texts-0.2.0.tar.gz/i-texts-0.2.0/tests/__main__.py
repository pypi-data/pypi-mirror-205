from i_texts import texts

assert texts.dict == {1: "1", "a": "a", "words": "a b c", "ru": "русский"}
assert texts[1] == "1"
assert texts["a"] == "a"
assert texts.get_words("words") == ["a", "b", "c"]
