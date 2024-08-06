from tasks.challenge_1 import load, backup, restore
from tasks.challenge_2 import main as challenge_2

TASKS = {
    "LOAD": {"task": load.run},
    "BACKUP": {"task": backup.run},
    "RESTORE": {"task": restore.run},
    "REPORT": {"task": challenge_2.run},
}


class TaskManager:
    """
    A class representing a task manager.

    Args:
        task_data (dict): The data related to the task.
        session: The session object.

    Methods:
        run(): Executes the task.

    """

    def __init__(self, task_data, session):
        self.task_data = task_data
        self.session = session

    def run(self):
        task = TASKS.get(self.task_data["task"])
        return task["task"](
            self.task_data["data"], self.session, self.task_data["task_id"]
        )
