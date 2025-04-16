from logging import DEBUG
from logging import basicConfig

from click import argument
from click import command
from click import echo
from click import get_current_context
from click import option

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
        self.tasks[taskname].run()

    def list_tasks(self):
        echo("Avalible tasks:")
        for task in self.tasks.values():
            echo(f"- {task.name}")


@command()
@argument("name", required=False, default=None)
@option("-l", "--list-tasks", default=False, is_flag=True, help="number of greetings")
@option("-c", "--clear", default=False, is_flag=True, help="clear database")
@option("-d", "--debug", default=False, is_flag=True, help="show debug logs")
def cmd(name: str, list_tasks: bool, clear: bool, debug: bool):
    if debug:
        basicConfig(level=DEBUG, format="%(message)s")

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
