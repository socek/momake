from logan.dependency import FileDependency
from logan.dependency import TaskDependency
from logan.runner import Runner
from logan.task import Task


class Readme(Task):
    name = "readme"

    dependecies = [
        FileDependency(".", "README.md"),
    ]

    def action(self):
        print("readme task")


readme = Readme()


class Lint(Task):
    name = "lint"

    dependecies = [
        TaskDependency(readme),
        FileDependency("logan", "*.py"),
    ]

    def action(self):
        print("lint task")


runner = Runner()
runner.add_task(Lint())
runner.add_task(readme)
runner.run("lint")
