from abc import abstractmethod
from build_bot_project.ibuild_bot import IBuildBot
from test_bot_project.itest_bot import ITestBot


class IAlgorithmController:

    def __init__(self):
        build_bot = IBuildBot()
        test_bot = ITestBot()

    @abstractmethod
    def add_algorithm(self, algorithm):
        pass

    @abstractmethod
    def run_algorithm(self, name):
        pass

    @abstractmethod
    def get_algorithm(self, name):
        pass

    @abstractmethod
    def update_algorithm(self, algorithm):
        pass

    @abstractmethod
    def search_algorithm(self, name):
        pass

    @abstractmethod
    def remove_algorithm(self, name):
        pass

    @abstractmethod
    def get_algorithms_list(self):
        pass



