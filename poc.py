from logan.dependency import FileDependency
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
        readme,
        FileDependency("logan", "*.py"),
    ]

    def action(self):
        print("lint task")


Lint().run()
