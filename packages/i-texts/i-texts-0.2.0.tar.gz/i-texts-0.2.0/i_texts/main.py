import env

from .core import Texts

path = env.get("TEXTS_PATH", None)

if not path:
    locales_path = env.get("LOCALES_PATH", "locales")
    locale = env.get("LOCALE")
    path = f"{locales_path}/{locale}.yml"

texts = Texts(path)
