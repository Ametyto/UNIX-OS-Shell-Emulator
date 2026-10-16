import os
import eel

import config
import commands
import environment

script_dir = os.path.dirname(os.path.abspath(__file__))
web_dir = os.path.join(script_dir, "web")
eel.init(web_dir)

@eel.expose
def get_user():
    return environment.USERHOST

@eel.expose
def run_start_script():
    script_path = config.settings.get("script_path")
    if not script_path or not os.path.exists(script_path):
        return ["__NO_PATH__"]
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

    parts = environment.replace_vars(cmd).split(maxsplit=1)
    if "__NOT_FOUND__" in parts:
            return "Ошибка. Переменной не существует."
    command_name = parts[0]
    args = parts[1].split() if len(parts) > 1 else []

    if command_name in commands.commands: 
        cmd_func = commands.commands[command_name]["func"]
        return cmd_func(command_name, args)
    else:
        return commands.errors["cmd_not_exist"](command_name)

if __name__ == "__main__":
    config.init_config()
    eel.start("index.html", mode='edge', size=(800, 500))