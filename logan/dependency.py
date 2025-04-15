from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import Optional

from logan.task import Task


class Dependency:
    def has_changed(self) -> bool:
        pass

    def should_run(self, last_runtime: datetime):
        if not last_runtime:
            return True
        return self.has_changed(last_runtime)


class FileDependency(Dependency):
    def __init__(self, path: str, pattern: str):
        super().__init__()
        self.path = path
        self.pattern = pattern

    def has_changed(self, last_runtime: datetime) -> bool:
        pathobj = Path(self.path)
        for path in pathobj.rglob(self.pattern):
            modified = datetime.fromtimestamp(path.lstat().st_mtime, tz=timezone.utc)
            if modified > last_runtime:
                return True
        return False


class TaskDependency(Dependency):
    def __init__(self, task: Task):
        super().__init__()
        self.task = task

    def has_changed(self, last_runtime: datetime) -> bool:
        return self.task.run()
