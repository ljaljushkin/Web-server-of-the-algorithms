from abc import abstractmethod


class ITestBot:
    def __init__(self):
        pass

    @abstractmethod
    def run(self, file, run_string):
        pass