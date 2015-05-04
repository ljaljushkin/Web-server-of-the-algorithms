from abc import abstractmethod


class IBuildBot:
    def __init__(self, language, config_parser):
        self.language = language
        self.config_parser = config_parser

    @abstractmethod
    def build(self, code_path, exe_path):
        pass

