import re
import os
import getpass
import platform

USERNAME = getpass.getuser()
HOSTNAME = platform.node()
USERHOST = f"{USERNAME}@{HOSTNAME}"
HOME = os.environ.get('HOME') or os.environ.get('USERPROFILE')

variables = {
    "HOME": HOME,
    "USER": USERNAME,
    "HOSTNAME": HOSTNAME
}

def get_var_value(match):
    var_name = match.group(1)
    if var_name in variables:
        return str(variables[var_name])
    return "__NOT_FOUND__"

def replace_vars(args):
    result = re.sub(r'\$(\S+)', get_var_value, args)
    return result     