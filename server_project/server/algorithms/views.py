import json
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    algs_list = ["alg1", "alg2", "alg3", "alg4", "alg5", "alg6", "alg7", "alg8", "alg9", "alg10"]

    return render(request,
                  "algorithms/index.html",
                  {"algs_list": algs_list})


def alg_details(request):
    print(request)
    return HttpResponse(request.POST["selected_alg"])


