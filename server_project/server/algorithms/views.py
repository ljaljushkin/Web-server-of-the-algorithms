from algorithms import IAlgorithmController
from algorithms.AlgorithmController import AlgorithmController
from algorithms.models import Algorithm, TestData, User, Status
from common.cmd_utils import split_lines

import ConfigParser
import os

from django.http import HttpResponse
from django.shortcuts import render

algorithm_controller = IAlgorithmController
config_parser = None


def create_algorithm_controller():
    config_parser = ConfigParser.ConfigParser()
    project_path = os.path.dirname(os.path.dirname(__file__))
    is_config_read_ok = config_parser.read(os.path.join(project_path, "config.cfg"))
    assert is_config_read_ok

    algorithm_controller = AlgorithmController(config_parser)
    return algorithm_controller


def index(request):
    algorithm_controller = create_algorithm_controller()
    algs_list = algorithm_controller.get_algorithm_names_list()

    return render(request,
                  "algorithms/index.html",
                  {"algs_list": algs_list})


def alg_details(request, alg_name):
    algorithm_controller = create_algorithm_controller()
    algorithm = algorithm_controller.get_algorithm(alg_name)
    # TODO: tags
    return render(request,
                  "algorithms/alg_details.html",
                  dict(name=algorithm.name,
                       description=algorithm.description,
                       language=algorithm.language,
                       source_code=algorithm.source_code,
                       build_options=algorithm.build_options,
                       run_options=algorithm.testdata_id.run_options,
                       test_data=algorithm.testdata_id.input_data,
                       price=algorithm.price,
                       tags="TBD"))


def add_algorithm(request):
    language_list = ["c++", "c#", "pascal"]
    return render(request,
                  "algorithms/add_algorithm.html",
                  {"language_list": language_list})


def update_algorithm(request):
    algorithm_controller = create_algorithm_controller()

    test_data = TestData.objects.create(input_data=request.POST["test_data"],
                                        output_data=request.POST["test_data"],
                                        run_options=request.POST["run_string"])
    test_data.save()

    old_algorithm = algorithm_controller.get_algorithm(name=request.POST["name"])
    algorithm_controller.update_algorithm(old_algorithm=old_algorithm,
                                          name=request.POST["name"],
                                          description=request.POST["description"],
                                          source_code=request.POST["code"],
                                          build_options=request.POST["build_string"],
                                          testdata_id=test_data,
                                          price=request.POST["price"],
                                          language=request.POST["language"])


def run_existing_algo(request):
    algorithm_controller = create_algorithm_controller()
    algorithm_controller.run_algorithm("TROLOLO_ALGORITHM_NAME")
    return HttpResponse(request)


def submit_algorithm(request):
    algorithm_controller = create_algorithm_controller()

    test_data = TestData.objects.create(input_data=request.POST["test_data"],
                                        output_data=request.POST["test_data"],
                                        run_options=request.POST["run_string"])
    test_data.save()

    # TODO: user
    user = User.objects.create(login="tanya",
                               password="zenit champion",
                               email="fedor",
                               account_cash=666)
    user.save()

    status = Status.objects.create(name="tanya_OK")
    status.save()

    new_algo = algorithm_controller.create_algorithm(name=request.POST["name"],
                                                     description=request.POST["description"],
                                                     source_code=request.POST["code"],
                                                     build_options=request.POST["build_string"],
                                                     testdata_id=test_data,
                                                     price=request.POST["price"],
                                                     user_id=user,
                                                     status_id=status,
                                                     language="cpp")

    (ret_code, out, err) = algorithm_controller.add_algorithm(new_algo)

    assert ret_code == 0

    new_algo.source_code = "OUTPUT STREAM FROM BUILD---> "
    for line in out.splitlines():
        new_algo.source_code += line.strip().decode('utf-8')

    new_algo.build_options = "ERROR STREAM FROM BUILD---> "
    for line in err.splitlines():
        new_algo.build_options += line.strip().decode('utf-8')

    (ret_code, out, err) = algorithm_controller.run_algorithm(new_algo.name)
    assert ret_code == 0
    assert split_lines(out).pop(0) == "This is a native C++ program."

    new_algo.description = "OUTPUT STREAM FROM EXE---> "
    for line in out.splitlines():
        new_algo.description += line.strip().decode('utf-8')

    test_data.run_options = "ERROR STREAM FROM BUILD--- "
    for line in err.splitlines():
        test_data.run_options += line.strip().decode('utf-8')

    test_data.save()
    new_algo.test_data_id = test_data
    new_algo.save()

    return HttpResponse(request)
