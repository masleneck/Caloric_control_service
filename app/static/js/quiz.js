import { init, nextQuestion, prevQuestion } from "./navigation.js";

document.getElementById("nextBtn").addEventListener("click", nextQuestion);
document.getElementById("prevBtn").addEventListener("click", prevQuestion);

// Функция загрузки вопросов с сервера
async function loadQuestions() {
    try {
        console.log("Запрашиваем вопросы с сервера...");
        const response = await fetch("http://127.0.0.1:8000/questions"); // Полный URL

        if (!response.ok) throw new Error(`Ошибка загрузки вопросов: ${response.status}`);

        const questions = await response.json();
        console.log("Получены вопросы:", questions);
        return questions;
    } catch (error) {
        console.error("Ошибка загрузки вопросов:", error);
        return []; // Возвращаем пустой массив при ошибке
    }
}

// Функция инициализации опросника
async function initializeQuiz() {
    const questions = await loadQuestions();
    
    if (questions.length > 0) {
        init(questions); // Запускаем опросник
    } else {
        console.error("Вопросы не загружены!");
    }
}

// Ждем загрузку DOM и запускаем опросник
document.addEventListener("DOMContentLoaded", () => {
    const homeBtn = document.getElementById("homeBtn");
    if (homeBtn) {
        homeBtn.addEventListener("click", () => {
            window.location.href = "/";
        });
    }
    initializeQuiz();
});
