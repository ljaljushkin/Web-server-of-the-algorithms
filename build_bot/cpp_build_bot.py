import os
from common_part import find_tool, shell


class CppBuildBot:
    def __init__(self):
        self.path_vcvarsall = self._find_vcvarall()
        if self.path_vcvarsall is not None:
            print(shell([self.path_vcvarsall]))
            cl_path = self.path_vcvarsall + "\\..\\bin\\cl.exe"
            # [is_found, cl_path] = find_tool("cl")
            # if is_found:
            print(shell(cl_path))
            # else:
            # print("cl was not found")
        else:
            print("vcvarall was not found")

    def _find_vcvarall(self):
        vs_versions = ["11.0", "10.0"]

        for curr_version in vs_versions:
            path_vcvarsall = 'C:\\Program Files (x86)\\Microsoft Visual Studio {version}\\VC\\vcvarsall.bat'.format(
                version=curr_version)
            print(path_vcvarsall)
            if os.path.exists(path_vcvarsall):
                return path_vcvarsall
        return None
