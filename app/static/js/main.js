import { showLoginForm } from "./auth/login.js";

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("startQuizBtn").addEventListener("click", () => {
        window.location.href = "/quiz";
    });

    showLoginForm();
});
