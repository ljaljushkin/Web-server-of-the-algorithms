import os
from algorithms.IAlgorithmController import IAlgorithmController
from algorithms.models import Algorithm
from build_bot_project.build_bot import BuildBot
from build_bot_project.languages.cpp_language import CPPLanguage
from build_bot_project.languages.cs_language import CSLanguage
from build_bot_project.languages.fp_language import FPLanguage
from test_bot_project.test_bot import TestBot


class AlgorithmController(IAlgorithmController):
    def __init__(self, config_parser):
        IAlgorithmController.__init__(self)
        self.build_bot = BuildBot()
        self.test_bot = TestBot()
        self.config_parser = config_parser
        self.work_dir = self.config_parser.get("general", "work_dir")

    def remove_algorithm(self, name):
        current_algorithm = Algorithm.objects.filter(name=name).get()
        current_algorithm.delete()

    def get_algorithm(self, name):
        return Algorithm.objects.filter(name=name).get()

    def update_algorithm(self, algorithm):
        pass

    def add_algorithm(self, algorithm):
        algorithm.save()

        language = None
        if algorithm.language == "cpp":
            language = CPPLanguage(self.config_parser)
        elif algorithm.language == "cs":
            language = CSLanguage(self.config_parser)
        elif algorithm.language == "fp":
            language = FPLanguage(self.config_parser)

        self.build_bot.set_language(language)

        algorithm_dir = self._get_algorithm_dir(algorithm)
        os.makedirs(algorithm_dir)
        source_file = algorithm_dir + os.sep + algorithm.name + "." + algorithm.language

        with open(source_file, "wb") as src_file:
            src_file.write(algorithm.source_code)

        exe_path = self._get_exe_path(algorithm)
        (ret_code, out, err) = self.build_bot.build(source_file, str(exe_path))

        if ret_code != 0:
            self.remove_algorithm(algorithm.name)

        return ret_code, out, err

    def run_algorithm(self, name):
        algorithm = self.get_algorithm(name)
        exe_path = self._get_exe_path(algorithm)
        return self.test_bot.run(file=exe_path,
                                 run_string=algorithm.testdata_id.run_options)

    def search_algorithm(self, name):
        return Algorithm.objects.get(name__iregex=r'\y{0}\y'.format(name)).get()

    def get_algorithms_list(self):
        return Algorithm.objects.get()

    def _get_algorithm_dir(self, algorithm):
        return self.work_dir + os.sep + str(algorithm.user_id.user_id) + os.sep + str(algorithm.algorithm_id)

    def _get_exe_path(self, algorithm):
        return self._get_algorithm_dir(algorithm) + os.sep + algorithm.name + ".exe"
