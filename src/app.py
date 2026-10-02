import os
import eel
import getpass
import platform
import json
import re

username = getpass.getuser()
hostname = platform.node()
username = f"{username}@{hostname}"

script_dir = os.path.dirname(os.path.abspath(__file__))
web_dir = os.path.join(script_dir, "web")
eel.init(web_dir)

commands_path = os.path.join(script_dir, "commands.json")
with open(commands_path, "r", encoding="utf-8") as commands_file:
    commands = json.load(commands_file)

home = os.environ.get('HOME') or os.environ.get('USERPROFILE')
variables = {"HOME":home,
             "TEST":"TEST_T"}

def get_var_value(match):
    var_name = match.group(1)
    if var_name in variables:
        return str(variables[var_name])
    return "__NOT_FOUND__"

def replace_vars(args):
    result = re.sub(r'\$(\S+)', get_var_value, args)
    return result     

@eel.expose
def get_user():
    return username

@eel.expose
def process_command(cmd: str) -> str:
    cmd = cmd.strip()
    if not cmd:
        return ""

    parts = cmd.split(maxsplit=1)
    command = parts[0].lower()
    args_joined = parts[1] if len(parts) > 1 else ""
    args = replace_vars(args_joined).split()
    if "__NOT_FOUND__" in args:
        return "Ошибка. Переменной не существует."

    if command == "help":
        if len(args)==0:
            return f"Доступные команды: {", ".join(map(str, commands.keys()))}"
        elif len(args)>1:
            return "Слишком много аргументов."
        elif args[0] in commands.keys():
            return commands.get(args[0])
        else:
            return f"Неправильный аргумент. Команды {args[0]} не существует."
    elif command == "echo":
        return f"echo {", ".join(map(str, args))}"
    elif command == "ls" or command == "cd":
        if len(args)>0:
            return f"Команда: {command}, аргументы: {" ".join(str(arg) for arg in args)}"
        return f"Команда: {command}, аргументы: нет"
    elif command == "exit":
        if len(args)>0:
            return f"Команда {command} не принимает аргументов."
        return "__EXIT__"
    else:
        return f"Несуществующая команда: {command}"

if __name__ == "__main__":
    eel.start("index.html", mode='edge', size=(800, 500))