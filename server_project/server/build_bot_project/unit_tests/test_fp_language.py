import os
import unittest
import pytest
from build_bot_project.languages.fp_language import FPLanguage
from common.cmd_utils import find_tool, shell, split_lines, screen_str


@pytest.mark.usefixtures("test_build_directory_fixture", "test_config_fixture")
class FPLanguageTests(unittest.TestCase):
    def setUp(self):
        self.fp_language_without_config = FPLanguage()
        self.test_file_name = "fp_basic"
        self.test_src_name = self.test_file_name + ".pas"
        self.test_exe_name = self.test_file_name + ".exe"

        self.test_src_file_path = os.path.join(self.src_code_dir, self.test_src_name)
        self.test_exe_file_path = self.build_dir_bin

    def test_are_all_fixture_attributes_set(self):
        assert hasattr(self, "build_dir")
        assert hasattr(self, "build_dir_bin")
        assert hasattr(self, "src_code_dir")
        assert hasattr(self, "config_parser")
        assert hasattr(self, "is_config_read_ok")
        assert hasattr(self, "fp_compiler_path")

    def test_can_find_build_dir_bin(self):
        self.assertTrue(os.path.exists(self.build_dir_bin))

    def test_can_find_test_src_file(self):
        self.assertTrue(os.path.exists(self.test_src_file_path))

    def test_can_create_fp_language_without_config(self):
        self.assertIsNotNone(self.fp_language_without_config)

    def test_fp_language_name(self):
        self.assertEqual(self.fp_language_without_config.get_name(), "Free Pascal")

    def test_fp_language_extension(self):
        self.assertEqual(self.fp_language_without_config.get_extension(), "pas")

    def test_can_get_default_fp_compiler_path(self):
        self.assertEquals(self.fp_language_without_config.get_compiler_path(), FPLanguage.DEFAULT_COMPILER_PATH)

    def test_is_default_compiler_path_exists(self):
        self.assertTrue(os.path.exists(self.fp_compiler_path))

    def test_can_find_fpc(self):
        fp_language_with_config = FPLanguage(self.config_parser)
        (is_found, path) = find_tool("fpc")
        self.assertTrue(is_found)
        self.assertEquals(path.pop(0), fp_language_with_config.compiler_path)

    def test_can_successfully_call_fpc_only(self):
        fp_language_with_config = FPLanguage(self.config_parser)
        (ret_code, out, err) = shell(fp_language_with_config.compiler_path + " -h")
        self.assertEquals(ret_code, 0)

    def test_can_successfully_call_fpc_to_compile_test_file(self):
        fp_language_with_config = FPLanguage(self.config_parser)
        (ret_code, out, err) = self._compile(fp_language_with_config)
        self.assertEquals(ret_code, 0)
        self.assertTrue(os.path.exists(self.test_exe_file_path))

    def test_can_successfully_compile_and_run_test_file(self):
        fp_language_with_config = FPLanguage(self.config_parser)
        self._compile(fp_language_with_config)
        test_exe = os.path.join(self.test_exe_file_path, self.test_exe_name)
        (ret_code, out, err) = shell(test_exe)
        self.assertEquals(ret_code, 0)
        self.assertEquals(split_lines(out).pop(0), "Hello, world.")

    def test_can_successfully_compile_and_run_test_file_with_config(self):
        fp_language_with_config = FPLanguage(self.config_parser)
        self._compile(fp_language_with_config)
        test_exe = os.path.join(self.test_exe_file_path, self.test_exe_name)
        (ret_code, out, err) = shell(test_exe)
        self.assertEquals(ret_code, 0)
        self.assertEquals(split_lines(out).pop(0), "Hello, world.")

    def _compile(self, language):
        compile_cmd = screen_str(language.compiler_path) \
                      + " -Fo" + self.build_dir + " -FE" + self.test_exe_file_path \
                      + " " + self.test_src_file_path
        return shell(compile_cmd)

