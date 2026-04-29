import statistics
from typing import List
from models import Task, Week, TaskOccurrence, Planning 


class TaskSorter:
    """
    Sorts tasks before placement to assist the greedy algorithm.
    Chosen heuristic:
    1. Shortest frequency first (e.g., Weekly before Yearly).
    2. In case of a tie, longest total duration first (Largest Processing Time First).
    """
    @staticmethod
    def sort(tasks: List[Task]) -> List[Task]:
        # First sort by ascending frequency (shortest periods = highest priority)
        # Then by descending duration (the '-' sign inverts the secondary sort direction)
        return sorted(tasks, key=lambda t: (t.frequency, -t.get_total_duration()))


class GreedyScheduler:
    """
    Greedy scheduling algorithm.
    Iteratively places tasks in the calendar, aiming to level the workload 
    while strictly respecting their frequency of occurrence.
    """
    def schedule(self, tasks: List[Task], weeks: List[Week]) -> None:
        # 1. Sort tasks to maximize the heuristic's efficiency
        sorted_tasks = TaskSorter.sort(tasks)

        for task in sorted_tasks:
            duration = task.get_total_duration()
            freq = task.frequency

            # Special case: Weekly tasks (freq = 1) -> place them in every week
            if freq == 1:
                for week in weeks:
                    week.add_occurrence(TaskOccurrence(task, week.week_number, duration))
                continue

            # General case: Find the best starting week within the allowed placement window
            # The allowed starting window corresponds to the first 'freq' weeks.
            # E.g., for a quarterly task (freq = 13), it must start between Week 1 and Week 13.
            search_window = weeks[:freq]

            # Select the starting week that currently has the lowest workload
            best_start_week = min(search_window, key=lambda w: w.total_load())

            # Place this occurrence and all subsequent ones, jumping by 'freq' weeks
            current_week_num = best_start_week.week_number
            while current_week_num <= 52:
                # The index in the 'weeks' list starts at 0, so we use (number - 1)
                target_week = weeks[current_week_num - 1]
                target_week.add_occurrence(TaskOccurrence(task, current_week_num, duration))

                # Move to the next occurrence
                current_week_num += freq


class WorkloadVarianceEvaluator:
    """
    Evaluates the fitness of a Planning by computing the statistical variance of the workload across all weeks.
    A lower variance means a more balanced schedule. 
    """
