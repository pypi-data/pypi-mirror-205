translation_table = {
                ord('æ'): 'a',
                ord('ø'): 'o',
                ord('å'): 'a',
                ord('Æ'): 'A',
                ord('Ø'): 'O',
                ord('Å'): 'A'
            }


def translate(word: str) -> str:
    return word.translate(translation_table)


class Model:
    def __init__(self, name: str):
        self.name: str = translate(name)
        self.writeable: bool = False
        self.abstract: bool = False
        self.common: bool = False
        self.connectors: list[str] = []
