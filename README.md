![Type: Personal](https://img.shields.io/badge/type-personal-blue)
![Language: Python](https://img.shields.io/badge/language-Python-success)
![Topic: Scheduling](https://img.shields.io/badge/topic-scheduling-purple)

# Preventive Maintenance Scheduler

Personal project focused on preventive maintenance task planning over an annual calendar.

## Project Overview

This project aims to build a scheduling system for preventive maintenance tasks distributed over multiple weeks.  
The goal is to generate a feasible and balanced annual planning while taking into account task frequencies, durations, and workload distribution.

This project is inspired by a real industrial scheduling problem where the placement of one task impacts the placement of many others.  
Because of these strong interdependencies, the problem is difficult to model exactly in a simple mathematical way, so I chose to implement a **Greedy Algorithm** to construct a practical solution.

## Objectives

- Model preventive maintenance tasks and their subtasks.
- Generate task occurrences according to maintenance frequency.
- Distribute tasks over the weeks of the year.
- Balance weekly workload as much as possible.
- Export the resulting planning to Excel / PDF.

## Features

- Task and subtask modeling
- Weekly planning management
- Greedy-based task placement
- Workload calculation by week
- Excel import/export support
- Extensible architecture for future optimization strategies

## Project Structure

The project follows an object-oriented design:

- `Task` / `SubTask`: maintenance task definitions
- `TaskOccurrence`: scheduled occurrence of a task
- `Week`: stores assigned occurrences and weekly load
- `Planning`: global planning object
- `TaskSorter`: sorts tasks before scheduling
- `TaskScheduler`: assigns tasks to weeks using a greedy approach
- `ExcelService`: handles file import/export

## Why Greedy?

In this scheduling problem, assigning one task to a given week can strongly affect the placement of many other tasks.  
This makes exact mathematical modeling difficult in practice, especially when business rules and placement dependencies become highly specific.

A greedy approach provides:
- a simple implementation,
- fast execution,
- feasible schedules,
- a strong baseline for future optimization.

## Possible Improvements

- Add evaluation metrics for workload balance
- Compare multiple greedy heuristics
- Add local search to improve an initial solution
- Visualize the final schedule with charts or Gantt views
- Benchmark different scheduling strategies

## Tech Stack

- Python
- pandas / openpyxl
- Mermaid for UML diagrams
- Excel / PDF export

## Status

Work in progress — the project is currently being cleaned up and documented.

## Author

Personal project developed to explore scheduling, heuristics, and optimization-oriented software design.
