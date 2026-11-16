import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", 90)
owner = st.session_state.owner

owner.name = st.text_input("Owner name", value=owner.name)
owner.available_minutes = int(
    st.number_input("Minutes available today", min_value=1, max_value=1440, value=owner.available_minutes)
)

st.subheader("Add a pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(pet_name, species))

if owner.pets:
    st.table([{"name": p.name, "species": p.species, "tasks": len(p.tasks)} for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.subheader("Add a task")
if owner.pets:
    target = st.selectbox("Pet", [p.name for p in owner.pets])
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        description = st.text_input("Task description", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
    with col5:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

    if st.button("Add task"):
        pet = next(p for p in owner.pets if p.name == target)
        pet.add_task(Task(description, int(duration), task_time, frequency, priority))
        st.rerun()
else:
    st.info("Add a pet before adding tasks.")

scheduler = Scheduler(owner)

st.subheader("Tasks")
col1, col2 = st.columns(2)
with col1:
    pet_filter = st.selectbox("Show pet", ["All"] + [p.name for p in owner.pets])
with col2:
    status_filter = st.selectbox("Show status", ["All", "Pending", "Completed"])

shown = scheduler.filter_tasks(
    pet_name=None if pet_filter == "All" else pet_filter,
    completed={"All": None, "Pending": False, "Completed": True}[status_filter],
)
shown = scheduler.sort_by_time(shown)

if shown:
    st.table(
        [
            {
                "pet": p.name,
                "description": t.description,
                "time": t.time,
                "due": str(t.due_date),
                "duration_minutes": t.duration_minutes,
                "frequency": t.frequency,
                "priority": t.priority,
                "done": t.completed,
            }
            for p, t in shown
        ]
    )
else:
    st.info("No tasks match.")

pending = scheduler.filter_tasks(completed=False)
if pending:
    labels = [f"{t.time} {t.description} ({p.name})" for p, t in pending]
    choice = st.selectbox("Mark a task complete", labels)
    if st.button("Complete task"):
        pet, task = pending[labels.index(choice)]
        scheduler.mark_task_complete(pet, task)
        st.rerun()

conflicts = scheduler.detect_conflicts()
for warning in conflicts:
    st.warning(warning + ". Move one of them to a different time.")

st.divider()
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    if conflicts:
        st.warning("Some tasks share a start time; resolve the conflicts above for a cleaner day.")
    else:
        st.success("No conflicts found.")
    st.text(scheduler.explain_plan())
