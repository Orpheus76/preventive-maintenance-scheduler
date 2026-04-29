from typing import List


class SubTask:
    def __init__(self, subtask_id: str, name: str, duration: float, frequency: int, task_id: str):
        self.subtask_id = subtask_id
        self.name = name
        self.duration = duration
        self.frequency = frequency
        self.task_id = task_id


class Task:
    def __init__(self, task_id: str, name: str, frequency: int):
        self.task_id = task_id
        self.name = name
        self.frequency = frequency
        self.subtasks: List[SubTask] = []

    def get_total_duration(self) -> float:
        return sum(st.duration for st in self.subtasks)


class TaskOccurrence:
    def __init__(self, task: Task, week_number: int, duration: float):
        self.task = task
        self.week_number = week_number
        self.duration = duration


class Week:
    def __init__(self, week_number: int):
        self.week_number = week_number
        self.assigned_occurrences: List[TaskOccurrence] = []

    def total_load(self) -> float:
        return sum(occ.duration for occ in self.assigned_occurrences)
    
    def add_occurrence(self, occ: TaskOccurrence):
        self.assigned_occurrences.append(occ)


class Planning:
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks
        self.weeks =[Week(i) for i in range(1, 53)]
    
    def plan(self, scheduler) -> None:
        """Délègue le placement à un objet respectant l'interface TaskScheduler."""
        scheduler.schedule(self.tasks, self.weeks)
