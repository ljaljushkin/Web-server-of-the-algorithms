import os
import unittest
import pytest
from build_bot.build_bot import BuildBot
from build_bot.Languages.cpp_language import CPPLanguage
from build_bot.Languages.fp_language import FPLanguage
from build_bot.Languages.cs_language import CSLanguage

test_name = __name__


@pytest.mark.usefixtures("test_config_fixture")
class BuildBotTests(unittest.TestCase):

    def test_are_all_fixture_attributes_set(self):
        assert hasattr(self, "build_dir")
        assert hasattr(self, "build_dir_bin")
        assert hasattr(self, "src_code_dir")
        assert hasattr(self, "config_parser")
        assert hasattr(self, "is_config_read_ok")

    def test_can_create_build_bot_for_cpp_language_without_config(self):
        language = CPPLanguage()
        build_bot = BuildBot(language, self.config_parser)
        self.assertEqual(build_bot.language.compiler_path, CPPLanguage.DEFAULT_COMPILER_PATH)

    def test_can_create_build_bot_for_cpp_language_with_config(self):
        language = CPPLanguage(self.config_parser)
        build_bot = BuildBot(language, self.config_parser)
        self.assertEqual(build_bot.language.compiler_path, CPPLanguage.DEFAULT_COMPILER_PATH)

    def test_can_create_build_bot_for_cs_language(self):
        language = CSLanguage()
        build_bot = BuildBot(language, self.config_parser)
        self.assertEqual(build_bot.language.compiler_path, CSLanguage.DEFAULT_COMPILER_PATH)

    def test_can_create_build_bot_for_fp_language(self):
        language = FPLanguage()
        build_bot = BuildBot(language, self.config_parser)
        self.assertEqual(build_bot.language.compiler_path, FPLanguage.DEFAULT_COMPILER_PATH)
