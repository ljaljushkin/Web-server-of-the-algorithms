# Веб-сервис алгоритмов

## Постановка задачи: 
Фирма «NewAlgorithm» занимается накоплением и распространением алгоритмов, реализованных пользователями. Средства, используемые ранее в компании, показали свою не эффективность. Для своей деятельности фирма решила разработать специализированную систему. 
Система должна позволять пользователям размещать реализации алгоритмов пользователей в системе. Каждый алгоритм содержит исходный код на одном из поддерживаемых системой языков программирования, текстовое описание, теги и разметку входных и выходных параметров алгоритма, а также набор тестовых данных. Для входных параметров при необходимости должна существовать возможность задания параметров по умолчанию. В первой версии системы в качестве языка программирования планируется использовать C/C++. Набор поддерживаемых языков программирования компания планирует расширять.
Каждый алгоритм, размещаемый в системе, проверяется на компилируемость и прохождение тестов, заданных пользователем. Если все тесты прошли, то пользователь может указать уровень доступа к алгоритму – открытый или требующий платы. Перед покупкой алгоритма, пользователь должен иметь возможность протестировать алгоритм на своих данных. 
Пользователи системы должны иметь возможность поиска алгоритма и его покупки.


## How to use:
	Was tested on windows 8.1. Install the following software:
		install python 2.* (https://www.python.org/) Python 3.0 isn't supported!
		install django 1.7 version. Latest versions are not supported! 
			pip install Django==1.7 (https://docs.djangoproject.com/en/1.9/howto/windows/)
		install git bash
		install Google Chrome (we don't promise correct behavior for other browsers)
		
	open git bash (terminal) and get sources from github:
		$ mkdir -p ~/Document/GitHub/
		$ cd ~/Document/GitHub/
		$ git clone https://github.com/ljaljushkin/Web-server-of-the-algorithms

	set path to the working dir and path to compilers in config.cfg (server_project\server\config.cfg)
		workdir # working directory (to compile/run/test algorithms from here)
		cpp_path # full path to C++ compiler
		cs_path # full path to C# compiler
		fp_path # full path to Free Pascal compiler
		
	go to folder with manage.py
		$ cd Web-server-of-the-algorithms/server_project/server/
	migrate data base. File server_project\server\db.sqlite3 should be created.
		$ python manage.py migrate
	run server
		$ python manage.py runserver
	open browser and go to:
		http://127.0.0.1:8000/algorithms/index.html

	admin mode is also available. 
		http://127.0.0.1:8000/admin
	to creare admin account:
		$ winpty python manage.py createsuperuser