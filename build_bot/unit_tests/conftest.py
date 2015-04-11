import os
import shutil
import pytest


@pytest.fixture(scope="class")
def test_build_directory_fixture(request):
    request.cls.test_name = getattr(request.module, "test_name", "default_module")

    request.cls.build_dir = os.path.dirname(__file__) + "\\..\\_build\\" + request.cls.test_name + "\\"
    if os.path.exists(request.cls.build_dir):
        shutil.rmtree(request.cls.build_dir)

    request.cls.build_dir_bin = request.cls.build_dir + "bin\\"
    if not os.path.exists(request.cls.build_dir_bin):
        os.makedirs(request.cls.build_dir_bin)

    request.cls.src_code_path = os.path.dirname(__file__) + "\\..\\code_sources\\"
