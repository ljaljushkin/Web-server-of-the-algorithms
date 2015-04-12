import os
from languages.language import Language


class FPLanguage(Language):

    COMPILER_FILE = "fp_compiler.exe"

    DEFAULT_COMPILER_DIR = "/path/to/fp/compiler"
    DEFAULT_COMPILER_PATH = os.path.join(DEFAULT_COMPILER_DIR, COMPILER_FILE)

    def get_compiler_path(self):
        return self.DEFAULT_COMPILER_PATH