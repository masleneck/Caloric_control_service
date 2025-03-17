document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("startQuizBtn").addEventListener("click", () => {
        window.location.href = "quiz.html"; // Переход на страницу опросника
    });

    // Вызываем отрисовку формы сразу после загрузки страницы
    showLoginForm();
});

// Функция для отрисовки формы входа сразу при загрузке страницы
function showLoginForm() {
    const main = document.getElementById("start-screen");

    // Проверяем, нет ли уже формы, чтобы не дублировать
    if (document.getElementById("login-form")) return;

    console.log("Отображение формы входа");

    const loginFormContainer = document.createElement("div");
    loginFormContainer.innerHTML = `
        <h2>Авторизация</h2>
        <form id="login-form">
            <input type="text" id="login" placeholder="Логин" required><br>
            <input type="password" id="login-password" placeholder="Пароль" required><br>
            <button type="submit" class="login-btn">Войти</button>
        </form>
    `;

    main.appendChild(loginFormContainer);

    // Вешаем обработчик на отправку формы
    document.getElementById("login-form").addEventListener("submit", loginUser);
}

// Функция отправки формы входа
function loginUser(event) {
    event.preventDefault(); 

    const login = document.getElementById("login").value.trim();
    const password = document.getElementById("login-password").value.trim();

    if (!login || !password) {
        alert("Введите логин и пароль!");
        return;
    }

    console.log("Отправка данных:", { login, password });

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ login, password })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Ответ от сервера:", data);
        alert(data.message || "Успешный вход!");
        window.location.href = "/home"; // Перенаправляем после входа
    })
    .catch(error => console.error("Ошибка авторизации:", error));
}
