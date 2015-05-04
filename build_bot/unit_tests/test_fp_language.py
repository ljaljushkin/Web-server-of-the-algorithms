import os
import unittest
from build_bot.Languages.fp_language import FPLanguage


class FPLanguageTests(unittest.TestCase):

    def test_can_create_fp_language(self):
        fp_language = FPLanguage()
        self.assertIsNotNone(fp_language)

    def test_can_get_fp_compiler(self):
        cpp_language = FPLanguage()
        self.assertIsNotNone(cpp_language.get_compiler_path(), FPLanguage.DEFAULT_COMPILER_DIR)

    def test_is_compiler_path_exists(self):
        self.assertTrue(os.path.exists(FPLanguage.DEFAULT_COMPILER_DIR))

