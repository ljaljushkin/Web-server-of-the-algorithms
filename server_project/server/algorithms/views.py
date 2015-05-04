from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from algorithms.models import Algorithm, TestData, User, Status


def index(request):
    alg_obj_list = Algorithm.objects.all()
    algs_list = []

    for item in alg_obj_list :
        algs_list.append(item.algorithm_name)

    return render(request,
                  "algorithms/index.html",
                  {"algs_list": algs_list})


def alg_details(request, alg_name):
    print(alg_name)
    algorithm = Algorithm.objects.filter(algorithm_name=alg_name).first();
    return render(request,
                  "algorithms/alg_details.html",
        {"name":algorithm.algorithm_name,
        "description":algorithm.algorithm_description,
        "source_code":algorithm.source_code})


def add_algorithm(request):
    return render(request,
                  "algorithms/add_algorithm.html",
        {})


def submit_algorithm(request):
    print("name = " + request.POST["name"])
    print("description = " + request.POST["description"])
    print("price = " + request.POST["price"])

    test_data = TestData.objects.create(input_data=request.POST["test_data"],
                                        output_data=request.POST["test_data"],
                                        run_options=request.POST["run_string"])
    test_data.save()

    user = User.objects.create(login="tanya",
                               password="zenit champion",
                               email="fedor",
                               account_cash=666)
    user.save()

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
    new_algo.save()

    return HttpResponse(request)


