from pawpal_system import Owner, Pet, Scheduler, Task

owner = Owner("Jordan", 90)

mochi = Pet("Mochi", "dog")
mochi.add_task(Task("Morning walk", 30, "07:30", "daily", "high"))
mochi.add_task(Task("Grooming", 40, "16:00", "weekly", "low"))

luna = Pet("Luna", "cat")
luna.add_task(Task("Feeding", 10, "08:00", "daily", "high"))
luna.add_task(Task("Play time", 20, "18:00", "daily", "medium"))

owner.add_pet(mochi)
owner.add_pet(luna)

print("Today's Schedule")
print("================")
print(Scheduler(owner).explain_plan())
