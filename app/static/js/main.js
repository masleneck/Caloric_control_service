document.getElementById("startQuizBtn").addEventListener("click", () => {
    window.location.href = "quiz.html"; // Переход на страницу опросника
});

document.getElementById("loginBtn").addEventListener("click", showLoginForm);

// Показываем форму входа
function showLoginForm() {
    const main = document.getElementById("start-screen");
    main.innerHTML = `
        <h2>Вход</h2>
        <form id="login-form">
            <input type="text" id="login" placeholder="Логин" required><br>
            <input type="password" id="login-password" placeholder="Пароль" required><br>
            <button type="submit" class="register-btn">Войти</button>
        </form>
    `;

    document.getElementById("login-form").addEventListener("submit", loginUser);
}

// Обрабатываем вход
function loginUser(event) {
    event.preventDefault();

    const login = document.getElementById("login").value.trim();
    const password = document.getElementById("login-password").value.trim();

    if (!login || !password) {
        alert("Введите логин и пароль!");
        return;
    }

    console.log("Отправка данных для входа:", { login, password });

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ login, password })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || "Успешный вход!");
        window.location.href = "/home"; // Перенаправляем после входа
    })
    .catch(error => console.error("Ошибка авторизации:", error));
}
