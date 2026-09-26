import os
import eel
import getpass
import platform
import json

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

def replace_vars(args):
    """Парсер. Поиск переменных и замена их на их значения"""
    if "$" in args:
        ind_start = args.find("$")
        while ind_start != -1:
            ind_end = len(args)
            for i in range(ind_start, len(args)):
                if args[i] == " ":
                    ind_end = i
                    break
            if args[ind_start+1:ind_end] in variables.keys():
                var = variables.get(args[ind_start+1:ind_end])
                args = args[:ind_start] + var + args[ind_end:]
            else: 
                return "__ERR_VARS__"
            ind_start = args.find("$", ind_start + len(var))
    return args     

@eel.expose
def get_user():
    return username

@eel.expose
def process_command(cmd: str) -> str:
    """Обработка команд и их выполнение"""
    cmd = cmd.strip()
    if not cmd:
        return ""

    parts = cmd.split(maxsplit=1)
    command = parts[0].lower()
    args_joined = parts[1] if len(parts) > 1 else ""
    args = replace_vars(args_joined).split()
    if len(args)==1 and args[0]=="__ERR_VARS__":
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
            return f"Команда: {command}, аргументы: {args_joined}"
        return f"Команда: {command}, аргументы: нет"
    elif command == "exit":
        if len(args)>0:
            return f"Команда {command} не принимает аргументов."
        return "__EXIT__"
    else:
        return f"Несуществующая команда: {command}"

if __name__ == "__main__":
    eel.start("index.html", mode='edge', size=(800, 500))