import { init, nextQuestion, prevQuestion } from "./navigation.js";

document.getElementById("nextBtn").addEventListener("click", nextQuestion);
document.getElementById("prevBtn").addEventListener("click", prevQuestion);

// Загрузка вопросов с сервера
async function loadQuestions() {
    try {
        console.log("Запрашиваем вопросы с сервера...");
        const response = await fetch("/questions");

        if (!response.ok) throw new Error(`Ошибка загрузки вопросов: ${response.status}`);

        const questions = await response.json();
        console.log("Получены вопросы:", questions);
        return questions;
    } catch (error) {
        console.error("Ошибка загрузки вопросов:", error);
        return [];
    }
}

// Инициализация теста
async function initializeQuiz() {
    const questions = await loadQuestions();

    if (questions.length > 0) {
        init(questions);
    } else {
        console.error("Вопросы не загружены!");
    }
}

// Запуск квиза после загрузки страницы
document.addEventListener("DOMContentLoaded", () => {
    const homeBtn = document.getElementById("homeBtn");
    if (homeBtn) {
        homeBtn.addEventListener("click", () => {
            window.location.href = "/";
        });
    }
    initializeQuiz();
});
