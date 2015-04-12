import os
from languages.language import Language
import configparser


class CPPLanguage(Language):

    COMPILER_FILE = "cl.exe"
    VC_BAT_FILE = "vcvarsall.bat"

    DEFAULT_COMPILER_DIR = "C:\\Program Files (x86)\\Microsoft Visual Studio 10.0\\VC\\bin"
    DEFAULT_VC_BAT_PATH = os.path.join(os.path.dirname(DEFAULT_COMPILER_DIR), VC_BAT_FILE)
    DEFAULT_COMPILER_PATH = os.path.join(DEFAULT_COMPILER_DIR, COMPILER_FILE)

    def __init__(self, config_parser=None):

        self.compiler_dir = self.DEFAULT_COMPILER_DIR
        if config_parser:
            compiler_dir = config_parser.get('compiler_paths', 'cpp_path')
            if compiler_dir:
                self.compiler_dir = compiler_dir

        self.compiler_path = os.path.join(self.compiler_dir, self.COMPILER_FILE)
        self.vc_bat_path = os.path.join(os.path.dirname(self.compiler_dir), self.VC_BAT_FILE)

    def get_compiler_path(self):
        return self.compiler_path

    def get_vc_bat_path(self):
        return self.vc_bat_path
