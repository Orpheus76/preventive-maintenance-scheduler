# Preventive Maintenance Scheduler

A Python-based scheduling engine designed to optimally distribute annual preventive maintenance tasks. Built with a strong emphasis on Object-Oriented Programming (OOP), SOLID principles, and algorithmic heuristics.

## 🧠 Algorithmic Approach

Scheduling maintenance tasks is a combinatorial optimization problem. In this specific industrial context, tasks possess **sequence-dependent constraints** (the placement of one task heavily influences the feasibility of others). 
Because formulating this exactly (e.g., via MILP) leads to state-space explosion, this engine implements a **Greedy Heuristic**.

The scheduling pipeline is divided into two steps:
1. **Sorting (`TaskSorter`):** Determines the priority of tasks before placement (e.g., by Largest Processing Time or Highest Frequency).
2. **Scheduling (`TaskScheduler`):** Iteratively places `TaskOccurrence`s into `Week` buckets, aiming to minimize the variance of `total_load()` across the 52 weeks while strictly respecting frequency intervals.

## 🏗️ System Architecture

The architecture strictly separates the **Data Model**, the **Business Logic**, and the **I/O Operations**. 

```mermaid
classDiagram
    class SubTask {
        +id : str
        +name : str
        +duration : float
        +frequency : str
        +task_id : str
    }
    class Task {
        +id : str
        +name : str
        +subtasks : List[SubTask]
        +frequency : str
        +get_total_duration() float
    }
    class TaskOccurrence {
        +task : Task
        +week_number : int
        +duration : float
    }
    class Week {
        +week_number : int
        +assigned_occurrences : List[TaskOccurrence]
        +total_load() float
        +add_occurrence(occ)
    }
    class Planning {
        +tasks : List[Task]
        +weeks : List[Week]
        +plan(scheduler)
        +export_pdf()
    }
    class TaskSorter {
        +sort(tasks: List[Task]) List[Task]
    }
    class TaskScheduler {
        <<interface>>
        +schedule(tasks: List[Task], weeks: List[Week])
    }
    class ExcelService {
        +read_data(filepath: str)
        +create_calendar(filepath: str, planning: Planning)
        +create_planning(filepath: str, planning: Planning)
        +export_pdf(excel_file: str, pdf_file: str)
    }

    Task "1" o-- "*" SubTask : composed of
    TaskOccurrence "*" --> "1" Task : refers to
    Week "1" o-- "*" TaskOccurrence : contains
    Planning "1" o-- "*" Task : manages
    Planning "1" o-- "*" Week : manages

    Planning ..> TaskSorter : uses
    Planning ..> TaskScheduler : delegates placement to
    Planning ..> ExcelService : uses for I/O
    ExcelService ..> SubTask : creates
    ExcelService ..> Planning : reads/writes/exports
```

## ⚙️ Design Patterns & Extensibility

- **Strategy Pattern:** The `Planning.plan(scheduler)` method accepts any object implementing the `TaskScheduler` interface. This allows seamless swapping between the current `GreedyScheduler` and future implementations (like a `LocalSearchScheduler`).
- **Single Responsibility Principle (SRP):** `ExcelService` is solely responsible for `pandas`/`openpyxl` interactions. The algorithmic core remains completely agnostic of the data source format.

## 🚀 Getting Started

*(Instructions to be completed once the core is pushed)*

```bash
git clone https://github.com/your-username/maintenance-scheduler.git
cd maintenance-scheduler
pip install -r requirements.txt
python main.py --input data/maintenance_data.xlsx
```

## 🗺️ Roadmap / Future Work

- [ ] **Baseline Implementation:** Finalize the `GreedyScheduler` and `TaskSorter` logic.
- [ ] **Fitness Evaluation:** Implement a variance-based load calculation to quantify the "quality" of a generated schedule.
- [ ] **Meta-heuristics:** Add a Local Search phase post-greedy placement to escape local optima and further flatten the workload curve.
