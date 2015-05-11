from abc import abstractmethod, abstractproperty, ABCMeta
from build_bot_project.ibuild_bot import IBuildBot


class IAlgorithmController:

    def __init__(self):
        build_bot = IBuildBot()
        pass

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



