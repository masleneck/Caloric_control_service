import { init, nextQuestion, prevQuestion } from "./navigation.js";
import { questions as mockQuestions } from "./questions.js";

document.getElementById("startQuizBtn").addEventListener("click", startQuiz);
document.getElementById("loginBtn").addEventListener("click", showLoginForm);
document.getElementById("nextBtn").addEventListener("click", nextQuestion);
document.getElementById("prevBtn").addEventListener("click", prevQuestion);

// Функция для загрузки вопросов
async function loadQuestions() {
    try {
        const response = await fetch("/questions/");
        if (!response.ok) throw new Error("Ошибка загрузки вопросов");
        return await response.json();
    } catch (error) {
        console.error("Ошибка при загрузке вопросов, используем моковые данные:", error);
        return mockQuestions;
    }
}

// Запуск опроса
async function startQuiz() {
    document.getElementById("start-screen").style.display = "none";
    document.getElementById("quiz-container").style.display = "block";
    const questions = await loadQuestions();
    
    if (questions.length > 0) {
        init(questions);
    } else {
        console.error("Вопросы не загружены");
    }
}

// Отображение формы входа
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

// Авторизация пользователя
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
    })
    .catch(error => console.error("Ошибка авторизации:", error));
}