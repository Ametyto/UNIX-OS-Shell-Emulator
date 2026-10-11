import argparse
import os

settings = {
    "vfs_path" : "",
    "script_path" : ""
}

def init_config():
    global settings
    parser = argparse.ArgumentParser(description="UNIX OS Shell Emulator")
    parser.add_argument("--vfs")
    parser.add_argument("--script")

    args, _ = parser.parse_known_args()

    if args.vfs:
        if os.path.exists(args.vfs):
            settings["vfs_path"] = os.path.abspath(args.vfs)
        else:
            settings["vfs_path"] = "not found"
            print("[ПРЕДУПРЕЖДЕНИЕ] Путь к VFS не был найден.")
    else:
        settings["vfs_path"] = "not specified"

    if args.script:
        if os.path.exists(args.script) and os.path.isfile(args.script):
            settings["script_path"] = os.path.abspath(args.script)
        else:
            settings["script_path"] = "not found"
            print("[ПРЕДУПРЕЖДЕНИЕ] Путь к скрипту не был найден.")
    else:
        settings["script_path"] = "not specified"