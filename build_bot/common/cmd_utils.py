import os
import subprocess
import tempfile

ERROR_INVALID_FUNCTION = 1
ERROR_PROC_NOT_FOUND = 127


def shell(cmd, env=None):
    print("calling command: " + str(cmd))
    p = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (std_out, std_err) = p.communicate()

    return p.returncode, std_out, std_err


def split_lines(text):
    if type(text).__name__ == 'bytes':
        text = text.decode('utf-8').strip('\n\r\t ')
    return [line.strip('\n\r') for line in text.split('\n')]


def find_tool(tool):
    print("try to find tool: " + tool)
    [returncode, std_out, std_err] = shell(['where', tool])

    paths = split_lines(std_out)
    for x in paths:
        print(x)

    is_found = True
    if returncode == ERROR_PROC_NOT_FOUND or returncode == ERROR_INVALID_FUNCTION:
        is_found = False

    return is_found, paths


def set_env(bat_file):
    # Run the command and pipe to a tempfile
    temp = tempfile.mktemp()
    cmd = '%s && set > %s' % (bat_file, temp)
    login = subprocess.Popen(cmd, shell=True)
    login.wait()

    # Parse the output
    data = []
    if os.path.isfile(temp):
        with open(temp, 'r') as file:
            data = file.readlines()
        os.remove(temp)

    # Every line will set an env variable
    for env in data:
        env = env.strip().split('=')
        os.environ[env[0]] = env[1]


def screen_str(string):
    return "\"" + string + "\""