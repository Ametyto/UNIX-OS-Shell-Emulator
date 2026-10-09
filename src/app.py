import os
import eel
import getpass
import platform
import json
import re
import argparse

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
config = {
    "vfs_path" : "",
    "script_path" : ""
}

def init_config():
    global config
    parser = argparse.ArgumentParser(description="UNIX OS Shell Emulator")
    parser.add_argument("--vfs")
    parser.add_argument("--script")

    args, _ = parser.parse_known_args()

    if args.vfs:
        if os.path.exists(args.vfs):
            config["vfs_path"] = os.path.abspath(args.vfs)
        else:
            config["vfs_path"] = "not found"
            print("[ПРЕДУПРЕЖДЕНИЕ] Путь к VFS не был найден.")
    else:
        config["vfs_path"] = "not specified"

    if args.script:
        if os.path.exists(args.script) and os.path.isfile(args.script):
            config["script_path"] = os.path.abspath(args.script)
        else:
            config["script_path"] = "not found"
            print("[ПРЕДУПРЕЖДЕНИЕ] Путь к скрипту не был найден.")
    else:
        config["script_path"] = "not specified"


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
def run_start_script():
    script_path = config.get("script_path")
    if not script_path or not os.path.exists(script_path):
        return ["__ERROR_NO_PATH__"]
    file = open(script_path, "r", encoding="utf-8")
    result = []
    for line in file:
        cmd = line.strip()
        if cmd:
            result.append(cmd)
            result.append(process_command(cmd))
    return result

@eel.expose
def process_command(cmd: str) -> str:
    cmd = cmd.strip()
    if not cmd:
        return ""

    parts = replace_vars(cmd).split(maxsplit=1)
    if "__NOT_FOUND__" in parts:
            return "Ошибка. Переменной не существует."
    command = parts[0]
    args = parts[1].split() if len(parts) > 1 else ""

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
        return f"{" ".join(map(str, args))}"
    elif command == "ls" or command == "cd":
        if len(args)>0:
            return f"Команда: {command}, аргументы: {" ".join(str(arg) for arg in args)}"
        return f"Команда: {command}, аргументы: нет"
    elif command == "conf-dump":
        if len(args)>0:
            return f"Команда {command} не принимает аргументов."
        return f"vfs: {config['vfs_path']}\nscript: {config['script_path']}"
    elif command == "exit":
        if len(args)>0:
            return f"Команда {command} не принимает аргументов."
        return "__EXIT__"
    else:
        return f"Несуществующая команда: {command}"

if __name__ == "__main__":
    init_config()
    eel.start("index.html", mode='edge', size=(800, 500))