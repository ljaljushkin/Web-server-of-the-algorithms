import os
import shutil
import pytest


@pytest.fixture(scope="class")
def test_build_directory_fixture(request):
    request.cls.build_dir = os.path.dirname(__file__) + "\\..\\_build\\"
    if os.path.exists(request.cls.build_dir):
        shutil.rmtree(request.cls.build_dir)

    request.cls.build_dir_bin = request.cls.build_dir + "bin\\"
    if not os.path.exists(request.cls.build_dir_bin):
        os.makedirs(request.cls.build_dir_bin)
