import os
import unittest
from build_bot_project.languages.fp_language import FPLanguage


class FPLanguageTests(unittest.TestCase):

    def setUp(self):
        self.fp_language_without_config = FPLanguage()

    def test_can_create_fp_language(self):
        self.assertIsNotNone(self.fp_language_without_config)

    def test_can_get_fp_compiler(self):
        self.assertIsNotNone(self.fp_language_without_config.get_compiler_path(), FPLanguage.DEFAULT_COMPILER_DIR)

    def test_is_compiler_path_exists(self):
        self.assertTrue(os.path.exists(FPLanguage.DEFAULT_COMPILER_DIR))

    def test_fp_language_name(self):
        self.assertEqual(self.fp_language_without_config.get_name(), "Free Pascal")

    def test_fp_language_extension(self):
        self.assertEqual(self.fp_language_without_config.get_extension(), "pas")


