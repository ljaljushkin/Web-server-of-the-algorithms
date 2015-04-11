from languages.language import Language


class CPPLanguage(Language):
    VS_PATH = "C:\\Program Files (x86)\\Microsoft Visual Studio 10.0\\VC\\"
    COMPILER_PATH = VS_PATH + "bin\\cl.exe"
    VCVARSALL_PATH = VS_PATH + "vcvarsall.bat"

    def get_compiler_path(self):
        return self.COMPILER_PATH
