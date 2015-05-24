import abc


class ILanguage:
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_compiler_path(self):
        pass

    @abc.abstractmethod
    def get_build_command(self, code_path, exe_path):
        pass

    @staticmethod
    @abc.abstractmethod
    def get_name(**kwargs):
        pass

    @staticmethod
    @abc.abstractmethod
    def get_extension(**kwargs):
        pass