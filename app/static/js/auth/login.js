export function showLoginForm() {
    const main = document.getElementById("start-screen");
  
    if (!main) {
      console.error("Элемент с id 'start-screen' не найден!");
      return;
    }
  
    if (document.getElementById("login-form")) {
      console.log("Форма входа уже отображена");
      return;
    }
  
    const loginFormContainer = document.createElement("div");
    loginFormContainer.innerHTML = `
      <div class="login-card">
        <h2 class="results-title">Авторизация</h2>
        <form id="login-form" class="register-form">
          <input type="text" id="login" placeholder="Email" required />
          <input type="password" id="login-password" placeholder="Пароль" required />
          <button type="submit" class="login-btn">Войти</button>
          <div id="error-message" class="error-message" style="display: none;"></div>
        </form>
      </div>
    `;
  
    main.appendChild(loginFormContainer);
  
    document.getElementById("login-form").addEventListener("submit", loginUser);
  }
  
  export async function loginUser(event) {
    event.preventDefault();
  
    const email = document.getElementById("login").value.trim();
    const password = document.getElementById("login-password").value.trim();
  
    if (!email || !password) {
      showError("Введите email и пароль!");
      return;
    }
  
    try {
      const response = await fetch("/auth/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        let message = "Ошибка авторизации";
      
        if (typeof errorData.detail === "string") {
          message = mapCustomError(errorData.detail);
        } else if (Array.isArray(errorData.detail)) {
          message = errorData.detail.map(e => mapCustomError(e.msg || e)).join(", ");
        } else if (typeof errorData.detail === "object") {
          message = Object.values(errorData.detail).map(mapCustomError).join(", ");
        }
      
        throw new Error(message);
      }
  
      const data = await response.json();
      console.log("Ответ от сервера:", data);
      console.log("Редирект на /home...");
      window.location.href = "/home";
    } catch (error) {
      console.error("Ошибка авторизации:", error);
      showError(error.message || "Ошибка авторизации");
    }
  }

  function mapCustomError(msg) {
    if (msg.includes("valid email address")) {
      return "Введите корректный email с символом @";
    }
    if (msg.includes("password") && msg.includes("too short")) {
      return "Пароль слишком короткий";
    }
    return msg;
  }
  
  function showError(message) {
    const errorContainer = document.getElementById("error-message");
    if (!errorContainer) return;
  
    errorContainer.innerHTML = `<i class="ri-error-warning-line"></i> ${message}`;
    errorContainer.style.display = "block";
  }
  