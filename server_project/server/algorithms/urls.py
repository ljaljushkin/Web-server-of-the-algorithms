from django.conf.urls import patterns, url

from algorithms import views

urlpatterns = patterns("",
                       url(r"^$", views.index, name="index"),
                       url(r"add_algorithm/$", views.add_algorithm, name="add_algorithm"),
                       url(r"statistics/$", views.statistics, name="statistics"),
                       url(r"buy_algorithm/([-\w]+)$", views.buy_algorithm, name="buy_algorithm"),
                       url(r"tag/([-\w]+)$", views.get_tagged_algorithms, name="get_tagged_algorithms"),
                       url(r"update_algorithm_page/([-\w]+)$", views.update_algorithm_page, name="update_algorithm"),
                       url(r"update_algorithm/$", views.update_algorithm, name="update_algorithm"),
                       url(r"submit_algorithm/$", views.submit_algorithm, name="submit_algorithm"),
                       url(r"register/$", views.register, name="register"),
                       url(r"login/$", views.login, name="login"),
                       url(r"logout/$", views.logout, name="logout"),
                       url(r"run/([-\w]+)$", views.run_existing_algo, name="run_existing_algo"),
                       url(r'^([-\w]+)$', views.alg_details, name="alg_details"),
                       url(r'^([-\w]+)/description/$', views.alg_description, name="alg_details"),
                       url(r"refill/$", views.refill, name="refill"),
                       url(r"my/$", views.my_algorithms, name="my_algorithms"),
                       url(r"password_reset/$", views.password_reset, name="password_reset"),
                       url(r"password_reset_page/$", views.password_reset_page, name="password_reset_page"))
