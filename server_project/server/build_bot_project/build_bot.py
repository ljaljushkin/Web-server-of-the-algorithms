from build_bot_project.common.cmd_utils import shell
from build_bot_project.ibuild_bot import IBuildBot


class BuildBot(IBuildBot):
    def __init__(self, language, config_parser):
        IBuildBot.__init__(self, language, config_parser)

    def build(self, code_path, exe_path):
        compile_cmd = self.language.get_build_command(code_path, exe_path)
        return shell(compile_cmd)
