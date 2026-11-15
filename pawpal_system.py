from dataclasses import dataclass, field

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    description: str
    duration_minutes: int
    time: str = "08:00"
    frequency: str = "daily"
    priority: str = "medium"
    completed: bool = False

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

    def build_plan(self) -> list[tuple[Pet, Task]]:
        """Pick pending tasks by priority within the time budget, ordered by time."""
        pending = [(p, t) for p, t in self.owner.get_all_tasks() if not t.completed]
        pending.sort(key=lambda pt: (PRIORITY_ORDER[pt[1].priority], pt[1].duration_minutes))
        chosen = []
        remaining = self.owner.available_minutes
        for pet, task in pending:
            if task.duration_minutes <= remaining:
                chosen.append((pet, task))
                remaining -= task.duration_minutes
        return sorted(chosen, key=lambda pt: pt[1].time)

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
            for p, t in self.owner.get_all_tasks()
            if not t.completed and (p, t) not in plan
        ]
        if skipped:
            lines.append("Skipped (not enough time): " + ", ".join(skipped))
        return "\n".join(lines)
