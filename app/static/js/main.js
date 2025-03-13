import { init, nextQuestion, prevQuestion } from "./navigation.js";

document.getElementById("nextBtn").addEventListener("click", nextQuestion);
document.getElementById("prevBtn").addEventListener("click", prevQuestion);

// Загрузка вопросов из бэка
async function loadQuestions() {
    try {
        const response = await fetch("/questions/");
        if (!response.ok) throw new Error("Ошибка загрузки вопросов");
        return await response.json();
    } catch (error) {
        console.error("Ошибка:", error);
        return [];
    }
}

// Инициализация с загрузкой вопросов
async function initialize() {
    const questions = await loadQuestions();
    if (questions.length > 0) {
        init(questions);
    } else {
        console.error("Вопросы не загружены");
    }
}

initialize();