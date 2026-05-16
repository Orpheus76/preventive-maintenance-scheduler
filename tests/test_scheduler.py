import pytest
from src.models import SubTask, Task, TaskOccurrence, Week, Planning
from src.scheduler import TaskSorter, GreedyScheduler


# ─── Helpers ──────────────────────────────────

def make_task(task_id: str, frequency: int, durations: list[float]) -> Task:
    task = Task(task_id=task_id, name=f"Task {task_id}", frequency=frequency)
    for i, d in enumerate(durations):
        task.subtasks.append(SubTask(f"ST{i:03}", f"Sub {i}", d, frequency, task_id))
    return task


def make_weeks(n: int = 52) -> list[Week]:
    return [Week(i) for i in range(1, n + 1)]


# ─────────────────────────────────────────────
# TaskSorter
# ─────────────────────────────────────────────

def test_sorter_sorts_by_ascending_frequency():
    t_annual    = make_task("T_annual",    52, [5.0])
    t_quarterly = make_task("T_quarterly", 13, [3.0])
    t_monthly   = make_task("T_monthly",    4, [2.0])
    result = TaskSorter.sort([t_annual, t_quarterly, t_monthly])
    assert [t.frequency for t in result] == [4, 13, 52]


def test_sorter_lpt_tiebreak_same_frequency():
    t_small = make_task("T_small", 13, [1.0])
    t_large = make_task("T_large", 13, [5.0])
    result = TaskSorter.sort([t_small, t_large])
    assert result[0].task_id == "T_large"
    assert result[1].task_id == "T_small"


def test_sorter_does_not_mutate_original_list():
    tasks = [make_task("T1", 52, [1.0]), make_task("T2", 4, [1.0])]
    original_order = [t.task_id for t in tasks]
    TaskSorter.sort(tasks)
    assert [t.task_id for t in tasks] == original_order


# ─────────────────────────────────────────────
# GreedyScheduler — hebdomadaire (freq=1)
# ─────────────────────────────────────────────

def test_weekly_task_placed_in_all_52_weeks():
    task = make_task("T_weekly", 1, [1.0])
    weeks = make_weeks()
    GreedyScheduler().schedule([task], weeks)
    for week in weeks:
        assert len(week.assigned_occurrences) == 1


# ─────────────────────────────────────────────
# GreedyScheduler — trimestrielle (freq=13)
# ─────────────────────────────────────────────

def test_quarterly_task_placed_exactly_4_times():
    task = make_task("T_quarterly", 13, [3.0])
    weeks = make_weeks()
    GreedyScheduler().schedule([task], weeks)
    total = sum(len(w.assigned_occurrences) for w in weeks)
    assert total == 4


def test_quarterly_task_occurrences_spaced_by_13_weeks():
    task = make_task("T_quarterly", 13, [3.0])
    weeks = make_weeks()
    GreedyScheduler().schedule([task], weeks)
    occupied = [w.week_number for w in weeks if w.assigned_occurrences]
    for i in range(1, len(occupied)):
        assert occupied[i] - occupied[i - 1] == 13


# ─────────────────────────────────────────────
# GreedyScheduler — semestrielle (freq=26)
# ─────────────────────────────────────────────

def test_biannual_task_placed_exactly_2_times():
    task = make_task("T_biannual", 26, [2.0])
    weeks = make_weeks()
    GreedyScheduler().schedule([task], weeks)
    total = sum(len(w.assigned_occurrences) for w in weeks)
    assert total == 2


# ─────────────────────────────────────────────
# GreedyScheduler — annuelle (freq=52)
# ─────────────────────────────────────────────

def test_annual_task_placed_exactly_once():
    task = make_task("T_annual", 52, [4.0])
    weeks = make_weeks()
    GreedyScheduler().schedule([task], weeks)
    total = sum(len(w.assigned_occurrences) for w in weeks)
    assert total == 1


# ─────────────────────────────────────────────
# GreedyScheduler — équilibrage de la charge
# ─────────────────────────────────────────────

def test_scheduler_picks_lowest_load_start_week():
    heavy_task = make_task("T_heavy", 52, [100.0])
    quarterly_task = make_task("T_quarterly", 13, [3.0])
    weeks = make_weeks()
    weeks[0].add_occurrence(TaskOccurrence(heavy_task, 1, 100.0))
    GreedyScheduler().schedule([quarterly_task], weeks)
    occupied = [
        w.week_number for w in weeks
        if any(occ.task is quarterly_task for occ in w.assigned_occurrences)
    ]
    assert occupied[0] != 1


# ─────────────────────────────────────────────
# GreedyScheduler — via Planning.plan()
# ─────────────────────────────────────────────

def test_planning_plan_delegates_to_scheduler():
    task = make_task("T_monthly", 4, [1.0, 2.0])
    planning = Planning(tasks=[task])
    planning.plan(GreedyScheduler())
    total = sum(len(w.assigned_occurrences) for w in planning.weeks)
    assert total == 13