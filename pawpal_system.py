from dataclasses import dataclass, field
from datetime import date, timedelta

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    description: str
    duration_minutes: int
    time: str = "08:00"
    frequency: str = "daily"
    priority: str = "medium"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, description: str) -> None:
        """Remove every task with the given description."""
        self.tasks = [t for t in self.tasks if t.description != description]


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every (pet, task) pair across all pets."""
        return [(pet, t) for pet in self.pets for t in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self, pairs: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Sort (pet, task) pairs by their HH:MM time, which orders correctly as text."""
        return sorted(pairs, key=lambda pt: pt[1].time)

    def filter_tasks(self, pet_name: str = None, completed: bool = None) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs matching an optional pet name and completion status."""
        return [
            (p, t)
            for p, t in self.owner.get_all_tasks()
            if (pet_name is None or p.name == pet_name)
            and (completed is None or t.completed == completed)
        ]

    def mark_task_complete(self, pet: Pet, task: Task) -> None:
        """Complete a task and add the next occurrence for daily or weekly tasks."""
        task.mark_complete()
        days = {"daily": 1, "weekly": 7}.get(task.frequency)
        if days:
            pet.add_task(
                Task(
                    task.description,
                    task.duration_minutes,
                    task.time,
                    task.frequency,
                    task.priority,
                    due_date=task.due_date + timedelta(days=days),
                )
            )

    def detect_conflicts(self) -> list[str]:
        """Return a warning for each group of pending tasks sharing a date and start time."""
        seen = {}
        for pet, task in self.filter_tasks(completed=False):
            seen.setdefault((task.due_date, task.time), []).append(f"{task.description} ({pet.name})")
        return [
            f"Warning: {', '.join(names)} are all scheduled at {time} on {day}"
            for (day, time), names in seen.items()
            if len(names) > 1
        ]

    def build_plan(self) -> list[tuple[Pet, Task]]:
        """Pick pending tasks due today by priority within the time budget, ordered by time."""
        pending = [
            (p, t) for p, t in self.filter_tasks(completed=False) if t.due_date <= date.today()
        ]
        pending.sort(key=lambda pt: (PRIORITY_ORDER[pt[1].priority], pt[1].duration_minutes))
        chosen = []
        remaining = self.owner.available_minutes
        for pet, task in pending:
            if task.duration_minutes <= remaining:
                chosen.append((pet, task))
                remaining -= task.duration_minutes
        return self.sort_by_time(chosen)

    def explain_plan(self) -> str:
        """Return a readable schedule and the reasoning behind it."""
        plan = self.build_plan()
        if not plan:
            return "No tasks fit in the available time."
        lines = [
            f"{t.time} - {t.description} for {p.name} "
            f"({t.duration_minutes} min, {t.frequency}) [priority: {t.priority}]"
            for p, t in plan
        ]
        used = sum(t.duration_minutes for _, t in plan)
        lines.append(f"Used {used} of {self.owner.available_minutes} minutes, highest priority first.")
        skipped = [
            t.description
            for p, t in self.filter_tasks(completed=False)
            if t.due_date <= date.today() and (p, t) not in plan
        ]
        if skipped:
            lines.append("Skipped (not enough time): " + ", ".join(skipped))
        return "\n".join(lines)
