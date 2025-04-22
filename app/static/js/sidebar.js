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

  loadUserNameAndStatus();
});

async function loadUserNameAndStatus() {
  try {
    const resProfile = await fetch("/profile/profile_info");
    if (!resProfile.ok) throw new Error("Ошибка при получении профиля");

    const profileData = await resProfile.json();
    const fullName = `${profileData.name} ${profileData.last_name}`;
    const usernameEl = document.getElementById("sidebar-username");
    if (usernameEl) {
      usernameEl.textContent = fullName;
    }

    const resStatus = await fetch("/profile/r_status");
    if (!resStatus.ok) throw new Error("Ошибка при получении статуса");

    const statusData = await resStatus.json();
    const status = statusData.status || "UNKNOWN";

    const readableStatus = {
      "SEDENTARY": "Малоподвижный",
      "LIGHT": "Низкая активность",
      "MODERATE": "Умеренная активность",
      "ACTIVE": "Активный",
      "ATHLETE": "Спортсмен"
    };

    const tooltipText = `Ваша активность за последние 7 дней:
0–1.5 ч — Малоподвижный
1.5–3 ч — Низкая активность
3–5 ч — Умеренная активность
5–8 ч — Активный
8+ ч — Спортсмен`;

    const statusEl = document.getElementById("sidebar-status");
    if (statusEl) {
      const cssClass = `status-${status.toLowerCase()}`;
      statusEl.innerHTML = `
        <span 
          class="${cssClass}" 
          title="${tooltipText}"
        >
          ${readableStatus[status] || "Неизвестно"}
        </span>
      `;
    }

  } catch (err) {
    console.error("Ошибка загрузки профиля или статуса:", err);
    const statusEl = document.getElementById("sidebar-status");
    if (statusEl) {
      statusEl.textContent = "Гость";
    }
  }
}

