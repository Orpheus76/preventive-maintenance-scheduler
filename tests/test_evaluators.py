import pytest
import math
from src.models import Task, TaskOccurrence, Planning
from src.evaluators import WorkloadVarianceEvaluator


# ─── Helper ───────────────────────────────────

def make_planning_with_loads(loads: list[float]) -> Planning:
    planning = Planning(tasks=[])
    dummy_task = Task(task_id="T_dummy", name="Dummy", frequency=52)
    for i, load in enumerate(loads):
        occ = TaskOccurrence(task=dummy_task, week_number=i + 1, duration=load)
        planning.weeks[i].add_occurrence(occ)
    return planning


# ─────────────────────────────────────────────
# Structure du résultat
# ─────────────────────────────────────────────

def test_evaluate_returns_dict():
    planning = Planning(tasks=[])
    assert isinstance(WorkloadVarianceEvaluator.evaluate(planning), dict)


def test_evaluate_returns_all_expected_keys():
    result = WorkloadVarianceEvaluator.evaluate(Planning(tasks=[]))
    expected = {"total_hours", "mean_weekly_load", "variance", "std_deviation", "max_week_load", "min_week_load"}
    assert expected == set(result.keys())


# ─────────────────────────────────────────────
# Planning vide
# ─────────────────────────────────────────────

def test_evaluate_empty_planning_total_hours_is_zero():
    result = WorkloadVarianceEvaluator.evaluate(Planning(tasks=[]))
    assert result["total_hours"] == 0.0


def test_evaluate_empty_planning_variance_is_zero():
    result = WorkloadVarianceEvaluator.evaluate(Planning(tasks=[]))
    assert result["variance"] == 0.0
    assert result["std_deviation"] == 0.0


# ─────────────────────────────────────────────
# Charge uniforme
# ─────────────────────────────────────────────

def test_evaluate_uniform_load_variance_is_zero():
    result = WorkloadVarianceEvaluator.evaluate(make_planning_with_loads([10.0] * 52))
    assert result["variance"] == 0.0
    assert result["std_deviation"] == 0.0


def test_evaluate_uniform_load_mean_is_correct():
    result = WorkloadVarianceEvaluator.evaluate(make_planning_with_loads([10.0] * 52))
    assert result["mean_weekly_load"] == pytest.approx(10.0)


def test_evaluate_uniform_load_total_hours_is_correct():
    result = WorkloadVarianceEvaluator.evaluate(make_planning_with_loads([10.0] * 52))
    assert result["total_hours"] == pytest.approx(520.0)


# ─────────────────────────────────────────────
# Valeurs calculées
# ─────────────────────────────────────────────

def test_evaluate_std_deviation_equals_sqrt_variance():
    result = WorkloadVarianceEvaluator.evaluate(make_planning_with_loads([20.0, 30.0]))
    assert result["std_deviation"] == pytest.approx(math.sqrt(result["variance"]), abs=0.01)


def test_evaluate_max_week_load():
    result = WorkloadVarianceEvaluator.evaluate(make_planning_with_loads([5.0, 15.0, 10.0]))
    assert result["max_week_load"] == pytest.approx(15.0)


def test_evaluate_min_week_load_is_zero_for_empty_weeks():
    result = WorkloadVarianceEvaluator.evaluate(make_planning_with_loads([5.0, 15.0, 10.0]))
    assert result["min_week_load"] == pytest.approx(0.0)


def test_evaluate_values_are_rounded_to_2_decimals():
    result = WorkloadVarianceEvaluator.evaluate(make_planning_with_loads([1.0, 2.0, 3.0]))
    for key, value in result.items():
        assert value == round(value, 2), f"{key} n'est pas arrondi à 2 décimales : {value}"