from django.conf.urls import patterns, url

from algorithms import views

urlpatterns = patterns("",
                       url(r"^$", views.index, name="index"),
                       url(r"add_algorithm/$", views.add_algorithm, name="add_algorithm"),
                       url(r"submit_algorithm/$", views.submit_algorithm, name="submit_algorithm"),
                       url(r"run_existing_algo/$", views.run_existing_algo, name="run_existing_algo"),
                       url(r'^([-\w]+)$', views.alg_details, name="alg_details"))
