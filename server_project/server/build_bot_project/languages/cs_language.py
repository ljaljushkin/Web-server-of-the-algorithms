import os
from build_bot_project.languages.ilanguage import ILanguage


class CSLanguage(ILanguage):

    COMPILER_FILE = "cs_compiler.exe"

    DEFAULT_COMPILER_DIR = "/path/to/cs/compiler"
    DEFAULT_COMPILER_PATH = os.path.join(DEFAULT_COMPILER_DIR, COMPILER_FILE)

    def __init__(self, config_parser=None):
        ILanguage.__init__(self)
        self.compiler_dir = self.DEFAULT_COMPILER_DIR
        self.compiler_path = os.path.join(self.compiler_dir, self.COMPILER_FILE)
        if config_parser:
            compiler_dir = config_parser.get('compiler_paths', 'cs_path')
            if compiler_dir:
                self.compiler_dir = compiler_dir

    def get_compiler_path(self):
        return self.compiler_path

    def get_build_command(self, code_path, exe_path):
        pass