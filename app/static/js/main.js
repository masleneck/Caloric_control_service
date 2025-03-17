document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("startQuizBtn").addEventListener("click", () => {
        window.location.href = "quiz.html"; // Переход на страницу опросника
    });

    // Вызываем отрисовку формы сразу после загрузки страницы
    showLoginForm();
});

// Функция для отрисовки формы входа
function showLoginForm() {
    const main = document.getElementById("start-screen");

    // Проверяем, существует ли элемент main
    if (!main) {
        console.error("Элемент с id 'start-screen' не найден!");
        return;
    }

    // Проверяем, нет ли уже формы, чтобы не дублировать
    if (document.getElementById("login-form")) {
        console.log("Форма входа уже отображена");
        return;
    }

    console.log("Отображение формы входа");

    // Очищаем содержимое main перед добавлением формы
    main.innerHTML = "";

    const loginFormContainer = document.createElement("div");
    loginFormContainer.innerHTML = `
        <h2>Авторизация</h2>
        <form id="login-form">
            <input type="text" id="login" placeholder="Логин" required><br>
            <input type="password" id="login-password" placeholder="Пароль" required><br>
            <button type="submit" class="login-btn">Войти</button>
            <div id="error-message"></div> <!-- Контейнер для ошибок -->
        </form>
    `;

    main.appendChild(loginFormContainer);

    // Вешаем обработчик на отправку формы
    document.getElementById("login-form").addEventListener("submit", loginUser);
}

// Функция отправки формы входа
async function loginUser(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const email = document.getElementById("login").value.trim(); // Используем email, а не login
    const password = document.getElementById("login-password").value.trim();

    if (!email || !password) {
        showError("Введите email и пароль!");
        return;
    }

    try {
        const response = await fetch("/auth/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }) // Отправляем email и пароль
        });

        console.log("Статус ответа:", response.status); 
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Ошибка авторизации");
        }

        const data = await response.json();
        console.log("Ответ от сервера:", data);

        // Перенаправляем пользователя на главную страницу после успешной авторизации
        window.location.href = "/home";
    } catch (error) {
        console.error("Ошибка авторизации:", error);
        showError(error.message || "Ошибка авторизации");
    }
}

// Функция для отображения ошибок
function showError(message) {
    const errorContainer = document.getElementById("error-message");

    // Если контейнера для ошибок нет, создаем его
    if (!errorContainer) {
        const errorDiv = document.createElement("div");
        errorDiv.id = "error-message";
        errorDiv.style.color = "red";
        errorDiv.style.marginTop = "10px";
        document.getElementById("login-form").appendChild(errorDiv);
    }

    // Отображаем сообщение об ошибке
    document.getElementById("error-message").textContent = message;
}

// Вызываем функцию отображения формы при загрузке страницы
showLoginForm();