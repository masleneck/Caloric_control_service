document.addEventListener("DOMContentLoaded", async () => {
  const nameEl = document.getElementById("name");
  const lastNameEl = document.getElementById("last-name");
  const genderEl = document.getElementById("gender");
  const birthdayEl = document.getElementById("birthday");
  const weightEl = document.getElementById("weight");
  const heightEl = document.getElementById("height");
  const goalEl = document.getElementById("goal");
  const bmiValueEl = document.getElementById("bmi-value");
  const editBtn = document.getElementById("edit-btn");
  const editForm = document.getElementById("edit-form");
  const confidentialForm = document.getElementById("confidential-form");
  const formWrapper = document.getElementById("form-wrapper");
  const homeBtn = document.getElementById("homeBtn");

  let isEditing = false;

  if (homeBtn) {
    homeBtn.addEventListener("click", () => {
      window.location.href = "/home";
    });
  }

  editBtn.addEventListener("click", async () => {
    isEditing = !isEditing;

    if (isEditing) {
      editBtn.textContent = "Отменить";
      formWrapper.style.display = "flex";
      await loadProfile();
    } else {
      editBtn.textContent = "Редактировать";
      formWrapper.style.display = "none";
    }
  });

  async function loadProfile() {
    try {
      const res = await fetch("/profile/profile_info");
      if (!res.ok) throw new Error("Не удалось загрузить профиль");
      const data = await res.json();

      nameEl.textContent = data.name;
      lastNameEl.textContent = data.last_name;
      genderEl.textContent = data.gender === "MALE" ? "Мужской" : "Женский";
      birthdayEl.textContent = data.birthday_date;
      weightEl.textContent = data.weight;
      heightEl.textContent = data.height;
      goalEl.textContent = data.goal;
      bmiValueEl.textContent = data.bmi ?? "--";

      document.getElementById("edit-name").value = data.name;
      document.getElementById("edit-last-name").value = data.last_name;
      document.getElementById("edit-gender").value = data.gender;
      document.getElementById("edit-birthday").value = data.birthday_date;
    } catch (err) {
      console.error(err);
    }
  }

  editForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const profileData = {
      name: document.getElementById("edit-name").value,
      last_name: document.getElementById("edit-last-name").value,
      gender: document.getElementById("edit-gender").value,
      birthday_date: document.getElementById("edit-birthday").value,
      weight: parseFloat(weightEl.textContent),
      height: parseFloat(heightEl.textContent),
      goal: goalEl.textContent,
    };

    try {
      const res = await fetch("/profile/update_profile", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(profileData)
      });

      if (!res.ok) throw new Error("Ошибка при обновлении профиля");

      alert("Профиль обновлён!");
      await loadProfile();
    } catch (err) {
      console.error(err);
      alert("Не удалось обновить профиль");
    }
  });

  confidentialForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const confidentialData = {
      current_email: document.getElementById("edit-email").value,
      current_password: document.getElementById("current-password").value,
      new_password: document.getElementById("new-password").value,
      confirm_new_password: document.getElementById("confirm-new-password").value
    };

    try {
      const res = await fetch("/profile/update_confidential_info", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(confidentialData)
      });

      if (!res.ok) throw new Error("Ошибка при обновлении пароля");

      alert("Пароль обновлён!");
      confidentialForm.reset();
    } catch (err) {
      console.error(err);
      alert("Не удалось обновить пароль");
    }
  });

  flatpickr("#edit-birthday", {
    locale: "ru",
    dateFormat: "Y-m-d",
    maxDate: "today",
    altInput: true,
    altFormat: "Y.m.d",
  });

  await loadProfile();
});
