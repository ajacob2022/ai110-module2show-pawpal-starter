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

tasks = owner.get_all_tasks()
if tasks:
    st.table(
        [
            {
                "pet": p.name,
                "description": t.description,
                "time": t.time,
                "duration_minutes": t.duration_minutes,
                "frequency": t.frequency,
                "priority": t.priority,
            }
            for p, t in tasks
        ]
    )

for warning in Scheduler(owner).detect_conflicts():
    st.warning(warning)

st.divider()
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    st.text(Scheduler(owner).explain_plan())
