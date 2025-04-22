document.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;

  const navMap = {
    "/home": "nav-home",
    "/profile": "nav-profile"
  };

  const urlMap = {
    "nav-home": "/home",
    "nav-profile": "/profile"
  };

  const activeBtnId = navMap[path];
  if (activeBtnId) {
    const activeBtn = document.getElementById(activeBtnId);
    if (activeBtn) {
      activeBtn.classList.add("active");
    }
  }

  for (const [btnId, url] of Object.entries(urlMap)) {
    const btn = document.getElementById(btnId);
    if (btn) {
      btn.addEventListener("click", () => {
        window.location.href = url;
      });
    }
  }
});

document.addEventListener("DOMContentLoaded", () => {
  loadUserName();
});

async function loadUserName() {
  try {
    const res = await fetch("/profile/profile_info");
    if (!res.ok) throw new Error("Ошибка при получении профиля");

    const data = await res.json();
    const fullName = `${data.name} ${data.last_name}`;
    
    const usernameEl = document.getElementById("sidebar-username");
    if (usernameEl) {
      usernameEl.textContent = fullName;
    }

    const statusEl = document.getElementById("sidebar-status");
    if (statusEl) {
      statusEl.textContent = "Профиль загружен";
    }

  } catch (err) {
    console.error("Ошибка загрузки профиля в сайдбар:", err);

    const statusEl = document.getElementById("sidebar-status");
    if (statusEl) {
      statusEl.textContent = "Гость";
    }
  }
}
