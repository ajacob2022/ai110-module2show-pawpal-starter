from datetime import date, timedelta

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


def make_scheduler():
    mochi = Pet("Mochi", "dog", [Task("Walk", 20, "09:00"), Task("Meds", 5, "07:00")])
    luna = Pet("Luna", "cat", [Task("Feed", 10, "09:00")])
    return Scheduler(Owner("Jordan", 100, [mochi, luna])), mochi


def test_sort_by_time():
    scheduler, _ = make_scheduler()
    times = [t.time for _, t in scheduler.sort_by_time(scheduler.owner.get_all_tasks())]
    assert times == ["07:00", "09:00", "09:00"]


def test_filter_by_pet_and_status():
    scheduler, mochi = make_scheduler()
    mochi.tasks[0].mark_complete()
    assert len(scheduler.filter_tasks(pet_name="Mochi")) == 2
    assert [t.description for _, t in scheduler.filter_tasks(completed=True)] == ["Walk"]


def test_daily_task_recurs_tomorrow():
    scheduler, mochi = make_scheduler()
    scheduler.mark_task_complete(mochi, mochi.tasks[0])
    assert mochi.tasks[-1].due_date == date.today() + timedelta(days=1)
    assert not mochi.tasks[-1].completed


def test_one_time_task_does_not_recur():
    pet = Pet("Mochi", "dog", [Task("Vet", 30, frequency="once")])
    scheduler = Scheduler(Owner("Jordan", 100, [pet]))
    scheduler.mark_task_complete(pet, pet.tasks[0])
    assert len(pet.tasks) == 1


def test_conflict_detected():
    scheduler, _ = make_scheduler()
    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1
    assert "09:00" in warnings[0]


def test_no_conflict():
    scheduler = Scheduler(Owner("Jordan", 100, [Pet("Mochi", "dog", [Task("Walk", 20, "09:00")])]))
    assert scheduler.detect_conflicts() == []


def test_pet_with_no_tasks():
    scheduler = Scheduler(Owner("Jordan", 60, [Pet("Mochi", "dog")]))
    assert scheduler.build_plan() == []
    assert scheduler.detect_conflicts() == []
    assert scheduler.sort_by_time(scheduler.owner.get_all_tasks()) == []


def test_weekly_task_recurs_in_seven_days():
    pet = Pet("Mochi", "dog", [Task("Groom", 30, frequency="weekly")])
    Scheduler(Owner("Jordan", 60, [pet])).mark_task_complete(pet, pet.tasks[0])
    assert pet.tasks[-1].due_date == date.today() + timedelta(days=7)


def test_future_task_not_in_todays_plan():
    pet = Pet("Mochi", "dog", [Task("Walk", 20, due_date=date.today() + timedelta(days=1))])
    assert Scheduler(Owner("Jordan", 60, [pet])).build_plan() == []


def test_completed_task_not_flagged_as_conflict():
    scheduler, mochi = make_scheduler()
    mochi.tasks[0].mark_complete()
    assert scheduler.detect_conflicts() == []


def test_same_time_on_different_days_is_not_a_conflict():
    tomorrow = date.today() + timedelta(days=1)
    pet = Pet("Mochi", "dog", [Task("Walk", 20, "09:00"), Task("Feed", 5, "09:00", due_date=tomorrow)])
    assert Scheduler(Owner("Jordan", 60, [pet])).detect_conflicts() == []
