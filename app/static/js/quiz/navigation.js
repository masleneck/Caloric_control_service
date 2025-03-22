import { renderQuestion } from "./ui.js";
import { processResults } from "./result.js";

let currentQuestionIndex = 0;
export let answers = {}; 
let questions = [];

function getAnswerByName(name) {
    return answers[name] || null;
}

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

    if (currentQuestionIndex >= questions.length) {
        processResults(answers);
        return;
    }

    console.log("Текущий вопрос:", questions[currentQuestionIndex]);
    renderQuestion(questions[currentQuestionIndex], answers);
    updateButtons();
}

export function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        loadQuestion();
    } else {
        processResults(answers);
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
    nextBtn.disabled = !answers[questions[currentQuestionIndex]?.name];

    document.querySelector(".progress").style.width = `${((currentQuestionIndex + 1) / questions.length) * 100}%`;
    document.getElementById("step-counter").innerText = `${currentQuestionIndex + 1}/${questions.length}`;
}
