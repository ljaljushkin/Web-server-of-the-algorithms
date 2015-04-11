from abc import abstractmethod


class BuildBot:
    def __init__(self, language):
        self.language = language
        self.compiler_path = self.language.get_compiler_path()

    @abstractmethod
    def build(self):
        pass
