from django.conf.urls import patterns, url

from algorithms import views

urlpatterns = patterns("",
                       url(r"^$", views.index, name="index"),
                       url(r"alg_details/$", views.alg_details, name="alg_details"))