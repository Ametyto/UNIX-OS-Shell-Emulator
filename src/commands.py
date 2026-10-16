import config

errors = {
    "too_many_args": "Слишком много аргументов.",
    "args_not_provided": lambda cmd: f"Команда {cmd} не принимает аргументов.",
    "cmd_not_exist": lambda cmd: f"Несуществующая команда: {cmd}"
}

def cmd_help(command, args):
    if len(args)==0:
        return f"Доступные команды: {", ".join(map(str, commands.keys()))}"
    elif len(args)>1:
        return errors["too_many_args"]
    elif args[0] in commands.keys():
        return commands[args[0]]["desc"]
    else:
        return f"Неправильный аргумент. Команды {args[0]} не существует."

def cmd_echo(command, args):
    return f"{" ".join(map(str, args))}"

def cmd_conf_dump(command, args):
    if len(args)>0:
        return errors["args_not_provided"](command)
    vfs_message = f"vfs: {config.settings['vfs_path']}"
    script_message = f"script: {config.settings['script_path']}"
    return vfs_message + "\n" + script_message

def cmd_exit(command, args):
    if len(args)>0:
        return errors["args_not_provided"](command)
    return "__EXIT__"

def stub(command, args):
    if len(args)>0:
        args_better = " ".join(str(arg) for arg in args)
        return f"Команда: {command}, аргументы: {args_better}"
    return f"Команда: {command}, аргументы: нет"

commands = {
    "help": {
        "func": cmd_help,
        "desc": "Команда help позволяет узнать информацию о доступных"
        " командах. Можно ввести один аргумент, соответствующий команде,"
        " чтобы узнать о ней и её синтаксисе. Пример: help exit"
    },
    "echo": {
        "func": cmd_echo,
        "desc": "Команда echo выводит переданный ей текст"
        "или значение переменных на экран. Пример: echo $USER"
    },
    "cd": {
        "func": stub,
        "desc": "Команда cd пока в разработке"
    },
    "ls": {
        "func": stub,
        "desc": "Команда ls пока в разработке"
    },
    "exit": {
        "func": cmd_exit,
        "desc": "Команда exit закрывает консоль. Аргументы не предполагаются."
    },
    "conf-dump": {
        "func": cmd_conf_dump,
        "desc": "Команда conf-dump выводит информацию"
        "о текущих параметрах приложения. Аргументы не предполагаются."
    },
}