import unittest
from languages.cpp_language import CPPLanguage
from languages.cs_language import CSLanguage
from languages.fp_language import FPLanguage


class LanguagesTests(unittest.TestCase):

    def test_can_create_cpp_language(self):
        cpp_language = CPPLanguage()
        self.assertIsNotNone(cpp_language)

    def test_can_create_cs_language(self):
        cs_language = CSLanguage()
        self.assertIsNotNone(cs_language)

    def test_can_create_fp_language(self):
        fp_language = FPLanguage()
        self.assertIsNotNone(fp_language)

    def test_can_get_cpp_compiler(self):
        cpp_language = CPPLanguage()
        self.assertIsNotNone(cpp_language.get_compiler_path(), CPPLanguage.COMPILER_PATH)

    def test_can_get_cs_compiler(self):
        cpp_language = CSLanguage()
        self.assertIsNotNone(cpp_language.get_compiler_path(), CSLanguage.COMPILER_PATH)

    def test_can_get_fp_compiler(self):
        cpp_language = FPLanguage()
        self.assertIsNotNone(cpp_language.get_compiler_path(), FPLanguage.COMPILER_PATH)


