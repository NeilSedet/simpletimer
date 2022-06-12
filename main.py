import datetime
import sys
import json

filename = "log.json"
argumentList = sys.argv[1:]
action = argumentList[0]
task = argumentList[1]

now = datetime.datetime.now()
date_time = now.strftime("%m:%d:%Y %H:%M:%S\n")

with open(filename, "r", encoding="utf-8") as file:
    data = json.loads(file.read())



def start():
    with open(filename, "r", encoding="utf-8") as file:
        last_line = file.readlines()[-1]
        old_action = last_line.partition(" ")[0]

        if old_action == 'start' or old_action == 'resume':
            print("Task already started")
            return

    with open(filename, "a", encoding="utf-8") as out:
        out.write(f"{action} {date_time}")


def stop():
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        last_line = lines[-1]
        old_action = last_line.partition(" ")[0]

        if old_action == 'stop':
            print("No task started")
            return

        if old_action == "resume":
            last_line = lines[-2]

        str_old_date_time = last_line.partition(" ")[2]
        old_date_time = datetime.datetime.strptime(
            str_old_date_time, "%m:%d:%Y %H:%M:%S\n"
        )
        diff = now - old_date_time
        no_seconds = ":".join(str(diff).split(":")[:2])
        print(no_seconds)

    with open(filename, "a", encoding="utf-8") as out:
        out.write(f"{action} {date_time}")


def clear():
    with open(filename, "w", encoding="utf-8") as out:
        out.write("log.txt\n")
        out.write("---\n")


def resume():
    with open(filename, "r", encoding="utf-8") as file:
        last_line = file.readlines()[-1]
        old_action = last_line.partition(" ")[0]

        if old_action == 'start' or old_action == 'resume':
            print("Task not paused")
            return

    with open(filename, "a", encoding="utf-8") as out:
        out.write(f"{action} {date_time}")


locals()[action]()
