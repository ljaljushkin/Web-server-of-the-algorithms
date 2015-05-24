import os
import tempfile

from common.cmd_utils import screen_str
from build_bot_project.languages.ilanguage import ILanguage


class FPLanguage(ILanguage):

    COMPILER_FILE = "fpc.exe"

    DEFAULT_COMPILER_DIR = "C:\\FPC\\2.6.4\\bin\\i386-Win32"
    DEFAULT_COMPILER_PATH = os.path.join(DEFAULT_COMPILER_DIR, COMPILER_FILE)

    def __init__(self, config_parser=None):
        ILanguage.__init__(self)
        self.compiler_dir = self.DEFAULT_COMPILER_DIR

        if config_parser:
            compiler_dir = config_parser.get('compiler_paths', 'fp_path')
            if compiler_dir:
                self.compiler_dir = compiler_dir
        self.compiler_path = os.path.join(self.compiler_dir, self.COMPILER_FILE)

    def get_compiler_path(self):
        return self.compiler_path

    def get_build_command(self, code_path, exe_path):
        exe_dir = os.path.dirname(exe_path)
        temp_dir = tempfile.gettempdir()
        compile_cmd = screen_str(self.compiler_path) \
                      + " -Fo" + temp_dir \
                      + " -FE" + str(exe_dir) \
                      + " " + code_path
        return compile_cmd

    @staticmethod
    def get_extension(**kwargs):
        return "pas"

    @staticmethod
    def get_name(**kwargs):
        return "Free Pascal"