from cmd_utils import shell
from ibuild_bot import IBuildBot


class BuildBot(IBuildBot):
    def __init__(self, language, config_parser):
        IBuildBot.__init__(self, language, config_parser)

    def build(self, code_path, exe_path):
        compile_cmd = self.language.get_build_command(code_path, exe_path)
        return shell(compile_cmd)