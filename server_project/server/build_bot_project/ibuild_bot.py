from abc import abstractmethod
from build_bot_project.languages.ilanguage import ILanguage


class IBuildBot:
    def __init__(self):
        self.language = ILanguage()

    @abstractmethod
    def build(self, code_path, exe_path):
        pass

