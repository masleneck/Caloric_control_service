import { renderQuestion } from "./ui.js";

let currentQuestionIndex = 0;
let answers = {};
let questions = [];

export function init(loadedQuestions) {
    questions = loadedQuestions;
    console.log("Опросник инициализирован с вопросами:", questions);
    loadQuestion();
}

export function loadQuestion() {
    if (questions.length === 0) {
        console.error("Ошибка: Вопросы не загружены");
        return;
    }

    console.log("Текущий вопрос:", questions[currentQuestionIndex]);
    renderQuestion(questions[currentQuestionIndex], answers);
    updateButtons();
}

export function nextQuestion() {
    console.log(`Переход к следующему вопросу: ${currentQuestionIndex + 1} из ${questions.length}`);

    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        loadQuestion();
    } else {
        console.log("Опрос завершен. Переход к форме регистрации.");
        setTimeout(showRegisterForm, 500);  // Небольшая задержка для вайба
    }
}

export function prevQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        loadQuestion();
    }
}

export function updateButtons() {
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    prevBtn.disabled = currentQuestionIndex === 0;
    nextBtn.disabled = !answers[questions[currentQuestionIndex]?.id];

    document.querySelector(".progress").style.width = `${((currentQuestionIndex + 1) / questions.length) * 100}%`;
    document.getElementById("step-counter").innerText = `${currentQuestionIndex + 1}/${questions.length}`;
}

// Форма регистрации после последнего вопроса
function showRegisterForm() {
    console.log("Переход на форму регистрации...");

    const main = document.getElementById("quiz-container");
    
    if (!main) {
        console.error("Ошибка: контейнер для формы регистрации не найден!");
        return;
    }

    // Очищаем `main` перед добавлением формы
    main.innerHTML = `
        <h2>Пройдите регистрацию</h2>
        <form id="register-form">
            <input type="text" id="fullname" placeholder="Ваше имя" required><br>
            <input type="email" id="email" placeholder="Email" required><br>
            <input type="password" id="password" placeholder="Пароль" required><br>
            <input type="password" id="confirm_password" placeholder="Подтвердите пароль" required><br>
            <button type="submit" class="register-btn">Зарегистрироваться</button>
        </form>
    `;

    document.getElementById("register-form").addEventListener("submit", registerUser);
}

// Обработка регистрации + редирект на главную
async function registerUser(event) {
    event.preventDefault();

    const fullname = document.getElementById("fullname").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirm_password").value.trim();

    if (!fullname || !email || !password || !confirmPassword) {
        alert("Заполните все поля!");
        return;
    }

    if (password !== confirmPassword) {
        alert("Пароли не совпадают!");
        return;
    }

    console.log("Отправка данных:", { fullname, email, password, confirmPassword });

    try {
        const response = await fetch("/auth/register/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ fullname, email, password, confirm_password: confirmPassword })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || "Ошибка при регистрации");
        }

        const data = await response.json();
        alert(data.message || "Регистрация успешна!");
        window.location.href = "/"; // Перенаправляем на главную страницу
    } catch (error) {
        console.error("Ошибка:", error);
        alert(error.message || "Произошла ошибка при регистрации");
    }
}