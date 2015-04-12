import os
import unittest
import pytest
from common.cmd_utils import shell, set_env, find_tool, split_lines, screen_str
from languages.cpp_language import CPPLanguage

test_name = __name__


@pytest.mark.usefixtures("test_build_directory_fixture", "test_config_fixture")
class CPPLanguageTests(unittest.TestCase):

    def setUp(self):
        self.cpp_language_without_config = CPPLanguage()
        self.test_file_name = "basic"
        self.test_src_name = self.test_file_name + ".cpp"
        self.test_exe_name = self.test_file_name + ".exe"

        self.test_src_file_path = os.path.join(self.src_code_dir, self.test_src_name)
        self.test_exe_file_path = os.path.join(self.build_dir_bin, self.test_exe_name)

    def test_are_all_fixture_attributes_set(self):
        assert hasattr(self, "build_dir")
        assert hasattr(self, "build_dir_bin")
        assert hasattr(self, "src_code_dir")
        assert hasattr(self, "config_parser")
        assert hasattr(self, "is_config_read_ok")

    def test_can_find_build_dir_bin(self):
        self.assertTrue(os.path.exists(self.build_dir_bin))

    def test_can_find_test_src_file(self):
        self.assertTrue(os.path.exists(self.test_src_file_path))

    def test_can_create_cpp_language_without_config(self):
        self.assertIsNotNone(self.cpp_language_without_config)

    def test_can_get_default_cpp_compiler_path(self):
        self.assertEquals(self.cpp_language_without_config.get_compiler_path(), CPPLanguage.DEFAULT_COMPILER_PATH)

    def test_can_get_default_vc_bat_path(self):
        self.assertEquals(self.cpp_language_without_config.vc_bat_path, CPPLanguage.DEFAULT_VC_BAT_PATH)

    def test_is_default_compiler_path_exists(self):
        self.assertTrue(os.path.exists(CPPLanguage.DEFAULT_COMPILER_PATH))

    def test_is_default_vc_bat_path_exists(self):
        self.assertTrue(os.path.exists(CPPLanguage.DEFAULT_VC_BAT_PATH))

    def test_can_set_env_from_bat(self):
        set_env(screen_str(self.cpp_language_without_config.vc_bat_path))
        self.assertIsNotNone(os.getenv("INCLUDE"))
        self.assertIsNotNone(os.getenv("LIB"))

    def test_can_find_cl(self):
        set_env(screen_str(self.cpp_language_without_config.vc_bat_path))
        (is_found, path) = find_tool("cl")
        self.assertTrue(is_found)
        self.assertEquals(path.pop(), self.cpp_language_without_config.compiler_path)

    def test_can_successfully_call_cl_only(self):
        set_env(screen_str(self.cpp_language_without_config.vc_bat_path))
        (ret_code, out, err) = shell(self.cpp_language_without_config.compiler_path)
        self.assertEquals(ret_code, 0)

    def test_can_successfully_call_cl_to_compile_test_file(self):
        (ret_code, out, err) = self._compile(self.cpp_language_without_config)
        self.assertEquals(ret_code, 0)
        self.assertTrue(os.path.exists(self.test_exe_file_path))

    def test_can_successfully_compile_and_run_test_file(self):
        self._compile(self.cpp_language_without_config)
        (ret_code, out, err) = shell(self.test_exe_file_path)
        self.assertEquals(ret_code, 0)
        self.assertEquals(split_lines(out).pop(), "This is a native C++ program.")

    def test_can_successfully_compile_and_run_test_file_with_config(self):
        cpp_language_with_config = CPPLanguage(self.config_parser)
        self._compile(cpp_language_with_config)
        (ret_code, out, err) = shell(self.test_exe_file_path)
        self.assertEquals(ret_code, 0)
        self.assertEquals(split_lines(out).pop(), "This is a native C++ program.")

    def _compile(self, language):
        set_env(screen_str(language.vc_bat_path))
        compile_cmd = screen_str(language.compiler_path) + " " + self.test_src_file_path \
                      + " /Fo" + self.build_dir + os.sep + " /Fe" + self.test_exe_file_path
        print(compile_cmd)
        return shell(compile_cmd)