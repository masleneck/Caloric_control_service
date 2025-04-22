import { setupLogout } from './logout.js';

document.addEventListener("DOMContentLoaded", () => {
  setupLogout();

  const mealToggle = document.getElementById("show-meals");
  const workoutToggle = document.getElementById("show-workouts");
  const calendar = document.querySelector(".calendar");
  const nutritionInfo = document.querySelector(".nutrition-info");
  const mealForm = document.querySelector(".add-event-body");
  const workoutForm = document.querySelector(".add-workout-body");
  const events = document.querySelector(".events");
  const container = document.querySelector(".container");
  const rightPanel = document.querySelector(".right");
  const addEventWrapper = document.querySelector(".add-event-wrapper");
  const addBtn = document.querySelector(".add-event");
  const closeBtn = document.querySelector(".close");

  mealForm.style.display = "none";
  workoutForm.style.display = "none";

  addBtn.addEventListener("click", () => {
    if (window.calendarMode === "meals") {
      mealForm.style.display = "flex";
      workoutForm.style.display = "none";
    } else {
      mealForm.style.display = "none";
      workoutForm.style.display = "flex";
    }
    addEventWrapper.classList.add("active");
  });

  closeBtn.addEventListener("click", () => {
    addEventWrapper.classList.remove("active");
    mealForm.style.display = "none";
    workoutForm.style.display = "none";
    if (typeof resetForm === "function") resetForm();
    if (typeof resetWorkoutForm === "function") resetWorkoutForm();
  });

  window.calendarMode = "meals";

  mealToggle.addEventListener("click", () => {
    window.calendarMode = "meals";

    mealToggle.classList.add("active");
    workoutToggle.classList.remove("active");

    calendar.classList.remove("workout-mode");
    calendar.classList.add("meal-mode");

    container.classList.remove("workout-mode");
    container.classList.add("meal-mode");

    rightPanel.classList.remove("workout-mode");
    rightPanel.classList.add("meal-mode");

    nutritionInfo.style.display = "flex";
    document.querySelector(".workout-summary").style.display = "none";
    events.setAttribute("data-mode", "meals");

    addEventWrapper.classList.remove("active");
    mealForm.style.display = "none";
    workoutForm.style.display = "none";

    const eventDate = document.querySelector(".event-date").textContent;
    if (typeof updateMealsFromServer === "function" && eventDate) {
      const serverDate = formatDateForServer(eventDate);
      fetch(`/meals/daily_meals?target_date=${serverDate}`)
        .then(res => res.json())
        .then(data => {
          if (data.meals) {
            updateMealsFromServer(serverDate, data.meals);
          }
        });
    }
  });

  workoutToggle.addEventListener("click", () => {
    window.calendarMode = "workouts";
  
    workoutToggle.classList.add("active");
    mealToggle.classList.remove("active");
  
    calendar.classList.remove("meal-mode");
    calendar.classList.add("workout-mode");
  
    container.classList.remove("meal-mode");
    container.classList.add("workout-mode");
  
    rightPanel.classList.remove("meal-mode");
    rightPanel.classList.add("workout-mode");
  
    nutritionInfo.style.display = "none";
    events.setAttribute("data-mode", "workouts");
  
    addEventWrapper.classList.remove("active");
    mealForm.style.display = "none";
    workoutForm.style.display = "none";
  
    document.querySelector(".workout-summary").style.display = "flex";
  
    const eventDate = document.querySelector(".event-date").textContent;
    if (typeof updateWorkoutsFromServer === "function" && eventDate) {
      const serverDate = formatDateForServer(eventDate);
  
      const duration = document.getElementById("totalDuration");
      const calories = document.getElementById("totalWorkoutCalories");
      if (duration) duration.textContent = "–";
      if (calories) calories.textContent = "–";
  
      fetch(`/workouts/daily_workouts?target_date=${serverDate}`)
        .then(res => res.json())
        .then(data => {
          if (data.workouts && data.workouts.length > 0) {
            updateWorkoutsFromServer(serverDate, data.workouts);
          } else {
            events.innerHTML = `<div class="no-event">Нет тренировок</div>`;
            window.workoutsByDate[serverDate] = [];
  
            document.getElementById("totalDuration").textContent = "–";
            document.getElementById("totalWorkoutCalories").textContent = "–";
          }
        });
    }
  });  
});

function formatDateForServer(str) {
  const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  const [day, monthName, year] = str.trim().split(" ");
  const month = (months.indexOf(monthName) + 1).toString().padStart(2, "0");
  return `${year}-${month}-${day.padStart(2, "0")}`;
}