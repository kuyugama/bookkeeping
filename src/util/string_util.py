def snake_to_camel(source: str, sep: str = "_") -> str:
    return "".join(word[0].upper() + word[1:] for word in source.split(sep) if word)
