import { setupLogout } from './logout.js';

  document.addEventListener("DOMContentLoaded", () => {
      setupLogout();
  });

  document.getElementById("nav-home").addEventListener("click", () => {
      alert("Home clicked");
  });

  document.getElementById("nav-profile").addEventListener("click", () => {
    window.location.href = "/profile";
  });

  document.getElementById("nav-options").addEventListener("click", () => {
      alert("Options clicked");
  });

  document.getElementById("nav-meals").addEventListener("click", () => {
      alert("Meals clicked");
  });

  document.getElementById("nav-training").addEventListener("click", () => {
      alert("Training clicked");
  });
