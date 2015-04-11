import os
import unittest
import pytest
from common.cmd_utils import shell, set_env, find_tool, split_lines, screen_str
from languages.cpp_language import CPPLanguage

test_name = __name__


@pytest.mark.usefixtures("test_build_directory_fixture")
class CPPLanguageTests(unittest.TestCase):
    def setUp(self):
        self.cpp_language = CPPLanguage()
        self.test_file_name = "basic"
        self.test_src_name = self.test_file_name + ".cpp"
        self.test_exe_name = self.test_file_name + ".exe"

    def test_are_all_fixture_attributes_set(self):
        assert hasattr(self, "build_dir")
        assert hasattr(self, "build_dir_bin")
        assert hasattr(self, "src_code_path")

    def test_can_find_test_file(self):
        self.assertTrue(os.path.exists(self.src_code_path + self.test_src_name))
        self.assertTrue(os.path.exists(self.build_dir_bin))

    def test_can_create_cpp_language(self):
        self.assertIsNotNone(self.cpp_language)

    def test_can_get_cpp_compiler(self):
        self.assertEquals(self.cpp_language.get_compiler_path(), CPPLanguage.COMPILER_PATH)

    def test_is_compiler_path_exists(self):
        self.assertTrue(os.path.exists(CPPLanguage.COMPILER_PATH))

    def test_is_vcvarsall_path_exists(self):
        self.assertTrue(os.path.exists(CPPLanguage.VCVARSALL_PATH))

    def test_can_set_env_from_bat(self):
        set_env(screen_str(self.cpp_language.VCVARSALL_PATH))
        self.assertIsNotNone(os.getenv("INCLUDE"))
        self.assertIsNotNone(os.getenv("LIB"))

    def test_can_find_cl(self):
        set_env(screen_str(self.cpp_language.VCVARSALL_PATH))
        (is_found, path) = find_tool("cl")
        self.assertTrue(is_found)
        self.assertEquals(path.pop(), self.cpp_language.COMPILER_PATH)

    def test_can_successfully_call_cl_only(self):
        set_env(screen_str(self.cpp_language.VCVARSALL_PATH))
        (ret_code, out, err) = shell(self.cpp_language.COMPILER_PATH)
        self.assertEquals(ret_code, 0)

    def test_can_successfully_call_cl_to_compile_test_file(self):
        set_env(screen_str(self.cpp_language.VCVARSALL_PATH))
        cmd = screen_str(self.cpp_language.COMPILER_PATH) + " " + self.src_code_path + self.test_src_name \
              + " /Fo" + self.build_dir + " /Fe" + self.build_dir_bin
        (ret_code, out, err) = shell(cmd)
        self.assertEquals(ret_code, 0)
        self.assertTrue(os.path.exists(self.build_dir_bin + self.test_exe_name))

    def test_can_successfully_compile_and_run_test_file(self):
        set_env(screen_str(self.cpp_language.VCVARSALL_PATH))
        compile_cmd = screen_str(self.cpp_language.COMPILER_PATH) + " " + self.src_code_path + self.test_src_name \
                      + " /Fo" + self.build_dir + " /Fe" + self.build_dir_bin
        shell(compile_cmd)
        run_cmd = self.build_dir_bin + self.test_exe_name
        (ret_code, out, err) = shell(run_cmd)
        self.assertEquals(ret_code, 0)
        self.assertEquals(split_lines(out).pop(), "This is a native C++ program.")
