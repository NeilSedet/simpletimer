import datetime
import sys
import json

filename = "log.json"
argumentList = sys.argv[1:]

now = datetime.datetime.now()


def strfdelta(tdelta, fmt):
    d = {"d": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    return fmt.format(**d)


def convert_to_timedelta(self, string):
        """
        Returns a time delta for strings in a format of: 0:00:00:00.0000
        Using RegEx to not introduce a dependancy on another package
        """
        dt_re = re.compile(r'^(\d+):(\d\d):(\d\d):(\d\d).(\d+)$')
        tmp = dt_re.match(string)
        try:
            days = self._regex_number_to_int(tmp, 1)
            hours = self._regex_number_to_int(tmp, 2)
            mins = self._regex_number_to_int(tmp, 3)
            secs = self._regex_number_to_int(tmp, 4)
            subsecs = self._regex_number_to_int(tmp, 5)
            td = datetime.timedelta(days=days, seconds=secs, microseconds=subsecs, minutes=mins, hours=hours)
            return td
        except AttributeError:
            self.log.info('Unable to convert %s to timedelta', string)
        except TypeError:
            self.log.info('Unable to convert %s to type timedelta', string)


def datetime_string(x):
    if isinstance(x, str):
        return datetime.datetime.strptime(x, "%m:%d:%Y %H:%M:%S")
    elif isinstance(x, datetime.timedelta):
        # return strfdelta(x, "{d} {H}:{M}:{S}")
        return str(x)
    else:
        try:
            return x.strftime("%m:%d:%Y %H:%M:%S")
        except:
            t = datetime.datetime.strptime(t,"%H:%M:%S")
            return datetime.timedelta(days=t.days, hours=t.hour, minutes=t.minute, seconds=t.second)



try:
    action = argumentList[0]
    task = argumentList[1]
except:
    print("Usage: simp {action} {task}")
    print("Type simp help for more info")
    exit()


def start():
    with open(filename, "r", encoding="utf-8") as file:

        data = json.loads(file.read())
        data[task] = dict()

        data[task]["last_runtime"] = datetime_string(now)
        data[task]["status"] = "running"
        data[task]["time_elapsed"] = "0 0:0:0"

        json_out = json.dumps(data, indent=4, sort_keys=True)

        with open(filename, "w") as outfile:
            outfile.write(json_out)


def stop():
    with open(filename, "r", encoding="utf-8") as file:
        data = json.loads(file.read())
        assert task in data, "Task not created"

        data[task]["status"] = "paused"
        data[task]["time_elapsed"] = datetime_string(
            datetime_string(data[task]["time_elapsed"])
            + (now - datetime_string(data[task]["last_runtime"]))
        )

        json_out = json.dumps(data, indent=4, sort_keys=True)

        with open(filename, "w") as outfile:
            outfile.write(json_out)


def resume():
    with open(filename, "r", encoding="utf-8") as file:
        data = json.loads(file.read())

        data[task]["last_runtime"] = datetime_string(now)
        data[task]["status"] = "running"

        json_out = json.dumps(data, indent=4, sort_keys=True)

        with open(filename, "w") as outfile:
            outfile.write(json_out)


locals()[action]()
