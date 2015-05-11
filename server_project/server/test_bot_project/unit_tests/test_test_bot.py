import unittest
import os
import pytest
from common.cmd_utils import split_lines
from test_bot_project.test_bot import TestBot


test_name = __name__


@pytest.mark.usefixtures("test_build_directory_fixture", "test_config_fixture")
class TestBotTests(unittest.TestCase):
    def setUp(self):
        self.test_file_name = "basic"
        self.test_exe_name = self.test_file_name + ".exe"
        self.test_exe_path = os.path.join(self.exe_dir, self.test_exe_name)

    def test_are_all_fixture_attributes_set(self):
        assert hasattr(self, "exe_dir")
        assert hasattr(self, "config_parser")
        assert hasattr(self, "is_config_read_ok")

    def test_can_create_test_bot_with_config(self):
        test_bot = TestBot(self.config_parser)
        self.assertIsNotNone(test_bot)

    def test_can_run_test_bot(self):
        test_bot = TestBot(self.config_parser)
        (ret_code, out, err) = test_bot.run(self.test_exe_path, "")
        self.assertEquals(ret_code, 0)
        self.assertEquals(split_lines(out).pop(0), "This is a native C++ program.")
