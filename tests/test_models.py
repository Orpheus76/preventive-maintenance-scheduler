import pytest
from src.models import SubTask, Task, TaskOccurrence, Week, Planning


# ─────────────────────────────────────────────
# SubTask
# ─────────────────────────────────────────────

def test_subtask_attributes():
    st = SubTask(subtask_id="ST001", name="Sensor calibration", duration=1.5, frequency=13, task_id="T001")
    assert st.subtask_id == "ST001"
    assert st.name == "Sensor calibration"
    assert st.duration == 1.5
    assert st.frequency == 13
    assert st.task_id == "T001"


# ─────────────────────────────────────────────
# Task
# ─────────────────────────────────────────────

def test_task_attributes():
    task = Task(task_id="T001", name="Maintenance - Boiler", frequency=13)
    assert task.task_id == "T001"
    assert task.name == "Maintenance - Boiler"
    assert task.frequency == 13
    assert task.subtasks == []


def test_task_get_total_duration_empty():
    task = Task(task_id="T001", name="Maintenance - Boiler", frequency=13)
    assert task.get_total_duration() == 0.0


def test_task_get_total_duration_single_subtask():
    task = Task(task_id="T001", name="Maintenance - Boiler", frequency=13)
    task.subtasks.append(SubTask("ST001", "Check", 2.5, 13, "T001"))
    assert task.get_total_duration() == 2.5


def test_task_get_total_duration_multiple_subtasks():
    task = Task(task_id="T001", name="Maintenance - Boiler", frequency=13)
    task.subtasks.append(SubTask("ST001", "Check A", 1.0, 13, "T001"))
    task.subtasks.append(SubTask("ST002", "Check B", 2.5, 13, "T001"))
    task.subtasks.append(SubTask("ST003", "Check C", 0.5, 13, "T001"))
    assert task.get_total_duration() == pytest.approx(4.0)


# ─────────────────────────────────────────────
# TaskOccurrence
# ─────────────────────────────────────────────

def test_task_occurrence_attributes():
    task = Task(task_id="T001", name="Maintenance - Boiler", frequency=13)
    occ = TaskOccurrence(task=task, week_number=5, duration=3.0)
    assert occ.task is task
    assert occ.week_number == 5
    assert occ.duration == 3.0


# ─────────────────────────────────────────────
# Week
# ─────────────────────────────────────────────

def test_week_initial_load_is_zero():
    week = Week(week_number=1)
    assert week.total_load() == 0.0


def test_week_add_occurrence_updates_load():
    week = Week(week_number=1)
    task = Task(task_id="T001", name="Maintenance - Boiler", frequency=13)
    occ = TaskOccurrence(task=task, week_number=1, duration=3.0)
    week.add_occurrence(occ)
    assert week.total_load() == 3.0


def test_week_add_multiple_occurrences():
    week = Week(week_number=1)
    task = Task(task_id="T001", name="Maintenance - Boiler", frequency=13)
    week.add_occurrence(TaskOccurrence(task, 1, 2.0))
    week.add_occurrence(TaskOccurrence(task, 1, 1.5))
    assert week.total_load() == pytest.approx(3.5)


# ─────────────────────────────────────────────
# Planning
# ─────────────────────────────────────────────

def test_planning_initializes_52_weeks():
    planning = Planning(tasks=[])
    assert len(planning.weeks) == 52


def test_planning_weeks_are_numbered_1_to_52():
    planning = Planning(tasks=[])
    assert planning.weeks[0].week_number == 1
    assert planning.weeks[-1].week_number == 52


def test_planning_stores_tasks():
    task = Task(task_id="T001", name="Maintenance - Boiler", frequency=13)
    planning = Planning(tasks=[task])
    assert len(planning.tasks) == 1
    assert planning.tasks[0] is task