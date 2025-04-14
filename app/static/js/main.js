import { showLoginForm } from "./auth/login.js";
import { loginUser } from "./auth/login.js";

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("startQuizBtn").addEventListener("click", () => {
        window.location.href = "/quiz";
    });

    showLoginForm();
});

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", loginUser);
  }
});
