import { renderQuestion } from "./ui.js";
import { questions } from "./questions.js";

let currentQuestionIndex = 0;
let answers = {}; // Ответы пользователя

export function init() {
    console.log("Опросник инициализирован"); // Проверяю грузит или нет 
    loadQuestion();
}

export function loadQuestion() {
    if (questions.length === 0) {
        console.error("Ошибка: Вопросы не загружены");
        return;
    }
    
    console.log("Текущий вопрос:", questions[currentQuestionIndex]); // Проверяю грузится ли первый вопрос
    renderQuestion(questions[currentQuestionIndex], answers);
    updateButtons();
}

export function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        loadQuestion();
    } else {
        showFinalScreen();
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

function showFinalScreen() {
    document.getElementById("question-container").innerHTML = "<h2>Спасибо за прохождение опроса!</h2>";
    document.getElementById("prevBtn").style.display = "none";
    document.getElementById("nextBtn").style.display = "none";

    const registerButton = document.createElement("button");
    registerButton.classList.add("register-btn");
    registerButton.innerText = "Зарегистрироваться";
    registerButton.onclick = showRegisterForm;

    document.querySelector("main").appendChild(registerButton);
}

function showRegisterForm() {
    const main = document.querySelector("main");
    main.innerHTML = `
        <h2>Пройдите регистрацию</h2>
        <form id="register-form">
            <input type="text" id="name" placeholder="Ваше имя" required><br>
            <input type="email" id="email" placeholder="Email" required><br>
            <input type="password" id="password" placeholder="Пароль" required><br>
            <input type="password" id="password" placeholder="Подтвердите пароль" required><br>
            <button type="submit" class="register-btn">Зарегистрироваться</button>
        </form>
    `;

    document.getElementById("register-form").addEventListener("submit", registerUser);
}

function registerUser(event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!name || !email || !password) {
        alert("Заполните все поля!");
        return;
    }

    console.log("Отправка данных:", { name, email, password });

    fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || "Регистрация успешна!");
    })
    .catch(error => console.error("Ошибка:", error));
}
