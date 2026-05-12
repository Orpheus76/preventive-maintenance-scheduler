import pandas as pd
from .models import Task, SubTask

PERIODICITY_MAP = {
    "Mensuelle": 4,
    "Trimestrielle": 13,
    "Semestrielle": 26,
    "Annuelle": 52,
}

class ExcelService:
    """
    Handles all I/O operations with Excel files.
    Responsible for reading raw maintenance data and building domain objects.
    Strictly isolated from the scheduling logic (Single Responsibility Principle)
    """

    @staticmethod
    def read_data(filepath: str) -> list[Task]:
        """
        Reads the Excel file and constructs a list of Task objects,
        each populated with their corresponding SubTask objects.
        """
        df = pd.read_excel(filepath)
        tasks_dict: dict[str, Task] = {}

        for _, row in df.iterrows():
            t_id = str(row["task_id"]).strip()
            periodicity = str(row["periodicity"]).strip()
            freq = PERIODICITY_MAP[periodicity]

            if t_id not in tasks_dict:
                tasks_dict[t_id] = Task(
                    task_id=t_id,
                    name=str(row["task_name"]).strip(),
                    frequency=freq,
                )

            subtask = SubTask(
                subtask_id=str(row["subtask_id"]).strip(),
                name=str(row["subtask_name"]).strip(),
                duration=float(row["duration_hours"]),
                frequency=freq,
                task_id=t_id,
            )

            tasks_dict[t_id].subtasks.append(subtask)

        return list(tasks_dict.values())