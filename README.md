# Logan

Proof of concept for a python make

# How to use

```
$ poetry install
$ poetry run logan
```

All tasks needs to be in `logantasks.py` or `logantasks` module.

Example:

```
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

```
