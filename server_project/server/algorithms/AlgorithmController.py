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
        currentAlgorithm = Algorithm.objects.get(name=name).get()
        currentAlgorithm.delete()

    def get_algorithm(self, name):
        return Algorithm.objects.get(name=name).get()

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

        dir = self.work_dir + os.sep + algorithm.user_id + os.sep + algorithm.id
        os.makedirs(dir)
        source_file = dir + os.sep + algorithm.name + "." + algorithm.language

        with open(source_file, "w+") as source_file:
            source_file.write(algorithm.source_code)

        exe_path = dir + os.sep + algorithm.name + ".exe"
        self.build_bot = BuildBot(language)
        (ret_code, out, err) = self.build_bot.build(source_file, exe_path)
        if ret_code != 0:
            self.remove_algorithm(algorithm.name)

    # work_dir/id/alg_id/
    # source.cpp
    #                           build.exe
    #                       data.txt


    def search_algorithm(self, name):
        return Algorithm.objects.get(name__iregex=r'\y{0}\y'.format(name)).get()

    def get_algorithms_list(self):
        return Algorithm.objects.get()


        # add(algorithm) : void
        # get(name) : algorithm
        # update(algorithm) : void
        # search(string) : List<algorithm>
        # remove(name) : void
        # getList() : List<algorithm>