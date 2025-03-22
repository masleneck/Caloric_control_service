export function setupLogout() {
  const logoutBtn = document.getElementById("logoutBtn");

  if (!logoutBtn) {
      console.error("Кнопка LOGOUT не найдена!");
      return;
  }

  logoutBtn.addEventListener("click", async () => {
      try {
          const response = await fetch("/auth/logout", {
              method: "POST",
              credentials: "include"
          });

          if (response.ok) {
              console.log("Вы успешно вышли из системы!");
              window.location.href = "/";
          } else {
              console.log("Ошибка при выходе из системы.");
          }
      } catch (error) {
          console.error("Ошибка при выходе:", error);
          alert("Что-то пошло не так при выходе.");
      }
  });
}
