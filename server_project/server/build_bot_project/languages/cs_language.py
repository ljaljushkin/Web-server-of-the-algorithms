import os
from build_bot_project.languages.ilanguage import ILanguage
from common.cmd_utils import screen_str


class CSLanguage(ILanguage):
    COMPILER_FILE = "csc.exe"

    DEFAULT_COMPILER_DIR = "C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319"
    DEFAULT_COMPILER_PATH = os.path.join(DEFAULT_COMPILER_DIR, COMPILER_FILE)

    def __init__(self, config_parser=None):
        ILanguage.__init__(self)
        self.compiler_dir = self.DEFAULT_COMPILER_DIR

        if config_parser:
            compiler_dir = config_parser.get('compiler_paths', 'cs_path')
            if compiler_dir:
                self.compiler_dir = compiler_dir
        self.compiler_path = os.path.join(self.compiler_dir, self.COMPILER_FILE)

    def get_compiler_path(self):
        return self.compiler_path

    def get_build_command(self, code_path, exe_path):
        compile_cmd = screen_str(self.compiler_path) \
                      + " /debug+" \
                      + " /out:" + exe_path \
                      + " " + code_path
        return compile_cmd
