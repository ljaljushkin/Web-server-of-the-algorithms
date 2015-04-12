import os
import unittest

from languages.cs_language import CSLanguage


class CSLanguageTests(unittest.TestCase):

    def test_can_create_cs_language(self):
        cs_language = CSLanguage()
        self.assertIsNotNone(cs_language)

    def test_can_get_cs_compiler(self):
        cpp_language = CSLanguage()
        self.assertIsNotNone(cpp_language.get_compiler_path(), CSLanguage.DEFAULT_COMPILER_DIR)

    def test_is_compiler_path_exists(self):
        self.assertTrue(os.path.exists(CSLanguage.DEFAULT_COMPILER_DIR))
