import abc


class Language:
    @abc.abstractmethod
    def get_compiler_path(self):
        pass