import os
from languages.language import Language


class CSLanguage(Language):

    COMPILER_FILE = "cs_compiler.exe"

    DEFAULT_COMPILER_DIR = "/path/to/cs/compiler"
    DEFAULT_COMPILER_PATH = os.path.join(DEFAULT_COMPILER_DIR, COMPILER_FILE)

    def get_compiler_path(self):
        return self.DEFAULT_COMPILER_PATH