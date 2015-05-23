import os
import unittest
import pytest
from build_bot_project.languages.cs_language import CSLanguage
from common.cmd_utils import find_tool, shell, split_lines, screen_str


test_name = __name__


@pytest.mark.usefixtures("test_build_directory_fixture", "test_config_fixture")
class CSLanguageTests(unittest.TestCase):
    def setUp(self):
        self.cs_language_without_config = CSLanguage()
        self.test_file_name = "cs_basic"
        self.test_src_name = self.test_file_name + ".cs"
        self.test_exe_name = self.test_file_name + ".exe"

        self.test_src_file_path = os.path.join(self.src_code_dir, self.test_src_name)
        self.test_exe_file_path = os.path.join(self.build_dir_bin, self.test_exe_name)

    def test_are_all_fixture_attributes_set(self):
        assert hasattr(self, "build_dir")
        assert hasattr(self, "build_dir_bin")
        assert hasattr(self, "src_code_dir")
        assert hasattr(self, "config_parser")
        assert hasattr(self, "is_config_read_ok")
        assert hasattr(self, "cs_compiler_path")

    def test_can_find_build_dir_bin(self):
        self.assertTrue(os.path.exists(self.build_dir_bin))

    def test_can_find_test_src_file(self):
        self.assertTrue(os.path.exists(self.test_src_file_path))

    def test_can_create_cs_language_without_config(self):
        self.assertIsNotNone(self.cs_language_without_config)

    def test_can_get_default_cs_compiler_path(self):
        self.assertEquals(self.cs_language_without_config.get_compiler_path(), CSLanguage.DEFAULT_COMPILER_PATH)

    def test_is_default_compiler_path_exists(self):
        self.assertTrue(os.path.exists(self.cs_compiler_path))

    def test_can_find_csc(self):
        cs_language_with_config = CSLanguage(self.config_parser)
        (is_found, path) = find_tool("csc")
        self.assertTrue(is_found)
        self.assertEquals(path.pop(0), cs_language_with_config.compiler_path)

    def test_can_successfully_call_csc_only(self):
        cs_language_with_config = CSLanguage(self.config_parser)
        (ret_code, out, err) = shell(cs_language_with_config.compiler_path + " -help")
        self.assertEquals(ret_code, 0)

    def test_can_successfully_call_csc_to_compile_test_file(self):
        cs_language_with_config = CSLanguage(self.config_parser)
        (ret_code, out, err) = self._compile(cs_language_with_config)
        self.assertEquals(ret_code, 0)
        self.assertTrue(os.path.exists(self.test_exe_file_path))

    def test_can_successfully_compile_and_run_test_file(self):
        cs_language_with_config = CSLanguage(self.config_parser)
        self._compile(cs_language_with_config)
        (ret_code, out, err) = shell(self.test_exe_file_path)
        self.assertEquals(ret_code, 0)
        self.assertEquals(split_lines(out).pop(0), "Hello World using C#!")

    def test_can_successfully_compile_and_run_test_file_with_config(self):
        cs_language_with_config = CSLanguage(self.config_parser)
        self._compile(cs_language_with_config)
        (ret_code, out, err) = shell(self.test_exe_file_path)
        self.assertEquals(ret_code, 0)
        self.assertEquals(split_lines(out).pop(0), "Hello World using C#!")

    def _compile(self, language):
        compile_cmd = screen_str(
            language.compiler_path) + " /debug+ /out:" + self.test_exe_file_path + " " + self.test_src_file_path
        return shell(compile_cmd)