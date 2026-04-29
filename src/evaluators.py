import math
from typing import List
from .models import Planning


class WorkloadVarianceEvaluator:
    """
    Evaluates the quality of a generated schedule.
    A lower standard deviation indicates a more balanced workload distribution.
    """

    @staticmethod
    def evaluate(planning: Planning) -> dict:
        loads = [w.total_load() for w in planning.weeks]

        if not loads:
            return {}

        total_hours = sum(loads)
        mean_load = total_hours / len(loads)
        variance = sum((load - mean_load) ** 2 for load in loads) / len(loads)

        return {
            "total_hours": round(total_hours, 2),
            "mean_weekly_load": round(mean_load, 2),
            "variance": round(variance, 2),
            "std_deviation": round(math.sqrt(variance), 2),
            "max_week_load": round(max(loads), 2),
            "min_week_load": round(min(loads), 2)
        }