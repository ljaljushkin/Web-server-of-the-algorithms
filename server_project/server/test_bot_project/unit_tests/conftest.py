import sys


if sys.version_info > (3, 0):
    import configparser
else:
    import ConfigParser

import os
import pytest

@pytest.fixture(scope="class")
def test_build_directory_fixture(request):
    request.cls.test_name = getattr(request.module, "test_name", "default_module")

    project_path = os.path.dirname(os.path.dirname(__file__))

    request.cls.exe_dir = os.path.join(project_path, "exe_to_run")


@pytest.fixture(scope="class")
def test_config_fixture(request, test_build_directory_fixture):
    project_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    config_file_path = os.path.join(project_path, "config.cfg")

    if sys.version_info > (3, 0):
        request.cls.config_parser = configparser.ConfigParser()
    else:
        request.cls.config_parser = ConfigParser.ConfigParser()

    request.cls.is_config_read_ok = request.cls.config_parser.read(config_file_path)

