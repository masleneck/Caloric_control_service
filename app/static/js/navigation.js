import { renderQuestion } from "./ui.js";
import { questions, loadQuestions } from "./questions.js";


let currentQuestionIndex = 0;
let answers = {}; // Ответы пользователя


// Загружаем вопросы перед первым рендером
export async function init() {
    await loadQuestions();  // Загружаем вопросы ОДИН раз
    loadQuestion();
}

// Загружает текущий вопрос на страницу
export function loadQuestion() {
    if (questions.length === 0) return;  // Проверяем, что вопросы загружены

    renderQuestion(questions[currentQuestionIndex], answers);
    updateButtons();
}

// Переход к следующему вопросу
export function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        loadQuestion();
    } else {
        showFinalScreen();
    }
}

// Переход к предыдущему вопросу
export function prevQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        loadQuestion();
    }
}

// Обновляем состояние кнопок
export function updateButtons() {
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    prevBtn.disabled = currentQuestionIndex === 0;
    nextBtn.disabled = !answers[questions[currentQuestionIndex]?.id];

    document.querySelector(".progress").style.width = `${((currentQuestionIndex + 1) / questions.length) * 100}%`;
    document.getElementById("step-counter").innerText = `${currentQuestionIndex + 1}/${questions.length}`;
}

// Финальный экран с кнопкой "Зарегистрироваться"
function showFinalScreen() {
    document.getElementById("question-container").innerHTML = "<h2>Сигмоида</h2>";
    document.getElementById("prevBtn").style.display = "none";
    document.getElementById("nextBtn").style.display = "none";

    // Добавляем кнопку "Зарегистрироваться"
    const registerButton = document.createElement("a");
    registerButton.href = ""; // Ссылка на регистрацию
    registerButton.classList.add("register-btn");
    registerButton.innerText = "Зарегистрироваться";

    document.querySelector("main").appendChild(registerButton);
}
