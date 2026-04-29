from src.models import Planning
from src.scheduler import GreedyScheduler
from src.evaluators import WorkloadVarianceEvaluator
from src.io_services import ExcelService


DATA_PATH = "data/maintenance_data.xlsx"


def print_fitness_report(report: dict) -> None:
    print("\n" + "=" * 45)
    print("        📊 Schedule Fitness Report")
    print("=" * 45)
    print(f"  Total hours scheduled  : {report['total_hours']}h")
    print(f"  Mean weekly load       : {report['mean_weekly_load']}h")
    print(f"  Standard deviation     : {report['std_deviation']}h")
    print(f"  Max load (worst week)  : {report['max_week_load']}h")
    print(f"  Min load (best week)   : {report['min_week_load']}h")
    print("=" * 45 + "\n")


def print_weekly_summary(planning: Planning) -> None:
    print("📅 Weekly Workload Distribution")
    print("-" * 45)
    for week in planning.weeks:
        load = week.total_load()
        bar = "█" * int(load)  # Petite visualisation ASCII
        print(f"  Week {week.week_number:02d} | {load:5.1f}h | {bar}")
    print("-" * 45 + "\n")


def main():
    # 1. Load data from Excel and build domain objects
    print()
    tasks = ExcelService.read_data(DATA_PATH)
    print()

    # 2. Instantiate the Planning and run the Greedy Scheduler
    print()
    planning = Planning(tasks)
    planning.plan(GreedyScheduler())
    print()

    # 3. Evaluate the fitness of the generated schedule
    report = WorkloadVarianceEvaluator.evaluate(planning)

    # 4. Display results
    print_fitness_report(report)
    print_weekly_summary(planning)


if __name__ == "__main__":
    main()