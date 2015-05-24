import ConfigParser
import os
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from algorithms import IAlgorithmController
from algorithms import IPayController
from algorithms.AlgorithmController import AlgorithmController
from algorithms.FakePayController import FakePayController

from algorithms.models import User, TestData, Status, BoughtAlgorithm, Tag, TagList
from build_bot_project.languages.cpp_language import CPPLanguage
from build_bot_project.languages.cs_language import CSLanguage
from build_bot_project.languages.fp_language import FPLanguage
from common.cmd_utils import STATUS_SUCCESS

algorithm_controller = IAlgorithmController
config_parser = None
pay_controller = IPayController


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

    tags_list_db = Tag.objects.all()
    tags_list = []

    for tag in tags_list_db:
        tags_list.append(tag.tag_name)

    return render(request,
                  "algorithms/index.html",
                  {"algs_list": algs_list,
                   "tags_list": tags_list,
                   "login": login})


def get_tagged_algorithms(request, tag):
    login = []
    if "login" in request.session.keys():
        login = request.session["login"]

    algorithm_controller = create_algorithm_controller()
    algs_list = algorithm_controller.get_tagged_algorithm_names_list(tag)

    tags_list_db = Tag.objects.all()
    tags_list = []

    for tag in tags_list_db:
        tags_list.append(tag.tag_name)

    return render(request,
                  "algorithms/index.html",
                  {"algs_list": algs_list,
                   "tags_list": tags_list,
                   "login": login})


def get_tags_for_algorithm(algorithm):
    tags_list_db = TagList.objects.filter(algorithm_id=algorithm).all()
    tags_list = []

    for tag in tags_list_db:
        tags_list.append(tag.tag_id.tag_name)

    return tags_list


def alg_details(request, alg_name):
    login = []
    if "login" in request.session.keys():
        login = request.session["login"]
    algorithm_controller = create_algorithm_controller()
    algorithm = algorithm_controller.get_algorithm(alg_name)
    # TODO: tags
    is_bought = False

    if login:
        try:
            user = User.objects.filter(login=login).get()
            bought_alg = BoughtAlgorithm.objects.filter(user_id=user, algorithm_id=algorithm).get()
            is_bought = True
        except BoughtAlgorithm.DoesNotExist:
            is_bought = False

    tags_list = get_tags_for_algorithm(algorithm)
    tags_string = ",".join(tags_list)

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
                       tags=tags_string,
                       login=login,
                       is_bought=is_bought))


def add_algorithm(request):
    login = []
    if "login" in request.session.keys():
        login = request.session["login"]
    else:
        return HttpResponseRedirect('/algorithms/login/')

    language_list = AlgorithmController.get_languages_list()

    return render(request,
                  "algorithms/add_algorithm.html",
                  dict(login=login,
                       language_list=language_list))


def buy_algorithm(request, alg_name):
    login = []
    if "login" in request.session.keys():
        login = request.session["login"]
    else:
        return HttpResponseRedirect('/algorithms/login/')

    algorithm_controller = create_algorithm_controller()
    algorithm = algorithm_controller.get_algorithm(alg_name)

    try:
        user = User.objects.filter(login=login).get()
        bought_alg = BoughtAlgorithm.objects.filter(user_id=user, algorithm_id=algorithm).get()
        return HttpResponse("Already bought!")
    except BoughtAlgorithm.DoesNotExist:
        pay_controller = FakePayController()
        if pay_controller.send_money(algorithm.price, login, algorithm.user_id.login):
            user = User.objects.filter(login=login).get()
            bought_alg = BoughtAlgorithm.objects.create(user_id=user, algorithm_id=algorithm)

            bought_alg.save()

            return HttpResponseRedirect("/algorithms/" + alg_name)
        else:
            return HttpResponse("Not enough money!")


def update_algorithm_page(request, alg_name):
    login = []
    if "login" in request.session.keys():
        login = request.session["login"]
    else:
        return HttpResponseRedirect('/algorithms/login/')

    algorithm_controller = create_algorithm_controller()
    algorithm = algorithm_controller.get_algorithm(alg_name)

    tags_list = get_tags_for_algorithm(algorithm)
    tags_string = ",".join(tags_list)

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
                       tags=tags_string))


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

    ret_code = algorithm_controller.update_algorithm(name=request.POST["name"],
                                                     description=request.POST["description"],
                                                     source_code=request.POST["code"],
                                                     build_options=request.POST["build_string"],
                                                     testdata_id=test_data,
                                                     price=request.POST["price"],
                                                     language=request.POST["language"],
                                                     tags=request.POST["tags"].strip().split(","))

    status = ["failed to update", "successfully updated"][ret_code == STATUS_SUCCESS]

    return HttpResponse(status)


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

        try:
            user = User.objects.filter(login=request.POST["login"], password=request.POST["password"]).get()
        except User.DoesNotExist:
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
                                                     language=request.POST["language"],
                                                     tags=request.POST["tags"].strip().split(","))

    (ret_code, out, err) = algorithm_controller.add_algorithm(new_algo)

    if ret_code == STATUS_SUCCESS:
        out_all = "Algorithm was successfully added! "
    else:
        out_all = "Failed to add algorithm! <br> ret_code = " + str(ret_code)

    out_all += "<br><br> OUTPUT STREAM FROM BUILD---> "
    for line in out.splitlines():
        out_all += line.strip().decode('utf-8') + "<br>"

    out_all += "<br><br> ERROR STREAM FROM BUILD---> "
    for line in err.splitlines():
        out_all += line.strip().decode('utf-8') + "<br>"

    if ret_code == STATUS_SUCCESS:
        (ret_code, out, err) = algorithm_controller.run_algorithm(new_algo.name)
        if ret_code == STATUS_SUCCESS:
            out_all += "<br><br>Algorithm was successfully run!"
        else:
            out_all += "<br><br> Failed to run algorithm! <br> ret_code = " + str(ret_code)

        out_all += "<br><br> OUTPUT STREAM FROM EXE---> "
        for line in out.splitlines():
            out_all += line.strip().decode('utf-8') + "<br>"

        out_all += "<br><br> ERROR STREAM FROM BUILD---> "
        for line in err.splitlines():
            out_all += line.strip().decode('utf-8') + "<br>"

    return HttpResponse(out_all)
