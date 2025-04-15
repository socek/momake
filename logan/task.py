from datetime import datetime
from datetime import timezone


class Task:
    name = None
    dependecies = []

    def __init__(self):
        self.runlog = {}
        self.last_runlog = None

    def feed_last_runlog(self, last_runlog: dict):
        self.last_runlog = last_runlog

    def get_last_runtime(self):
        if "runtime" in self.last_runlog:
            return datetime.fromisoformat(self.last_runlog["runtime"])

    def should_run(self):
        last_runtime = self.get_last_runtime()
        for dependency in self.dependecies:
            if dependency.should_run(last_runtime):
                return True
        return False

    def action(self):
        pass

    def run(self):
        print(f"Checking {self.name}...")
        self.runlog["check_runtime"] = datetime.now(timezone.utc)
        if self.should_run():
            self.runlog["runtime"] = datetime.now(timezone.utc)
            print(f"Running {self.name}...")
            self.action()
            self.runlog["runtime_finish"] = datetime.now(timezone.utc)
            return True
        else:
            return False

    def collect_runlog(self):
        runlog = {
            "check_runtime": self.runlog["check_runtime"].isoformat(),
        }
        if self.runlog.get("runtime"):
            runlog["runtime"] = self.runlog["runtime"].isoformat()
            runlog["runtime_finish"] = self.runlog["runtime_finish"].isoformat()
        return runlog
