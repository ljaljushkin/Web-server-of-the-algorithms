from common.cmd_utils import shell, screen_str
from test_bot_project.itest_bot import ITestBot


class TestBot(ITestBot):
    def __init__(self):
        ITestBot.__init__(self)

    def get_run_command(self, file, run_string):
        run_cmd = screen_str(file) \
                      + " " + run_string
        return run_cmd

    def run(self, file, run_string):
        run_cmd = self.get_run_command(file, run_string)
        return shell(run_cmd)
