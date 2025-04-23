from logging import DEBUG
from logging import Handler
from logging import basicConfig
from os import getcwd
from pathlib import Path
from sys import path

from click import argument
from click import command
from click import echo
from click import get_current_context
from click import option
from click import style

from momake.exceptions import TaskFailed
from momake.finder import TaskFinder
from momake.runlog.commands import clear_database
from momake.task import Task


class Runner:
    def __init__(self):
        self.tasks: dict[str, Task] = {}

    def add(self, task: Task):
        assert task.name
        self.tasks[task.name] = task

    def run(self, taskname: str):
        try:
            self.tasks[taskname].run()
        except TaskFailed as er:
            ctx = get_current_context()
            echo(style(f"Task filed: {er.args[0]}", fg="red"))
            ctx.exit(1)

    def list_tasks(self):
        echo("Avalible tasks:")
        for task in self.tasks.values():
            echo(f"- {task.name}")


class SpecialHandler(Handler):
    fg = {
        "DEBUG": "blue",
        "INFO": "white",
        "WARNING": "yellow",
        "ERROR": "red",
    }

    def emit(self, record):
        fg = self.fg[record.levelname]
        echo(style(record.getMessage(), fg=fg))

def debug_on(ctx, param, value) -> bool:
    if not value:
        return False
    handler = SpecialHandler()
    basicConfig(level=DEBUG, format="%(message)s", handlers=[handler])
    return True

def search_task_path():
    selfpath = Path(getcwd())
    root = Path("/")
    while selfpath != root:
        dirname = selfpath / "momaketasks" / "__init__.py"
        filename = selfpath / "momaketasks.py"
        if dirname.exists or filename.exists:
            path.append(str(selfpath))
        selfpath = selfpath.parent

@command()
@argument("name", required=False, default=None)
@option("-l", "--list-tasks", default=False, is_flag=True, help="number of greetings")
@option("-c", "--clear", default=False, is_flag=True, help="clear database")
@option("-d", "--debug", default=False, is_flag=True, help="show debug logs", callback=debug_on)
def cmd(name: str, list_tasks: bool, clear: bool, debug: bool):
    search_task_path()

    if clear:
        clear_database()
        echo("Database deleted...")
        return

    runner = Runner()
    for taskcls in TaskFinder().find():
        task = taskcls()
        runner.add(task)

    if list_tasks:
        runner.list_tasks()
        return

    if name:
        runner.run(name)
        return

    ctx = get_current_context()
    echo(ctx.get_help())
    echo()
    runner.list_tasks()
