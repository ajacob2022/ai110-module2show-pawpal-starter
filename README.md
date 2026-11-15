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
07:30 - Morning walk for Mochi (30 min, daily) [priority: high]
08:00 - Feeding for Luna (10 min, daily) [priority: high]
18:00 - Play time for Luna (20 min, daily) [priority: medium]
Used 60 of 90 minutes, highest priority first.
Skipped (not enough time): Grooming
```

## Testing PawPal+

```bash
pytest
```

```
7 passed
```

## Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.build_plan` | Chosen by priority (high first), then shorter duration; the final plan is ordered by task time |
| Filtering | `Scheduler.build_plan` | Skips completed tasks and tasks that no longer fit the time available |
| Conflict handling | `Scheduler.build_plan` | Tasks that exceed the owner's available minutes are skipped and reported |
| Recurring tasks | `Task.frequency` | Stored and displayed; no automatic rescheduling |

## Demo Walkthrough

1. Run `python main.py` for the terminal demo, or `streamlit run app.py` for the UI.
2. Enter the owner name, minutes available, pet name and species.
3. Add tasks with a title, duration and priority.
4. Click "Generate schedule" to see the ordered plan with start times.
5. Tasks that do not fit are listed as skipped.
