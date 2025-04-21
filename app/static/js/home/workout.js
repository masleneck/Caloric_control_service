const eventsContainer = document.querySelector(".events");

if (!window.workoutsByDate) window.workoutsByDate = {};

const workoutNameInput = document.getElementById("workoutName");
const workoutDurationInput = document.getElementById("workoutDuration");
const workoutCaloriesInput = document.getElementById("workoutCalories");
const workoutSuggestions = document.getElementById("workoutSuggestions");
const saveWorkoutBtn = document.querySelector(".add-event-btn");
const addEventWrapper = document.querySelector(".add-event-wrapper");

let editWorkoutMode = false;
let editWorkoutTarget = null;

const months = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

function formatDate(dateStr) {
  if (/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) return dateStr;
  const [day, monthName, year] = dateStr.split(" ");
  const monthIndex = months.indexOf(monthName);
  return `${year}-${String(monthIndex + 1).padStart(2, '0')}-${day.padStart(2, '0')}`;
}

function formatDateForServer(str) {
  if (/^\d{4}-\d{2}-\d{2}$/.test(str)) {
    return str;
  }
  const [day, monthName, year] = str.trim().split(" ");
  const monthIndex = months.indexOf(monthName);
  return `${year}-${String(monthIndex + 1).padStart(2, "0")}-${day.padStart(2, "0")}`;
}


function updateWorkoutsFromServer(dateStr, workouts) {
  const parsedWorkouts = workouts.map(w => ({
    name: w.name,
    duration: w.duration,
    calories: w.calories,
    description: w.description || "",
    date: dateStr
  }));

  window.workoutsByDate[dateStr] = parsedWorkouts;
  renderWorkoutsForDate(dateStr);
  refreshWorkoutSummary(dateStr);
}

window.updateWorkoutsFromServer = updateWorkoutsFromServer;

function renderWorkoutsForDate(dateStr) {
  if (window.calendarMode !== "workouts") return;
  eventsContainer.innerHTML = "";
  const workouts = window.workoutsByDate[dateStr] || [];

  workouts.forEach(workout => {
    const div = document.createElement("div");
    div.className = "event";
    div.innerHTML = `
      <div class="title">
        <i class="fas fa-dumbbell"></i>
        <h3>${workout.name}</h3>
      </div>
      <div class="products">
        Длительность: ${workout.duration} мин<br>
        Калории: ${workout.calories} ккал
      </div>
      <div class="actions">
        <button class="edit" data-name="${workout.name}">
          <i class="ri-edit-line"></i>
        </button>
        <button class="delete" data-name="${workout.name}">
          <i class="ri-delete-bin-line"></i>
        </button>
      </div>
    `;

    div.querySelector(".delete").addEventListener("click", () => {
      deleteWorkout(workout.name, dateStr);
    });

    div.querySelector(".edit").addEventListener("click", () => {
      startEditWorkout(workout.name, dateStr);
    });

    eventsContainer.appendChild(div);
  });
}

function startEditWorkout(name, dateStr) {
  const workout = window.workoutsByDate[dateStr].find(w => w.name === name);
  if (!workout) return;

  workoutNameInput.value = workout.name;
  workoutDurationInput.value = workout.duration;
  workoutCaloriesInput.value = workout.calories;

  // Показываем только блок тренировки
  document.querySelector(".add-event-body").style.display = "none";
  document.querySelector(".add-workout-body").style.display = "flex";

  addEventWrapper.classList.add("active");
  editWorkoutMode = true;
  editWorkoutTarget = { name, dateStr };
}

async function deleteWorkout(name, dateStr) {
  if (!confirm("Удалить эту тренировку?")) return;

  const formattedDate = formatDate(dateStr);
  const query = `?workout_date=${encodeURIComponent(formattedDate)}&workout_name=${encodeURIComponent(name)}`;

  try {
    const res = await fetch(`/workouts/delete_workout${query}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" }
    });

    if (res.ok) {
      const list = window.workoutsByDate[dateStr] || [];
      window.workoutsByDate[dateStr] = list.filter(w => w.name !== name);
      if (window.workoutsByDate[dateStr].length === 0) {
        delete window.workoutsByDate[dateStr];
      }
      renderWorkoutsForDate(dateStr);
      refreshWorkoutSummary(dateStr);
    } else {
      const error = await res.json();
      console.error("Ошибка удаления:", error);
    }
  } catch (err) {
    console.error("Ошибка удаления:", err);
  }
}

saveWorkoutBtn.addEventListener("click", async () => {
  if (window.calendarMode !== "workouts") return;

  const name = workoutNameInput.value.trim();
  const duration = parseInt(workoutDurationInput.value.trim(), 10);
  const calories = parseInt(workoutCaloriesInput.value.trim(), 10);
  const rawDate = document.querySelector(".event-date").textContent;
  const formattedDate = formatDate(rawDate);

  if (!name || isNaN(duration) || isNaN(calories)) {
    alert("Заполните все поля корректно.");
    return;
  }

  try {
    const res = await fetch("/workouts/upsert_workout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("authToken")}`
      },
      body: JSON.stringify({
        workout_date: formattedDate,
        workout_names: [name],
        workouts_duration_minutes: [duration],
        workouts_calories_burned: [calories]
      })
    });

    const data = await res.json();

    if (!res.ok) {
      console.error("Ошибка сохранения:", data);
      alert("Ошибка при сохранении тренировки.");
      return;
    }

    const updatedWorkout = { name, duration, calories, date: formattedDate };

    if (!window.workoutsByDate[formattedDate]) {
      window.workoutsByDate[formattedDate] = [];
    }

    if (editWorkoutMode && editWorkoutTarget) {
      const list = window.workoutsByDate[formattedDate];
      const index = list.findIndex(w => w.name === editWorkoutTarget.name);
      if (index !== -1) list[index] = updatedWorkout;
    } else {
      window.workoutsByDate[formattedDate].push(updatedWorkout);
    }

    renderWorkoutsForDate(formattedDate);
    refreshWorkoutSummary(formattedDate);

    workoutNameInput.value = "";
    workoutDurationInput.value = "";
    workoutCaloriesInput.value = "";
    workoutSuggestions.innerHTML = "";
    addEventWrapper.classList.remove("active");

    editWorkoutMode = false;
    editWorkoutTarget = null;

  } catch (err) {
    console.error("Ошибка:", err);
    alert("Произошла ошибка при сохранении.");
  }
});

workoutNameInput.addEventListener("input", debounce(async (e) => {
  const query = e.target.value.trim();
  if (query.length < 2) {
    workoutSuggestions.innerHTML = "";
    workoutSuggestions.style.display = "none";
    return;
  }

  try {
    const res = await fetch(`/workouts/search_item?query=${encodeURIComponent(query)}&limit=5`);
    const data = await res.json();

    workoutSuggestions.innerHTML = "";
    if (data.length > 0) {
      data.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item.name;
        li.classList.add("suggestion-item");
        li.addEventListener("click", () => {
          workoutNameInput.value = item.name;
          workoutSuggestions.style.display = "none";
          if (item.calories) workoutCaloriesInput.value = item.calories;
        });
        workoutSuggestions.appendChild(li);
      });
      workoutSuggestions.style.display = "block";
    } else {
      workoutSuggestions.style.display = "none";
    }
  } catch (err) {
    console.error("Ошибка поиска тренировок:", err);
    workoutSuggestions.style.display = "none";
  }
}, 300));

document.addEventListener("click", (e) => {
  if (e.target !== workoutNameInput) {
    workoutSuggestions.style.display = "none";
  }
});

function debounce(func, timeout = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => { func.apply(this, args); }, timeout);
  };
}

function refreshWorkoutSummary(dateStr) {
  const serverDate = formatDateForServer(dateStr);
  fetch(`/workouts/daily_summary?target_date=${serverDate}`)
    .then(res => res.json())
    .then(summary => {
      const infoBlock = document.querySelector(".workout-summary");
      if (!infoBlock) return;

      infoBlock.innerHTML = `
        <p>Длительность: <span id="totalDuration">${summary.total_duration || 0}</span> мин</p>
        <p>Потрачено калорий: <span id="totalWorkoutCalories">${summary.total_calories_burned || 0}</span> ккал</p>
      `;
    })
    .catch(err => {
      console.error("Ошибка загрузки сводки по тренировкам:", err);
    });
}

