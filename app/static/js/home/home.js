document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("logoutBtn").addEventListener("click", () => {
      console.log("Logging out...");
      window.location.href = "/";
  });

  // Заглушки
  document.getElementById("nav-home").addEventListener("click", () => {
      alert("Home clicked");
  });

  document.getElementById("nav-profile").addEventListener("click", () => {
      alert("Profile clicked");
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
});
