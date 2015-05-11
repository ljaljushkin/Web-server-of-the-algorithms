from abc import abstractmethod


class ITestBot:
    def __init__(self, config_parser):
        self.config_parser = config_parser

    @abstractmethod
    def run(self, file, run_string):
        pass