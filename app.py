import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

owner_name = st.text_input("Owner name", value="Jordan")
available = st.number_input("Minutes available today", min_value=1, max_value=1440, value=90)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.subheader("Tasks")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    task_title = st.text_input("Task description", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    task_time = st.text_input("Time (HH:MM)", value="08:00")
with col5:
    frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

if st.button("Add task"):
    st.session_state.tasks.append(Task(task_title, int(duration), task_time, frequency, priority))

if st.session_state.tasks:
    st.table(
        [
            {
                "description": t.description,
                "time": t.time,
                "duration_minutes": t.duration_minutes,
                "frequency": t.frequency,
                "priority": t.priority,
            }
            for t in st.session_state.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()
st.subheader("Schedule")

if st.button("Generate schedule"):
    pet = Pet(pet_name, species, list(st.session_state.tasks))
    owner = Owner(owner_name, int(available), [pet])
    st.text(f"Daily plan for {pet.name} ({pet.species}):")
    st.text(Scheduler(owner).explain_plan())
