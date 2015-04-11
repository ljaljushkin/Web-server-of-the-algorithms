import os
import unittest
from common.cmd_utils import shell, set_env, find_tool
from languages.cpp_language import CPPLanguage


class CPPLanguageTests(unittest.TestCase):
    def setUp(self):
        self.cpp_language = CPPLanguage()

    def test_can_create_cpp_language(self):
        self.assertIsNotNone(self.cpp_language)

    def test_can_get_cpp_compiler(self):
        self.assertEquals(self.cpp_language.get_compiler_path(), CPPLanguage.COMPILER_PATH)

    def test_is_compiler_path_exists(self):
        self.assertTrue(os.path.exists(CPPLanguage.COMPILER_PATH))

    def test_is_vcvarsall_path_exists(self):
        self.assertTrue(os.path.exists(CPPLanguage.VCVARSALL_PATH))

    def test_can_set_env_from_bat(self):
        set_env("\""+self.cpp_language.VCVARSALL_PATH+"\"")
        self.assertIsNotNone(os.getenv("INCLUDE"))
        self.assertIsNotNone(os.getenv("LIB"))

    def test_can_find_cl(self):
        set_env("\""+self.cpp_language.VCVARSALL_PATH+"\"")
        (is_found, path) = find_tool("cl")
        self.assertTrue(is_found)
        self.assertEquals(path.pop(), self.cpp_language.COMPILER_PATH)
