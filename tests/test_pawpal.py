from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status():
    task = Task("Walk", 20)
    assert not task.completed
    task.mark_complete()
    assert task.completed


def test_adding_task_increases_count():
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Walk", 20))
    assert len(pet.tasks) == 1


def test_remove_task():
    pet = Pet("Mochi", "dog", [Task("Walk", 20)])
    pet.remove_task("Walk")
    assert pet.tasks == []


def test_plan_prefers_priority_and_orders_by_time():
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Groom", 20, "09:00", priority="low"))
    pet.add_task(Task("Meds", 5, "10:00", priority="high"))
    pet.add_task(Task("Play", 10, "08:00", priority="medium"))
    owner = Owner("Jordan", 100, [pet])
    assert [t.description for _, t in Scheduler(owner).build_plan()] == ["Play", "Groom", "Meds"]


def test_time_limit_skips_tasks():
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Walk", 25, priority="high"))
    pet.add_task(Task("Groom", 20, priority="low"))
    owner = Owner("Jordan", 30, [pet])
    assert [t.description for _, t in Scheduler(owner).build_plan()] == ["Walk"]


def test_completed_tasks_excluded():
    done = Task("Walk", 20, priority="high")
    done.mark_complete()
    owner = Owner("Jordan", 60, [Pet("Mochi", "dog", [done])])
    assert Scheduler(owner).build_plan() == []


def test_empty_plan_explanation():
    assert Scheduler(Owner("Jordan", 60)).explain_plan() == "No tasks fit in the available time."
