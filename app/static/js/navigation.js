import { renderQuestion } from "./ui.js";

let currentQuestionIndex = 0;
export let answers = {};  // Экспортируем answers
let questions = [];
let sessionId = null; // Добавляем sessionId для сохранения теста

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
        processResults();
        return;
    }

    console.log("Текущий вопрос:", questions[currentQuestionIndex]);
    renderQuestion(questions[currentQuestionIndex], answers);  // Передаём answers в renderQuestion
    updateButtons();
}

export function nextQuestion() {
    console.log(`Переход к следующему вопросу: ${currentQuestionIndex + 1} из ${questions.length}`);

    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        loadQuestion();
    } else {
        console.log("Опрос завершен. Рассчитываем результаты...");
        processResults();
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

// Функция обработки и отправки результатов
async function processResults() {
    console.log("Отправка данных для расчёта...");
    console.log("Проверка сохранённых ответов перед отправкой:", answers);

    // Маппинг значений, чтобы они соответствовали API
    const genderMap = {
        "Мужской": "MALE",
        "Женский": "FEMALE"
    };

    const goalMap = {
        "Снизить вес": "LOSE_WEIGHT",
        "Поддерживать форму": "KEEPING_FIT",
        "Набрать мышечную массу": "GAIN_MUSCLE_MASS"
    };

    // Преобразуем ответы в корректный формат
    const formattedAnswers = {
        gender: genderMap[answers[27]] || "UNKNOWN",
        birthday_date: answers[28] || "Ошибка: не указана",
        height: Number(answers[29]) || 0,
        weight: Number(answers[30]) || 0,
        goal: goalMap[answers[31]] || "UNKNOWN",
        bad_habits: answers[32] || "Не указано",
        steps_per_day: Number(answers[33]) || 0,
        sleep_hours: Number(answers[34]) || 0,
        water_intake: answers[35] || "Не указано",
        hormone_issues: answers[36] || "Не указано"
    };

    console.log("Исправленный объект перед отправкой:", formattedAnswers);

    try {
        // Отправляем данные в `/questions/calculate`
        const response = await fetch("/questions/calculate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formattedAnswers),
        });

        if (!response.ok) throw new Error(`Ошибка расчёта: ${response.status}`);

        const results = await response.json();
        console.log("Рассчитанные данные:", results);

        // Сохраняем результат теста в `/save_test_result/`
        await saveTestResult(formattedAnswers);

        // Показываем результаты пользователю
        showResults(results);
    } catch (error) {
        console.error("Ошибка расчёта:", error);
    }
}

// Функция сохранения теста в `/save_test_result/`
async function saveTestResult(data) {
    console.log("Сохранение результатов теста...");

    try {
        const response = await fetch("/questions/save_test_result/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (!response.ok) throw new Error(`Ошибка сохранения: ${response.status}`);

        const responseData = await response.json();
        console.log("Тест успешно сохранён! Session ID:", responseData.session_id);
        sessionId = responseData.session_id; // Сохраняем sessionId
    } catch (error) {
        console.error("Ошибка сохранения теста:", error);
    }
}

// Функция отображения результатов
function showResults(results) {
    console.log("Вывод результатов...");

    const main = document.getElementById("quiz-container");
    main.innerHTML = `
        <h2>Ваши результаты</h2>
        <div id="results">
            <p><strong>Калорийность:</strong> ${results["Калорийность"]} ккал</p>
            <p><strong>Белки:</strong> ${results["Белки (г)"]} г</p>
            <p><strong>Жиры:</strong> ${results["Жиры (г)"]} г</p>
            <p><strong>Углеводы:</strong> ${results["Углеводы (г)"]} г</p>
            <p><strong>ИМТ:</strong> ${results["ИМТ"]}</p>
            <p><strong>Рекомендуемое потребление воды:</strong> ${results["Рекомендуемое потребление воды (л)"]} л</p>
        </div>
        <button id="registerBtn" class="register-btn">Зарегистрироваться</button>
    `;

    document.getElementById("registerBtn").addEventListener("click", showRegisterForm);
}

// Функция отображения формы регистрации
function showRegisterForm() {
    console.log("Переход на форму регистрации...");

    const main = document.getElementById("quiz-container");
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

// Функция регистрации пользователя
async function registerUser(event) {
    event.preventDefault();

    const fullname = document.getElementById("fullname").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;

    if (password !== confirmPassword) {
        alert("Пароли не совпадают!");
        return;
    }

    try {
        const response = await fetch("/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ fullname, email, password, confirm_password: confirmPassword })
        });

        if (!response.ok) throw new Error("Ошибка регистрации");

        alert("Регистрация успешна! Войдите в систему.");
        window.location.href = "/login";
    } catch (error) {
        console.error("Ошибка регистрации:", error);
    }
}

export { processResults };
