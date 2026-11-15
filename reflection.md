# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The design has four classes. Owner holds the owner's name, daily available time, and their pets. Pet holds the pet's name, species, and its care tasks. Task holds a description, time, frequency, duration, priority, and completion status. Scheduler takes an Owner and builds a daily plan from their tasks, then explains why it chose that plan.

Three core actions a user should be able to perform:

- Add an owner and a pet.
- Add care tasks (walks, feeding, meds) to a pet with a duration and priority.
- Generate and view today's schedule along with an explanation of it.

**b. Design changes**

The design stayed close to the UML. The main addition was a module-level priority ordering used by Scheduler to sort tasks, which kept the Task class simple.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers the owner's available minutes and each task's priority and duration. Time is a hard limit, and priority decides which tasks get that time first.

**b. Tradeoffs**

It picks tasks greedily by priority and skips any task that does not fit, instead of searching for the best combination. Conflict detection only flags tasks that share the exact same start time and does not check whether durations overlap. Both choices keep the code simple and predictable, which suits a daily pet-care plan.

---

## 3. AI Collaboration

**a. How you used AI**

I used an AI assistant to draft the UML, generate the class skeleton, and implement the scheduler and tests. Prompts that named the exact classes and constraints worked best. I also used AI to corrrect an error that was preventing the app from running.

**b. Judgment and verification**

I kept the scheduler to a simple greedy approach rather than a more complex optimization. I verified the behavior by running the tests and the Streamlit app.

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion, adding and removing tasks, priority ordering, the time limit, excluding completed tasks, and the empty-plan message. These cover the core scheduling rules.

**b. Confidence**

I am confident in the core behavior. Next I would test invalid priorities, zero available time, and duplicate task descriptions.

---

## 5. Reflection

**a. What went well**

The clean separation between the logic layer and the Streamlit UI.

**b. What you would improve**

I would add recurring tasks, preferred times, and per-pet plans.

**c. Key takeaway**

Designing the classes first made the implementation and tests straightforward.
