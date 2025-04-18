export function showRegisterForm() {
    console.log("Переход на форму регистрации...");
  
    const main = document.getElementById("quiz-container");
    main.innerHTML = `
        <div class="register-card">
            <h2 class="results-title">Пройдите регистрацию</h2>
            <form id="register-form" class="register-form">
                <input type="text" id="fullname" placeholder="Ваше имя" required>
                <input type="email" id="email" placeholder="Email" required>
                <input type="password" id="password" placeholder="Пароль" required>
                <input type="password" id="confirm_password" placeholder="Подтвердите пароль" required>
                <button type="submit" class="register-btn">Зарегистрироваться</button>
            </form>
        </div>
    `;
  
    document.getElementById("register-form").addEventListener("submit", registerUser);
  }  

async function registerUser(event) {
  event.preventDefault();

  const fullname = document.getElementById("fullname").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm_password").value;

  if (password !== confirmPassword) {
      alert("Пароли не совпадают!");
      return;
  }

  try {
      const response = await fetch("/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ fullname, email, password, confirm_password: confirmPassword })
      });

      if (!response.ok) throw new Error("Ошибка регистрации");

      alert("Регистрация успешна! Войдите в систему.");
      window.location.href = "/";
  } catch (error) {
      console.error("Ошибка регистрации:", error);
  }
}
