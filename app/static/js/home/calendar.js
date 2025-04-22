
const calendar = document.querySelector(".calendar"),
  date = document.querySelector(".date"),
  daysContainer = document.querySelector(".days"),
  prev = document.querySelector(".prev"),
  next = document.querySelector(".next"),
  todayBtn = document.querySelector(".today-btn"),
  gotoBtn = document.querySelector(".goto-btn"),
  dateInput = document.querySelector(".date-input"),
  eventDay = document.querySelector(".event-day"),
  eventDate = document.querySelector(".event-date"),
  eventsContainer = document.querySelector(".events"),
  addEventBtn = document.querySelector(".add-event"),
  addEventWrapper = document.querySelector(".add-event-wrapper"),
  addEventCloseBtn = document.querySelector(".close");

let today = new Date();
let activeDay;
let month = today.getMonth();
let year = today.getFullYear();

const months = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];

function initCalendar() {
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const prevLastDay = new Date(year, month, 0);
  const prevDays = prevLastDay.getDate();
  const lastDate = lastDay.getDate();
  const day = firstDay.getDay();
  const nextDays = 7 - lastDay.getDay() - 1;

  date.innerHTML = months[month] + " " + year;

  let days = "";

  for (let x = day; x > 0; x--) {
    days += `<div class="day prev-date">${prevDays - x + 1}</div>`;
  }

  for (let i = 1; i <= lastDate; i++) {
    const isToday =
      i === new Date().getDate() &&
      year === new Date().getFullYear() &&
      month === new Date().getMonth();

    if (isToday) {
      activeDay = i;
      getActiveDay(i);
    }

    days += `<div class="day ${isToday ? "today active" : ""}">${i}</div>`;
  }

  for (let j = 1; j <= nextDays; j++) {
    days += `<div class="day next-date">${j}</div>`;
  }

  daysContainer.innerHTML = days;
  addListner();
}

function addListner() {
  const days = document.querySelectorAll(".day");
  days.forEach((day) => {
    day.addEventListener("click", (e) => {
      const clickedDay = Number(e.target.innerHTML);
      getActiveDay(clickedDay);
      activeDay = clickedDay;

      days.forEach((d) => d.classList.remove("active"));

      if (e.target.classList.contains("prev-date")) {
        prevMonth();
        setTimeout(() => {
          document
            .querySelectorAll(".day")
            .forEach((d) => d.innerHTML === e.target.innerHTML && d.classList.add("active"));
        }, 100);
      } else if (e.target.classList.contains("next-date")) {
        nextMonth();
        setTimeout(() => {
          document
            .querySelectorAll(".day")
            .forEach((d) => d.innerHTML === e.target.innerHTML && d.classList.add("active"));
        }, 100);
      } else {
        e.target.classList.add("active");
      }
    });
  });
}

function getActiveDay(day) {
  const dateObj = new Date(year, month, day);
  const dayName = dateObj.toString().split(" ")[0];
  const formattedDate = `${day} ${months[month]} ${year}`;
  const serverDate = formatDateForServer(formattedDate);

  eventDay.innerHTML = dayName;
  eventDate.innerHTML = formattedDate;

  eventsContainer.innerHTML = "";

  if (window.calendarMode === "meals") {
    fetch(`/meals/daily_meals?target_date=${serverDate}`)
      .then(res => res.json())
      .then(data => {
        if (typeof updateMealsFromServer === "function") {
          updateMealsFromServer(serverDate, data.meals || {});
        }
      })
      .catch(err => {
        console.error("Ошибка загрузки приёмов пищи:", err);
        eventsContainer.innerHTML = "<div class='error'>Ошибка загрузки приёмов пищи</div>";
      });

    fetch(`/meals/daily_nutrition?target_date=${serverDate}`)
      .then(res => res.json())
      .then(nutrition => {
        document.getElementById("calories").textContent = nutrition.total_calories || 0;
        document.getElementById("proteins").textContent = nutrition.total_proteins || 0;
        document.getElementById("fats").textContent = nutrition.total_fats || 0;
        document.getElementById("carbs").textContent = nutrition.total_carbs || 0;
      })
      .catch(err => {
        console.error("Ошибка загрузки nutrition:", err);
        document.getElementById("calories").textContent = "-";
        document.getElementById("proteins").textContent = "-";
        document.getElementById("fats").textContent = "-";
        document.getElementById("carbs").textContent = "-";
      });
  } else if (window.calendarMode === "workouts") {
    fetch(`/workouts/daily_workouts?target_date=${serverDate}`)
      .then(res => res.json())
      .then(data => {
        if (typeof updateWorkoutsFromServer === "function") {
          updateWorkoutsFromServer(serverDate, data.workouts || []);
        }
      })
      .catch(err => {
        console.error("Ошибка загрузки тренировок:", err);
        eventsContainer.innerHTML = "<div class='error'>Ошибка загрузки тренировок</div>";
      });

    fetch(`/workouts/daily_summary?target_date=${serverDate}`)
      .then(res => res.json())
      .then(summary => {
        const duration = document.getElementById("totalDuration");
        const calories = document.getElementById("totalWorkoutCalories");
        if (duration) duration.textContent = summary.total_duration || 0;
        if (calories) calories.textContent = summary.total_calories_burned || 0;
      })
      .catch(err => {
        console.error("Ошибка загрузки сводки:", err);
        const duration = document.getElementById("totalDuration");
        const calories = document.getElementById("totalWorkoutCalories");
        if (duration) duration.textContent = "-";
        if (calories) calories.textContent = "-";
      });

    document.getElementById("calories").textContent = "-";
    document.getElementById("proteins").textContent = "-";
    document.getElementById("fats").textContent = "-";
    document.getElementById("carbs").textContent = "-";
  }
}

function formatDateForServer(str) {
  const [day, monthName, year] = str.trim().split(" ");
  const month = (months.indexOf(monthName) + 1).toString().padStart(2, "0");
  return `${year}-${month}-${day.padStart(2, "0")}`;
}

function prevMonth() {
  month--;
  if (month < 0) {
    month = 11;
    year--;
  }
  initCalendar();
}

function nextMonth() {
  month++;
  if (month > 11) {
    month = 0;
    year++;
  }
  initCalendar();
}

prev.addEventListener("click", prevMonth);
next.addEventListener("click", nextMonth);

todayBtn.addEventListener("click", () => {
  today = new Date();
  month = today.getMonth();
  year = today.getFullYear();
  initCalendar();
});

gotoBtn.addEventListener("click", () => {
  const dateArr = dateInput.value.split("/");
  if (
    dateArr.length === 2 &&
    dateArr[0] > 0 &&
    dateArr[0] < 13 &&
    dateArr[1].length === 4
  ) {
    month = dateArr[0] - 1;
    year = parseInt(dateArr[1]);
    initCalendar();
  } else {
    alert("Invalid Date");
  }
});

dateInput.addEventListener("input", (e) => {
  dateInput.value = dateInput.value.replace(/[^0-9/]/g, "");
  if (dateInput.value.length === 2) {
    dateInput.value += "/";
  }
  if (dateInput.value.length > 7) {
    dateInput.value = dateInput.value.slice(0, 7);
  }
});

addEventCloseBtn.addEventListener("click", () => {
  addEventWrapper.classList.remove("active");
});

initCalendar();
