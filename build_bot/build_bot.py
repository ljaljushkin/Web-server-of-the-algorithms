from abc import abstractmethod


class BuildBot:
    @abstractmethod
    def build(self):
        pass
