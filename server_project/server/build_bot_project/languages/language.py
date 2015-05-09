import abc


class Language:
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_compiler_path(self):
        pass

    @abc.abstractmethod
    def get_build_command(self, code_path, exe_path):
        pass