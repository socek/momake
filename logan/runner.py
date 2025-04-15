from collections.abc import Mapping
from json import dump
from json import load
from pathlib import Path

from logan.dependency import Dependency
from logan.task import Task


def deep_update(d, u):
    for k, v in u.items():
        if isinstance(v, Mapping):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def default_runlog():
    return {
        "tasks": {},
        # "dependencies": {},
    }


class Runner:
    def __init__(self):
        self.lastrun_log = None
        self.tasks: dict[str, Task] = {}
        self.dependecies: dict[str, Dependency] = {}

    def read_file(self):
        cache = Path("logan.json")
        if not cache.exists():
            self.lastrun_log = default_runlog()
            return

        with cache.open("r") as cachestream:
            self.lastrun_log = load(cachestream)

    def write_file(self, runlog):
        cache = Path("logan.json")
        newrunlog = deep_update({}, self.lastrun_log)
        deep_update(newrunlog, runlog)
        with cache.open("w") as cachestream:
            dump(newrunlog, cachestream)

    def add_task(self, task: Task):
        self.tasks[task.name] = task
        # for dependency in task.dependecies:
        #     if dependency.hashme() not in self.dependecies:
        #         self.dependecies[dependency.hashme()] = dependency

    def feed_tasks(self):
        runlog = self.lastrun_log["tasks"]
        for task in self.tasks.values():
            task.feed_last_runlog(runlog.get(task.name, {}))

    # def feed_dependecies(self):
    #     runlog = self.lastrun_log["dependencies"]
    #     for dependency in self.dependecies.values():
    #         dep_hash = dependency.hashme()
    #         dependency.feed_lastrun(runlog.get(dep_hash, {}))

    def collect_runlog(self):
        runlog = default_runlog()
        for task in self.tasks.values():
            runlog["tasks"][task.name] = task.collect_runlog()
        return runlog


    def run(self, taskname: str):
        self.read_file()
        self.feed_tasks()
        # self.feed_dependecies()

        self.tasks[taskname].run()

        runlog = self.collect_runlog()

        self.write_file(runlog)
