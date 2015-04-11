import unittest

from build_bot import BuildBot
from languages.cpp_language import CPPLanguage
from languages.cs_language import CSLanguage
from languages.fp_language import FPLanguage


class BuildBotTests(unittest.TestCase):
    def test_can_create_build_bot_for_cpp_language(self):
        language = CPPLanguage()
        # self.assertEqual("",language.COMPILER_PATH)
        build_bot = BuildBot(language)
        self.assertEqual(build_bot.compiler_path, CPPLanguage.COMPILER_PATH)

    def test_can_create_build_bot_for_cs_language(self):
        language = CSLanguage()
        build_bot = BuildBot(language)
        self.assertEqual(build_bot.compiler_path, CSLanguage.COMPILER_PATH)

    def test_can_create_build_bot_for_fp_language(self):
        language = FPLanguage()
        build_bot = BuildBot(language)
        self.assertEqual(build_bot.compiler_path, FPLanguage.COMPILER_PATH)
