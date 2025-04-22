const mealType = document.getElementById("mealType");
const productSearch = document.getElementById("productSearch");
const productResults = document.getElementById("productResults");
const selectedContainer = document.getElementById("selectedProducts");
const saveMealBtn = document.querySelector(".add-event-btn");
const addEventWrapper = document.querySelector(".add-event-wrapper");
const eventsContainer = document.querySelector(".events");

if (!window.mealsByDate) {
  window.mealsByDate = {};
}

const months = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

let selectedProducts = [];
let editMode = false;
let editTargetElement = null;

productSearch.addEventListener("input", debounce(async (e) => {
  const query = e.target.value.trim();
  if (query.length < 2) {
    productResults.innerHTML = "";
    return;
  }

  try {
    const res = await fetch(`/meals/search_item?query=${encodeURIComponent(query)}&limit=5`);
    const data = await res.json();
    
    productResults.innerHTML = "";
    data.forEach(item => {
      const li = document.createElement("li");
      li.textContent = item.name;
      li.classList.add("suggestion-item");
      li.addEventListener("click", () => selectProduct(item));
      productResults.appendChild(li);
    });
  } catch (err) {
    console.error("Ошибка поиска:", err);
  }
}, 300));

function selectProduct(item) {
  const existingIndex = selectedProducts.findIndex(p => p.name === item.name);
  if (existingIndex >= 0) {
    selectedProducts[existingIndex].grams += 100;
  } else {
    selectedProducts.push({
      name: item.name,
      grams: 100
    });
  }

  productSearch.value = "";
  productResults.innerHTML = "";
  renderSelected();
}

function renderSelected() {
  selectedContainer.innerHTML = "";
  selectedProducts.forEach((product, index) => {
    const div = document.createElement("div");
    div.className = "selected-product";
    div.innerHTML = `
      <span>${product.name}</span>
      <input type="number" value="${product.grams}" min="1" max="5000" data-index="${index}">
      <button class="remove-btn" data-index="${index}">×</button>
    `;
    selectedContainer.appendChild(div);
  });

  selectedContainer.querySelectorAll("input").forEach(input => {
    input.addEventListener("change", (e) => {
      let value = parseInt(e.target.value) || 1;
      if (value > 5000) value = 5000;
      selectedProducts[e.target.dataset.index].grams = value;
      input.value = value;
    });
  
    input.addEventListener("input", (e) => {
      let value = parseInt(e.target.value) || 1;
      if (value > 5000) {
        alert("Нельзя указывать больше 5000 грамм.");
        value = 5000;
        e.target.value = value;
      }
      selectedProducts[e.target.dataset.index].grams = value;
    });
  });

  selectedContainer.querySelectorAll(".remove-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      selectedProducts.splice(e.target.dataset.index, 1);
      renderSelected();
    });
  });
}

saveMealBtn.addEventListener("click", async () => {
  if (window.calendarMode !== "meals") return;
  const mealDateRaw = document.querySelector(".event-date").textContent;
  const formattedDate = formatDate(mealDateRaw);

  if (selectedProducts.length === 0) {
    alert("Добавьте продукты!");
    return;
  }

  if (!editMode) {
    const existing = window.mealsByDate[formattedDate]?.some(meal => meal.mealType === mealType.value);
    if (existing) {
      alert("Приём пищи с таким типом уже существует на эту дату.");
      return;
    }
  }

  try {
    const res = await fetch("/meals/upsert_meal", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem('authToken')}`
      },
      body: JSON.stringify({
        mealtime: mealType.value,
        meal_date: formattedDate,
        food_names: selectedProducts.map(p => p.name),
        food_quantities: selectedProducts.map(p => p.grams)
      })
    });

    const data = await res.json();

    if (res.ok) {
      updateLocalMeals(mealType.value, selectedProducts, formattedDate);
      renderEventsForDate(formattedDate);
      refreshNutrition(mealDateRaw);
      resetForm();
    } else {
      console.error("Ответ от сервера при сохранении:", data);
      throw new Error(data.message || "Ошибка сервера");
    }    
  } catch (err) {
    console.error("Ошибка сохранения:", err.message || err);
    alert("Ошибка сохранения");
  }
});

function updateMealsFromServer(dateStr, mealsObj) {
  if (window.calendarMode !== "meals") return;
  const meals = Object.entries(mealsObj).map(([mealType, data]) => ({
    mealType,
    products: data.products.map(p => {
      const match = p.match(/^(.*)\s+\((\d+(?:\.\d+)?)g\)$/);
      return match
        ? { name: match[1].trim(), grams: parseFloat(match[2]) }
        : { name: p, grams: 0 };
    }),
    mealDate: dateStr
  }));

  window.mealsByDate[dateStr] = meals;
  renderEventsForDate(dateStr);
}

window.updateMealsFromServer = updateMealsFromServer;

function updateLocalMeals(mealType, products, mealDate) {
  if (!window.mealsByDate[mealDate]) {
    window.mealsByDate[mealDate] = [];
  }

  const existingIndex = window.mealsByDate[mealDate].findIndex(m => m.mealType === mealType);
  const mealData = { mealType, products, mealDate };

  if (existingIndex >= 0) {
    window.mealsByDate[mealDate][existingIndex] = mealData;
  } else {
    window.mealsByDate[mealDate].push(mealData);
  }

  localStorage.setItem('mealsByDate', JSON.stringify(window.mealsByDate));
  renderEventsForDate(mealDate);
}

function renderEventsForDate(dateStr) {
  if (window.calendarMode !== "meals") return;
  eventsContainer.innerHTML = "";
  const meals = window.mealsByDate[dateStr] || [];

  const mealNames = {
    BREAKFAST: "Завтрак",
    LUNCH: "Обед",
    DINNER: "Ужин",
    SNACK: "Перекус"
  };

  meals.forEach(meal => {
    const div = document.createElement("div");
    div.className = "event";
    div.innerHTML = `
      <div class="title">
        <i class="fas fa-utensils"></i>
        <h3>${mealNames[meal.mealType] || meal.mealType}</h3>
      </div>
      <div class="products">
        ${meal.products.map(p => `${p.name} (${p.grams}г)`).join(", ")}
      </div>
      <div class="actions">
        <button class="edit" data-type="${meal.mealType}">
          <i class="ri-edit-line"></i>
        </button>
        <button class="delete" data-type="${meal.mealType}">
          <i class="ri-delete-bin-line"></i>
        </button>
      </div>
    `;

    div.querySelector(".edit").addEventListener("click", () => {
      editMeal(meal.mealType, dateStr);
    });

    div.querySelector(".delete").addEventListener("click", () => {
      deleteMeal(meal.mealType, dateStr);
    });

    eventsContainer.appendChild(div);
  });
}

function editMeal(mealType, dateStr) {
  if (window.calendarMode !== "meals") return;
  const meal = window.mealsByDate[dateStr].find(m => m.mealType === mealType);
  if (!meal) return;

  selectedProducts = meal.products.map(p => ({ ...p }));
  document.getElementById("mealType").value = mealType;
  document.getElementById("mealType").disabled = true;

  document.querySelector(".add-event-body").style.display = "flex";
  document.querySelector(".add-workout-body").style.display = "none";

  document.querySelector(".add-event-wrapper").classList.add("active");
  editMode = true;
  editTargetElement = { mealType, dateStr };
  renderSelected();
}

async function deleteMeal(mealType, dateStr) {
  if (window.calendarMode !== "meals") return;
  if (!confirm("Удалить этот приём пищи?")) return;

  const formattedDate = formatDate(dateStr);
  const query = `?meal_date=${encodeURIComponent(formattedDate)}&mealtime=${encodeURIComponent(mealType)}`;

  try {
    const res = await fetch(`/meals/delete_meal${query}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" }
    });

    if (res.ok) {
      if (!window.mealsByDate) window.mealsByDate = {};
      if (window.mealsByDate[dateStr]) {
        window.mealsByDate[dateStr] = window.mealsByDate[dateStr].filter(
          (m) => m.mealType !== mealType
        );
        if (window.mealsByDate[dateStr].length === 0) {
          delete window.mealsByDate[dateStr];
        }
      }

      renderEventsForDate(dateStr);

      const serverDate = formatDateForServer(dateStr);
      fetch(`/meals/daily_nutrition?target_date=${serverDate}`)
        .then(res => res.json())
        .then(nutrition => {
          document.getElementById("calories").textContent = nutrition.total_calories || 0;
          document.getElementById("proteins").textContent = nutrition.total_proteins || 0;
          document.getElementById("fats").textContent = nutrition.total_fats || 0;
          document.getElementById("carbs").textContent = nutrition.total_carbs || 0;
        });
    } else {
      const error = await res.json();
      console.error("Ошибка ответа сервера:", res.status, error);
    }
  } catch (err) {
    console.error("Ошибка удаления:", err);
  }
}

function formatDateForServer(str) {
  const [day, monthName, year] = str.trim().split(" ");
  const monthIndex = months.indexOf(monthName);
  return `${year}-${String(monthIndex + 1).padStart(2, "0")}-${day.padStart(2, "0")}`;
}

function refreshNutrition(formattedDate) {
  const serverDate = formatDateForServer(formattedDate);
  fetch(`/meals/daily_nutrition?target_date=${serverDate}`)
    .then(res => res.json())
    .then(nutrition => {
      document.getElementById("calories").textContent = nutrition.total_calories || 0;
      document.getElementById("proteins").textContent = nutrition.total_proteins || 0;
      document.getElementById("fats").textContent = nutrition.total_fats || 0;
      document.getElementById("carbs").textContent = nutrition.total_carbs || 0;
    })
    .catch(err => {
      console.error("Ошибка обновления нутриентов:", err);
    });
}

function formatDate(dateStr) {
  if (/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) {
    return dateStr;
  }
  const [day, monthName, year] = dateStr.split(" ");
  const monthIndex = months.indexOf(monthName);
  return `${year}-${String(monthIndex + 1).padStart(2, '0')}-${day.padStart(2, '0')}`;
}

async function updateNutritionInfo(dateStr) {
  const formatted = formatDate(dateStr);
  try {
    const res = await fetch(`/meals/daily_nutrition?target_date=${formatted}`);
    const data = await res.json();

    document.querySelector(".nutrition-info").innerHTML = `
      <div>Калории: ${data.total_calories}</div>
      <div>Белки: ${data.total_proteins} г</div>
      <div>Жиры: ${data.total_fats} г</div>
      <div>Углеводы: ${data.total_carbs} г</div>
    `;
  } catch (err) {
    console.error("Ошибка при загрузке нутриентов:", err);
  }
}

window.updateNutritionInfo = updateNutritionInfo;

function resetForm() {
  selectedProducts = [];
  productSearch.value = "";
  productResults.innerHTML = "";
  selectedContainer.innerHTML = "";
  mealType.disabled = false;
  mealType.value = "BREAKFAST";
  addEventWrapper.classList.remove("active");
  editMode = false;
}

function debounce(func, timeout = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => { func.apply(this, args); }, timeout);
  };
}

window.calendarMode = "meals";