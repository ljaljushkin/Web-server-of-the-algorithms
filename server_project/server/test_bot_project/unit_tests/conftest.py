import os
import pytest


@pytest.fixture(scope="class")
def test_build_directory_fixture(request):
    request.cls.test_name = getattr(request.module, "test_name", "default_module")

    project_path = os.path.dirname(os.path.dirname(__file__))

    request.cls.exe_dir = os.path.join(project_path, "exe_to_run")
