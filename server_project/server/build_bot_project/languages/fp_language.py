import os
from build_bot_project.languages.ilanguage import ILanguage


class FPLanguage(ILanguage):

    COMPILER_FILE = "fp_compiler.exe"

    DEFAULT_COMPILER_DIR = "/path/to/fp/compiler"
    DEFAULT_COMPILER_PATH = os.path.join(DEFAULT_COMPILER_DIR, COMPILER_FILE)

    def __init__(self, config_parser=None):
        ILanguage.__init__(self)
        self.compiler_dir = self.DEFAULT_COMPILER_DIR
        self.compiler_path = os.path.join(self.compiler_dir, self.COMPILER_FILE)
        if config_parser:
            compiler_dir = config_parser.get('compiler_paths', 'fp_path')
            if compiler_dir:
                self.compiler_dir = compiler_dir

    def get_compiler_path(self):
        return self.compiler_path

    def get_build_command(self, code_path, exe_path):
        pass

    @staticmethod
    def get_extension(**kwargs):
        return "pas"

    @staticmethod
    def get_name(**kwargs):
        return "Free Pascal"