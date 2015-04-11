from languages.language import Language


class CPPLanguage(Language):
    COMPILER_PATH = "C:\\Program Files (x86)\\Microsoft Visual Studio 10.0\\VC\\bin\\cl.exe"

    def get_compiler_path(self):
        return self.COMPILER_PATH
