import typing
from provider import namespace
import provider

from provider.dataclass import ModelMeta


LoaderFunc = typing.Callable[[typing.Any], None]


P = typing.TypeVar("P", bound=provider.Provider)


class Task(metaclass=ModelMeta):
    def __init__(self, **data: typing.Any) -> None:
        setattr(self, "__dict__", data)

    def json(self) -> dict:
        return {"task": self.__class__.__name__, "ctx": self.__dict__}

    def run(self, p) -> None:
        """
        Runs the task to fetch resources.
        """
        raise Exception("the run method must be implemented")


_PENDING_TASKS: typing.List[Task] = []


def _reset():
    global _PENDING_TASKS
    _PENDING_TASKS = []


def call(task: Task):
    """
    Registers the intent to call an async task. The task will be deferred
    and executed in the future.
    """
    _PENDING_TASKS.append(task)


def _execute(provider: provider.Provider, task: str, ctx: typing.Optional[dict]):
    """
    Actually execute a task.

    The task can either be a top-level resource loader, defined with the
    `@resources.fetcher` decorator, or a subtask class
    (e.g. `class MyTask(tasks.Task)`).

    Top-level resource loaders do not accept any context values.
    """
    # check if we have a top-level resource loader registered under the name
    resource_loader = namespace._RESOURCE_LOADERS.get(task)
    if resource_loader is not None:
        return resource_loader(provider)

    if ctx is None:
        ctx = {}

    for Klass in Task.__subclasses__():
        # todo: handle ambiguity in task class naming
        if Klass.__name__ == task:
            task = Klass(**ctx)
            return task.run(provider)

    # if we get here, we couldn't find the task.
    raise Exception(f"could not find task {task}")


def get() -> typing.List[Task]:
    return _PENDING_TASKS
