import os
import unittest
import pytest
from common.cmd_utils import shell, set_env, find_tool
from languages.cpp_language import CPPLanguage


@pytest.mark.usefixtures("test_build_directory_fixture")
class CPPLanguageTests(unittest.TestCase):

    def setUp(self):
        self.cpp_language = CPPLanguage()
        self.test_file = os.path.dirname(__file__) + "\\..\\code_sources\\basic.cpp"

    def test_are_all_fixture_attributes_set(self):
        assert hasattr(self, "build_dir")
        assert hasattr(self, "build_dir_bin")

    def test_can_find_test_file(self):
        self.assertTrue(os.path.exists(self.test_file))
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
        set_env("\"" + self.cpp_language.VCVARSALL_PATH + "\"")
        self.assertIsNotNone(os.getenv("INCLUDE"))
        self.assertIsNotNone(os.getenv("LIB"))

    def test_can_find_cl(self):
        set_env("\"" + self.cpp_language.VCVARSALL_PATH + "\"")
        (is_found, path) = find_tool("cl")
        self.assertTrue(is_found)
        self.assertEquals(path.pop(), self.cpp_language.COMPILER_PATH)

    def test_can_successfully_call_cl_only(self):
        set_env("\"" + self.cpp_language.VCVARSALL_PATH + "\"")
        (ret_code, out, err) = shell(self.cpp_language.COMPILER_PATH)
        self.assertEquals(ret_code, 0)

    def test_can_successfully_call_cl_to_compile_test_file(self):
        set_env("\"" + self.cpp_language.VCVARSALL_PATH + "\"")
        cmd = "\"" + self.cpp_language.COMPILER_PATH + "\" " + self.test_file + " /Fo" + self.build_dir + " /Fe" + self.build_dir_bin
        (ret_code, out, err) = shell(cmd)
        self.assertEquals(ret_code, 0)
