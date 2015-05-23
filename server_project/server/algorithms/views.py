import ConfigParser
import os
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from algorithms import IAlgorithmController
from algorithms.AlgorithmController import AlgorithmController
from algorithms.models import User, TestData, Status
from common.cmd_utils import split_lines

algorithm_controller = IAlgorithmController
config_parser = None


def create_algorithm_controller():
    config_parser = ConfigParser.ConfigParser()
    project_path = os.path.dirname(os.path.dirname(__file__))
    is_config_read_ok = config_parser.read(os.path.join(project_path, "config.cfg"))
    assert is_config_read_ok

    algorithm_controller = AlgorithmController(config_parser)
    return algorithm_controller


def alg_description(request, alg_name):
    print request, alg_name
    algorithm_controller = create_algorithm_controller()
    algorithm = algorithm_controller.get_algorithm(alg_name)
    return HttpResponse(algorithm.description)


def index(request):
    login = []
    if "login" in request.session.keys():
        login = request.session["login"]

    algorithm_controller = create_algorithm_controller()
    algs_list = algorithm_controller.get_algorithm_names_list()

    return render(request,
                  "algorithms/index.html",
                  {"algs_list": algs_list,
                   "login": login})


def alg_details(request, alg_name):
    login = []
    if "login" in request.session.keys():
        login = request.session["login"]
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
                       tags="TBD",
                       login=login))


def add_algorithm(request):
    login = []
    if "login" in request.session.keys():
        login = request.session["login"]
    else:
        return HttpResponseRedirect('/algorithms/login/')

    language_list = ["c++", "c#", "pascal"]

    return render(request,
                  "algorithms/add_algorithm.html",
                  dict(login=login,
                       language_list=language_list))


def update_algorithm_page(request, alg_name):
    login = []
    if "login" in request.session.keys():
        login = request.session["login"]
    else:
        return HttpResponseRedirect('/algorithms/login/')

    algorithm_controller = create_algorithm_controller()
    algorithm = algorithm_controller.get_algorithm(alg_name)

    return render(request,
                  "algorithms/update_algorithm.html",
                  dict(login=login,
                       name=algorithm.name,
                       description=algorithm.description,
                       language_list=["c++", "c#", "pascal"],
                       code=algorithm.source_code,
                       build_string=algorithm.build_options,
                       run_string=algorithm.testdata_id.run_options,
                       test_data=algorithm.testdata_id.input_data,
                       price=algorithm.price,
                       tags=algorithm.tag))


def update_algorithm(request):
    login = []
    if "login" in request.session.keys():
        login = request.session["login"]
    else:
        return HttpResponseRedirect('/algorithms/login/')

    algorithm_controller = create_algorithm_controller()
    test_data = TestData.objects.create(input_data=request.POST["test_data"],
                                        output_data=request.POST["test_data"],
                                        run_options=request.POST["run_string"])
    test_data.save()

    algorithm_controller.update_algorithm(name=request.POST["name"],
                                          description=request.POST["description"],
                                          source_code=request.POST["code"],
                                          build_options=request.POST["build_string"],
                                          testdata_id=test_data,
                                          price=request.POST["price"],
                                          language=request.POST["language"])
    return HttpResponse("successfully updated")


def run_existing_algo(request, alg_name):
    algorithm_controller = create_algorithm_controller()
    (ret_code, out, err) = algorithm_controller.run_algorithm(alg_name)
    out_all = "ret_code = " + str(ret_code) + "<br>"
    for line in out.splitlines():
        out_all += line.strip().decode('utf-8')

    out_all += "<br>"
    for line in err.splitlines():
        out_all += line.strip().decode('utf-8')
    return HttpResponse(out_all)


def login(request):
    if "login" in request.POST.keys() \
            and "password" in request.POST.keys():

        user = None

        try :
            user = User.objects.filter(login=request.POST["login"], password=request.POST["password"]).get()
        except User.DoesNotExist :
            user = None

        if user is not None:
            request.session["login"] = user.login
            return HttpResponseRedirect('/algorithms/')
        else:
            return HttpResponseRedirect('/algorithms/register/')
    return render(request,
                  "algorithms/login.html",
        {})

def logout(request):
    try:
        del request.session['login']
    except KeyError:
        pass
    return HttpResponseRedirect('/algorithms/')


def register(request):
    if "login" in request.POST.keys() \
            and "email" in request.POST.keys() \
            and "password" in request.POST.keys():
        print (request.POST["login"])
        user = User.objects.create(login=request.POST["login"],
                                   email=request.POST["email"],
                                   password=request.POST["password"],
                                   account_cash=0)
        user.save()
    return render(request,
                  "algorithms/register.html",
        {})


def submit_algorithm(request):
    algorithm_controller = create_algorithm_controller()

    test_data = TestData.objects.create(input_data=request.POST["test_data"],
                                        output_data=request.POST["test_data"],
                                        run_options=request.POST["run_string"])
    test_data.save()

    user = User.objects.filter(login=request.session["login"]).get()

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

    # TODO: print to the redirected html page

    out_all = "OUTPUT STREAM FROM BUILD---> "
    for line in out.splitlines():
        out_all += line.strip().decode('utf-8') + "<br>"

    out_all += "<br><br> ERROR STREAM FROM BUILD---> "
    for line in err.splitlines():
        new_algo.build_options += line.strip().decode('utf-8') + "<br>"

    (ret_code, out, err) = algorithm_controller.run_algorithm(new_algo.name)
    out_all += " <br><br> ret_code = " + str(ret_code)

    out_all += "<br><br> OUTPUT STREAM FROM EXE---> "
    for line in out.splitlines():
        out_all += line.strip().decode('utf-8') + "<br>"

    out_all += "<br><br> ERROR STREAM FROM BUILD---> "
    for line in err.splitlines():
        out_all += line.strip().decode('utf-8') + "<br>"

    test_data.save()
    new_algo.test_data_id = test_data
    new_algo.save()

    return HttpResponse(out_all)
