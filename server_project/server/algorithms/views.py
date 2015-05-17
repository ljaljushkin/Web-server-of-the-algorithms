import sys
from build_bot_project.build_bot import BuildBot
from build_bot_project.common.cmd_utils import shell, split_lines
from build_bot_project.languages.cpp_language import CPPLanguage

if sys.version_info > (3, 0):
    import configparser
else:
    import ConfigParser

import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from algorithms.models import Algorithm, TestData, User, Status

def index(request):
    login = []
    if "login" in request.session.keys() :
        login = request.session["login"] 
        
    alg_obj_list = Algorithm.objects.all()
    algs_list = []

    for item in alg_obj_list:
        algs_list.append(item.algorithm_name)

    return render(request,
                  "algorithms/index.html",
                  {"algs_list": algs_list,
                   "login" : login})


def alg_details(request, alg_name):
    login = []
    if "login" in request.session.keys() :
        login = request.session["login"] 

    print(alg_name)
    algorithm = Algorithm.objects.filter(algorithm_name=alg_name).first()
    return render(request,
                  "algorithms/alg_details.html",
                  {"name": algorithm.algorithm_name,
                   "description": algorithm.algorithm_description,
                   "source_code": algorithm.source_code,
                   "login" : login})


def add_algorithm(request):
    login = []
    if "login" in request.session.keys() :
        login = request.session["login"] 
        
    return render(request,
                  "algorithms/add_algorithm.html",
                    {"login" : login})

def login(request):
    if "login" in request.POST.keys() \
    and "password" in request.POST.keys() :
        user = User.objects.filter(login = request.POST["login"], password = request.POST["password"]).get()
        if user != None :
            request.session["login"] = user.login
            return HttpResponseRedirect('/algorithms/')
        else :
            return HttpResponseRedirect('/algorithms/login/')
   
def logout(request):
    try:
        del request.session['login']
    except KeyError:
        pass
    return HttpResponseRedirect('/algorithms/')
   
def register(request):
    if "login" in request.POST.keys() \
    and "email" in request.POST.keys() \
    and "password" in request.POST.keys() :
        print (request.POST["login"])
        user = User.objects.create(login = request.POST["login"],
                                    email = request.POST["email"],
                                    password = request.POST["password"],
                                    account_cash = 0)
        user.save()
    return render(request,
                  "algorithms/register.html",
        {})
		
def submit_algorithm(request):
    if not "login" in request.session :
        return HttpResponseRedirect('/algorithms/login/')
     
    print("name = " + request.POST["name"])
    print("description = " + request.POST["description"])
    print("price = " + request.POST["price"])

    test_data = TestData.objects.create(input_data=request.POST["test_data"],
                                        output_data=request.POST["test_data"],
                                        run_options=request.POST["run_string"])
    test_data.save()

    user = User.objects.filter(login=request.session["login"]).get()

    status = Status.objects.create(status_name="tanya_OK")
    status.save()

    new_algo = Algorithm.objects.create(algorithm_name=request.POST["name"],
                                        algorithm_description=request.POST["description"],
                                        source_code=request.POST["code"],
                                        build_options=request.POST["build_string"],
                                        testdata_id=test_data,
                                        price=request.POST["price"],
                                        user_id=user,
                                        status_id=status,
                                        language="cpp")

    if sys.version_info > (3, 0):
        config_parser = configparser.ConfigParser()
    else:
        config_parser = ConfigParser.ConfigParser()

    project_path = os.path.dirname(os.path.dirname(__file__))
    is_config_read_ok = config_parser.read(os.path.join(project_path, "config.cfg"))
    assert is_config_read_ok

    cpp_language = CPPLanguage(config_parser)
    build_bot_project = BuildBot(cpp_language, config_parser)

    output_dir = config_parser.get("build_options", "output_path")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    code_path = project_path + os.sep + "build_bot_project" + os.sep + "code_to_compile" + os.sep + "basic.cpp"
    exe_path = os.path.join(output_dir, "basic.exe")
    (ret_code, out, err) = build_bot_project.build(code_path, exe_path)
    assert ret_code == 0

    new_algo.source_code = "OUTPUT STREAM FROM BUILD---> "
    for line in out.splitlines():
        new_algo.source_code += line.strip().decode('utf-8')

    new_algo.build_options = "ERROR STREAM FROM BUILD---> "
    for line in err.splitlines():
        new_algo.build_options += line.strip().decode('utf-8')

    (ret_code, out, err) = shell(exe_path)
    assert ret_code == 0
    assert split_lines(out).pop(0) == "This is a native C++ program."

    new_algo.algorithm_description = "OUTPUT STREAM FROM EXE---> "
    for line in out.splitlines():
        new_algo.algorithm_description += line.strip().decode('utf-8')

    new_algo.save()

    return HttpResponse(request)
