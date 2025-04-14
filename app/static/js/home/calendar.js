const calendarDays = document.getElementById("calendarDays");
const monthDisplay = document.getElementById("monthDisplay");

let nav = 0;
let selectedDate = null;

const weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];

function loadCalendar() {
  const dt = new Date();

  if (nav !== 0) {
    dt.setMonth(new Date().getMonth() + nav);
  }

  const month = dt.getMonth();
  const year = dt.getFullYear();

  const firstDayOfMonth = new Date(year, month, 1);
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const dateString = firstDayOfMonth.toLocaleDateString('ru-RU', {
    weekday: 'long',
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
  });

  const paddingDays = new Date(year, month, 1).getDay() || 7; // 1–7, где Пн = 1

  monthDisplay.innerText = dt.toLocaleDateString('ru-RU', {
    month: 'long',
    year: 'numeric',
  });

  calendarDays.innerHTML = '';

  for (let i = 1; i <= paddingDays + daysInMonth - 1; i++) {
    const daySquare = document.createElement("div");
    daySquare.classList.add("calendar-day");

    if (i >= paddingDays) {
      const day = i - paddingDays + 1;
      const dateStr = `${year}-${(month + 1).toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
      daySquare.innerText = day;

      daySquare.addEventListener("click", () => {
        document.getElementById("selectedDate").innerText = `${day} ${monthDisplay.innerText}`;
        selectedDate = dateStr;
      });
    } else {
      daySquare.classList.add("padding");
    }

    calendarDays.appendChild(daySquare);
  }
}

document.getElementById("nextMonth").addEventListener("click", () => {
  nav++;
  loadCalendar();
});

document.getElementById("prevMonth").addEventListener("click", () => {
  nav--;
  loadCalendar();
});

loadCalendar();
