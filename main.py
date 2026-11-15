from pawpal_system import Owner, Pet, Scheduler, Task

owner = Owner("Jordan", 90)

mochi = Pet("Mochi", "dog")
mochi.add_task(Task("Grooming", 40, "16:00", "weekly", "low"))
mochi.add_task(Task("Morning walk", 30, "07:30", "daily", "high"))

luna = Pet("Luna", "cat")
luna.add_task(Task("Play time", 20, "18:00", "daily", "medium"))
luna.add_task(Task("Feeding", 10, "07:30", "daily", "high"))

owner.add_pet(mochi)
owner.add_pet(luna)

scheduler = Scheduler(owner)

print("Today's Schedule")
print("================")
print(scheduler.explain_plan())

print()
print("All tasks sorted by time")
for pet, task in scheduler.sort_by_time(owner.get_all_tasks()):
    print(f"{task.time} {task.description} ({pet.name})")

print()
print("Luna's tasks")
for pet, task in scheduler.filter_tasks(pet_name="Luna"):
    print(f"{task.description}")

print()
print("Conflicts")
for warning in scheduler.detect_conflicts():
    print(warning)

scheduler.mark_task_complete(mochi, mochi.tasks[1])
print()
print("Completed tasks")
for pet, task in scheduler.filter_tasks(completed=True):
    print(f"{task.description} ({pet.name})")
print()
print("Mochi's tasks after completing the walk")
for pet, task in scheduler.filter_tasks(pet_name="Mochi"):
    print(f"{task.description} due {task.due_date} done={task.completed}")
