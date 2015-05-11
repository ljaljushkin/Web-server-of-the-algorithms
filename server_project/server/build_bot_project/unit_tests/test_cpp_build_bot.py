import os
import unittest

import pytest

from build_bot_project.build_bot import BuildBot
from common.cmd_utils import shell
from common.cmd_utils import split_lines
from build_bot_project.languages.cpp_language import CPPLanguage


test_name = __name__


@pytest.mark.usefixtures("test_build_directory_fixture", "test_config_fixture")
class CppBuildBotTests(unittest.TestCase):
    def setUp(self):
        self.test_file_name = "basic"
        self.test_src_name = self.test_file_name + ".cpp"
        self.test_exe_name = self.test_file_name + ".exe"

        self.test_src_file_path = os.path.join(self.src_code_dir, self.test_src_name)

        self.output_dir = os.path.join(self.build_dir, "cfg_output_dir")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.test_exe_path = os.path.join(self.output_dir, self.test_exe_name)

        self.language = CPPLanguage(self.config_parser)
        self.build_bot = BuildBot(self.language)

    def test_are_all_fixture_attributes_set(self):
        assert hasattr(self, "build_dir")
        assert hasattr(self, "build_dir_bin")
        assert hasattr(self, "src_code_dir")
        assert hasattr(self, "config_parser")
        assert hasattr(self, "is_config_read_ok")

    def test_can_successfully_run_build_bot(self):
        (ret_code, out, err) = self.build_bot.build(self.test_src_file_path, self.test_exe_path)
        self.assertEquals(ret_code, 0)

    def test_does_exist_exe_file_created_by_build_bot(self):
        self.build_bot.build(self.test_src_file_path, self.test_exe_path)
        self.assertTrue(os.path.exists(self.test_exe_path))

    def test_can_successfully_run_created_exe_file(self):
        self.build_bot.build(self.test_src_file_path, self.test_exe_path)
        (ret_code, out, err) = shell(self.test_exe_path)
        self.assertEquals(ret_code, 0)
        self.assertEquals(split_lines(out).pop(0), "This is a native C++ program.")
