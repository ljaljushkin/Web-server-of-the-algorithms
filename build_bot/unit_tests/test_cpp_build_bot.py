import os
import unittest
import pytest
from build_bot.build_bot import BuildBot
from build_bot.Languages.cpp_language import CPPLanguage
from build_bot.common.cmd_utils import shell, split_lines

test_name = __name__


@pytest.mark.usefixtures("test_config_fixture")
class CppBuildBotTests(unittest.TestCase):
    def setUp(self):
        self.test_file_name = "basic"
        self.test_src_name = self.test_file_name + ".cpp"
        self.test_exe_name = self.test_file_name + ".exe"

        self.test_src_file_path = os.path.join(self.src_code_dir, self.test_src_name)
        self.test_exe_file_path = os.path.join(self.build_dir_bin, self.test_exe_name)

        self.language = CPPLanguage(self.config_parser)
        self.build_bot = BuildBot(self.language, self.config_parser)

    def test_are_all_fixture_attributes_set(self):
        assert hasattr(self, "build_dir")
        assert hasattr(self, "build_dir_bin")
        assert hasattr(self, "src_code_dir")
        assert hasattr(self, "config_parser")
        assert hasattr(self, "is_config_read_ok")

    def test_can_successfully_run_build_bot(self):
        (ret_code, out, err) = self.build_bot.build(self.test_src_file_path, self.test_file_name)
        self.assertEquals(ret_code, 0)

    def test_does_exist_exe_file_created_by_build_bot(self):
        output_dir = self.config_parser.get('build_config', 'output_dir')
        self.build_bot.build(self.test_src_file_path, self.test_file_name)
        self.assertTrue(os.path.exists(output_dir + os.sep + self.test_exe_name))

    def test_can_successfully_run_created_exe_file(self):
        self.build_bot.build(self.test_src_file_path, self.test_file_name)
        output_dir = self.config_parser.get('build_config', 'output_dir')
        (ret_code, out, err) = shell(output_dir + os.sep + self.test_exe_name)
        self.assertEquals(ret_code, 0)
        self.assertEquals(split_lines(out).pop(), "This is a native C++ program.")
