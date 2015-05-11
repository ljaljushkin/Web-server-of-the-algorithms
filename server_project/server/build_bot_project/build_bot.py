from build_bot_project.languages.cpp_language import CPPLanguage
from common.cmd_utils import shell
from build_bot_project.ibuild_bot import IBuildBot


class BuildBot(IBuildBot):

    def __init__(self):
        IBuildBot.__init__(self)
        self.language = CPPLanguage()

    def build(self, code_path, exe_path):
        compile_cmd = self.language.get_build_command(code_path, exe_path)
        return shell(compile_cmd)

    def set_language(self, language):
        self.language = language