import os
from algorithms.IAlgorithmController import IAlgorithmController
from algorithms.models import Algorithm
from build_bot_project.build_bot import BuildBot
from build_bot_project.languages.cpp_language import CPPLanguage
from build_bot_project.languages.cs_language import CSLanguage
from build_bot_project.languages.fp_language import FPLanguage


class AlgorithmController(IAlgorithmController):
    def __init__(self, config_parser):
        IAlgorithmController.__init__(self)
        self.config_parser = config_parser
        self.work_dir = self.config_parser.get("general", "work_dir")

    def remove_algorithm(self, name):
        currentAlgorithm = Algorithm.objects.filter(name=name).get()
        currentAlgorithm.delete()

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

        dir = self._getAlgorithmDir(algorithm)
        os.makedirs(dir)
        source_file = dir + os.sep + algorithm.name + "." + algorithm.language

        with open(source_file, "wb") as file:
            file.write(algorithm.source_code)

        exe_path = self._getExePath(algorithm)
        self.build_bot = BuildBot(language)
        (ret_code, out, err) = self.build_bot.build(source_file, str(exe_path))

        if ret_code != 0:
            self.remove_algorithm(algorithm.name)

        return ret_code, out, err

    def _getAlgorithmDir(self, algorithm):
        return self.work_dir + os.sep + str(algorithm.user_id.user_id) + os.sep + str(algorithm.algorithm_id)

    def _getExePath(self,algorithm):
        return self._getAlgorithmDir(algorithm) + os.sep + algorithm.name + ".exe"

    def run_algorithm(self, name):
        algorithm = self.get_algorithm(name)
        exe_path = self._getExePath(algorithm)
        # (ret_code, out, err) = RunBot.start()
        return 0, "This is a native C++ program.", "fake_err"

    def search_algorithm(self, name):
        return Algorithm.objects.get(name__iregex=r'\y{0}\y'.format(name)).get()

    def get_algorithms_list(self):
        return Algorithm.objects.get()
