import { init, nextQuestion, prevQuestion } from "./navigation.js";
import { questions as mockQuestions } from "../questions.js";

document.getElementById("nextBtn").addEventListener("click", nextQuestion);
document.getElementById("prevBtn").addEventListener("click", prevQuestion);

// Загрузка вопросов
async function loadQuestions() {
    try {
        const response = await fetch("/questions");
        if (!response.ok) throw new Error("Ошибка загрузки вопросов");
        return await response.json();
    } catch (error) {
        console.error("Ошибка загрузки, используем моковые данные:", error);
        return mockQuestions; // Используем моковые вопросы
    }
}

// Инициализация опросника
async function initializeQuiz() {
    const questions = await loadQuestions();
    
    if (questions.length > 0) {
        init(questions); // Запускаем опросник
    } else {
        console.error("Вопросы не загружены");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const homeBtn = document.getElementById("homeBtn");

    if (homeBtn) {
        homeBtn.addEventListener("click", () => {
            window.location.href = "index.html";
        });
    }
});

// Запускаем опросник
initializeQuiz();
