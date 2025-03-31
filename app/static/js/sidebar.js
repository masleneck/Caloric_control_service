document.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;

  const navMap = {
    "/home": "nav-home",
    "/profile": "nav-profile",
    "/options": "nav-options",
    "/meals": "nav-meals",
    "/training": "nav-training"
  };

  const urlMap = {
    "nav-home": "/home",
    "nav-profile": "/profile",
    "nav-options": "/options",
    "nav-meals": "/meals",
    "nav-training": "/training"
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
