import pandas as pd
from .models import Task, SubTask


class ExcelService:
    """
    Handles all I/O operations with Excel files.
    Responsible for reading raw maintenance data and building domain objects.
    Strictly isolated from the scheduling logic (Single Responsiblity Principle)
    """

    @staticmethod
    def read_data(filepath: str) -> list[Task]:
        """
        Reads the Excel file and constructs a list of Task objects, each populated with their corresponding SubTask objects.
        """
        df = pd.read_excel(filepath)
        tasks_dict: dict[str, Task] = {}

        for _, row in df.iterrows():
            t_id = str(row["task_id"])

            # If the Task doesn't exist yet, create and register it
            if t_id not in tasks_dict:
                tasks_dict[t_id] = Task(
                    task_id = t_id,
                    name = str(row["task_name"]),
                    frequency = int(row["frequency_weeks"]),
                )

            # Create the SubTask and attach it to its parent Task
            subtask = SubTask(
                subtask_id = str(row["subtask_id"]),
                name = str(row["subtask_name"]),
                duration = float(row["duration_hours"]),
                frequency = int(row["frequency_weeks"]),
                task_id = t_id,
            )
            tasks_dict[t_id].subtasks.append(subtask)

        return list(tasks_dict.values())