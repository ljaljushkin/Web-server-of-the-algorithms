from languages.language import Language


class FPLanguage(Language):

    COMPILER_PATH = "/path/to/cs/compiler"

    def get_compiler_path(self):
        return self.COMPILER_PATH