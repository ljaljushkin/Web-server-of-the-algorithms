import sys

from algorithms import IAlgorithmController
from algorithms.AlgorithmController import AlgorithmController
from build_bot_project.build_bot import BuildBot
from common.cmd_utils import shell, split_lines
from build_bot_project.languages.cpp_language import CPPLanguage


if sys.version_info > (3, 0):
    import configparser
else:
    import ConfigParser

import os
from django.http import HttpResponse
from django.shortcuts import render

from algorithms.models import Algorithm, TestData, User, Status

algorithm_controller = IAlgorithmController
config_parser = None


def init():
    if sys.version_info > (3, 0):
        config_parser = configparser.ConfigParser()
    else:
        config_parser = ConfigParser.ConfigParser()
    project_path = os.path.dirname(os.path.dirname(__file__))
    is_config_read_ok = config_parser.read(os.path.join(project_path, "config.cfg"))
    assert is_config_read_ok

    algorithm_controller = AlgorithmController(config_parser)
    return algorithm_controller, config_parser


def index(request):
    alg_obj_list = Algorithm.objects.all()
    algs_list = []

    for item in alg_obj_list:
        algs_list.append(item.name)

    return render(request,
                  "algorithms/index.html",
                  {"algs_list": algs_list})


def alg_details(request, alg_name):
    algorithm = Algorithm.objects.filter(name=alg_name).first()
    return render(request,
                  "algorithms/alg_details.html",
                  dict(name=algorithm.name,
                       description=algorithm.description,
                       source_code=algorithm.source_code,
                       build_options=algorithm.build_options,
                       run_options=algorithm.testdata_id.run_options))


def add_algorithm(request):
    return render(request,
                  "algorithms/add_algorithm.html",
        {})


def submit_algorithm(request):
    test_data = TestData.objects.create(input_data=request.POST["test_data"],
                                        output_data=request.POST["test_data"],
                                        run_options=request.POST["run_string"])
    test_data.save()

    user = User.objects.create(login="tanya",
                               password="zenit champion",
                               email="fedor",
                               account_cash=666)
    user.save()

    status = Status.objects.create(name="tanya_OK")
    status.save()

    new_algo = Algorithm.objects.create(name=request.POST["name"],
                                        description=request.POST["description"],
                                        source_code=request.POST["code"],
                                        build_options=request.POST["build_string"],
                                        testdata_id=test_data,
                                        price=request.POST["price"],
                                        user_id=user,
                                        status_id=status,
                                        language="cpp")

    algorithm_controller, config_parser = init()
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

    test_data.run_options = "ERROR STREAM FROM BUILD---> "
    for line in err.splitlines():
        test_data.run_options += line.strip().decode('utf-8')

    test_data.save()
    new_algo.test_data_id = test_data
    new_algo.save()

    return HttpResponse(request)
