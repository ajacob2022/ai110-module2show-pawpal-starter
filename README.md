# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Sample Output

Output of `python main.py`:

```
Today's Schedule
================
07:30 - Feeding for Luna (10 min, daily) [priority: high]
07:30 - Morning walk for Mochi (30 min, daily) [priority: high]
18:00 - Play time for Luna (20 min, daily) [priority: medium]
Used 60 of 90 minutes, highest priority first.
Skipped (not enough time): Grooming

All tasks sorted by time
07:30 Morning walk (Mochi)
07:30 Feeding (Luna)
16:00 Grooming (Mochi)
18:00 Play time (Luna)

Luna's tasks
Play time
Feeding

Conflicts
Warning: Morning walk (Mochi), Feeding (Luna) are all scheduled at 07:30 on 2026-11-15

Completed tasks
Morning walk (Mochi)

Mochi's tasks after completing the walk
Grooming due 2026-11-15 done=False
Morning walk due 2026-11-15 done=True
Morning walk due 2026-11-16 done=False
```

## Testing PawPal+

```bash
python -m pytest
```

The tests cover:

- Task completion and adding or removing tasks
- Sorting tasks chronologically by time
- Filtering by pet name and completion status
- Priority selection within the time budget, skipped tasks, and completed or future-dated tasks being left out
- Recurrence: daily tasks repeat the next day, weekly tasks in seven days, one-time tasks do not repeat
- Conflict detection for tasks at the same time, including no false warnings for completed tasks or different days
- Edge cases such as a pet with no tasks

```
============================= test session starts =============================
platform win32 -- Python 3.12.5, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\Adam\Desktop\project2_codepath\ai110-module2show-pawpal-starter
plugins: anyio-4.12.1
collected 18 items

tests\test_pawpal.py ..................                                  [100%]

============================= 18 passed in 0.09s ==============================
```

Confidence level: 4 out of 5 stars. The core scheduling rules are tested, but invalid input (such as a bad time format or priority) and overlapping durations are not.

## Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting | `Scheduler.sort_by_time` | Sorts (pet, task) pairs by their `HH:MM` time; zero-padded times sort correctly as text |
| Filtering | `Scheduler.filter_tasks` | Filters by pet name and/or completion status |
| Recurring tasks | `Scheduler.mark_task_complete` | Completing a daily or weekly task adds a copy due 1 or 7 days later using `timedelta`; one-time tasks do not repeat |
| Conflict detection | `Scheduler.detect_conflicts` | Returns a warning string for every group of pending tasks with the same date and start time, across any pets |
| Plan building | `Scheduler.build_plan` | Picks tasks due today by priority within the time budget, then orders them by time |

## Demo Walkthrough

1. Run `python main.py` for the terminal demo, or `streamlit run app.py` for the UI.
2. Enter the owner name, minutes available, pet name and species.
3. Add tasks with a title, duration and priority.
4. Click "Generate schedule" to see the ordered plan with start times.
5. Tasks that do not fit are listed as skipped.
