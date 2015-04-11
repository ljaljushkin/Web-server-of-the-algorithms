import subprocess


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
    if returncode == 127 or returncode == 1:
        is_found = False

    return is_found, paths
