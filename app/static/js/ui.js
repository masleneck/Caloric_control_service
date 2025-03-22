import { answers } from "./navigation.js"; // Импортируем answers

// Рендер вопроса
export function renderQuestion(questionData, answers) {
    const container = document.getElementById("question-container");
    container.innerHTML = "";

    const questionTitle = document.createElement("div");
    questionTitle.classList.add("question");
    questionTitle.innerText = questionData.text;
    container.appendChild(questionTitle);

    if (questionData.type === "options") {
        const optionsContainer = document.createElement("div");
        optionsContainer.classList.add("options");

        questionData.options.forEach(option => {
            const div = document.createElement("div");
            div.classList.add("option");
            div.innerText = option;
            div.setAttribute("data-question-name", questionData.name);

            // Передаём answers в selectOption
            div.onclick = () => selectOption(div, option, questionData.name, answers);

            if (answers[questionData.name] === option) {
                div.classList.add("selected");
            }

            optionsContainer.appendChild(div);
        });

        container.appendChild(optionsContainer);
    } else if (questionData.type === "input") {
        const input = document.createElement("input");
        input.type = "text";
        input.placeholder = questionData.placeholder || "";
        input.value = answers[questionData.name] || "";

        input.oninput = () => {
            answers[questionData.name] = input.value;
            updateNextButton(input.value);
        };

        container.appendChild(input);
    }
}

// Обновление кнопки "Далее"
export function updateNextButton(value) {
    const nextBtn = document.getElementById("nextBtn");
    nextBtn.disabled = !value;
    nextBtn.classList.toggle("active", !!value);
}

// Сохраняем ответ и активируем кнопку "Далее"
export function selectOption(element, value, questionName, answers) {
    console.log(`Выбран вариант: ${value} для вопроса "${questionName}"`);

    // Убираем выделение только у текущего вопроса
    document.querySelectorAll(`[data-question-name="${questionName}"]`).forEach(opt => opt.classList.remove("selected"));

    // Добавляем выделение выбранному варианту
    element.classList.add("selected");

    // Сохраняем ответ в answers
    answers[questionName] = value;
    console.log("Текущие сохранённые ответы:", answers);

    // Активируем кнопку "Далее"
    document.getElementById("nextBtn").disabled = false;
    document.getElementById("nextBtn").classList.add("active");
}
