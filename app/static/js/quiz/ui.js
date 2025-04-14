// Отрисовка текущего вопроса
export function renderQuestion(questionData, answers) {
    const container = document.getElementById("question-container");
    container.innerHTML = "";

    const questionTitle = document.createElement("div");
    questionTitle.classList.add("question");
    questionTitle.innerText = questionData.text;

    // Добавление tooltip
    if (questionData.name === "bad_habits") {
        const tooltip = createTooltip("Например: курение, алкоголь, переедание", "right");
        questionTitle.appendChild(tooltip);
    }
    
    if (questionData.name === "water_intake") {
        const tooltip = createTooltip("1 стакан ≈ 250 мл", "bottom");
        questionTitle.appendChild(tooltip);
    }    

    container.appendChild(questionTitle);

    if (questionData.type === "options") {
        const optionsContainer = document.createElement("div");
        optionsContainer.classList.add("options");

        questionData.options.forEach(option => {
            const div = document.createElement("div");
            div.classList.add("option");
            div.innerText = option;
            div.setAttribute("data-question-name", questionData.name);

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

        if (questionData.name === "birthday_date") {
            input.placeholder = "Выберите дату рождения";
            input.readOnly = true;

            container.appendChild(input);

            flatpickr(input, {
                locale: "ru",
                dateFormat: "Y-m-d",
                maxDate: "today",
                defaultDate: answers[questionData.name] || null,
                onChange: function (selectedDates, dateStr) {
                    answers[questionData.name] = dateStr;
                    updateNextButton(dateStr);
                }
            });
            return;
        } else if (questionData.name === "height") {
            input.placeholder = "Указать рост в см";
        } else if (questionData.name === "weight") {
            input.placeholder = "Указать вес в кг";
        }

        input.value = answers[questionData.name] || "";

        input.oninput = () => {
            answers[questionData.name] = input.value;
            updateNextButton(input.value);
        };

        container.appendChild(input);
    }
}

// tooltip генератор
function createTooltip(text, position = "bottom") {
    const wrapper = document.createElement("span");
    wrapper.classList.add("tooltip-wrapper", `tooltip-${position}`);

    const icon = document.createElement("i");
    icon.classList.add("ri-question-line", "tooltip-icon");

    const tooltipText = document.createElement("span");
    tooltipText.classList.add("tooltip-text");
    tooltipText.innerText = text;

    wrapper.appendChild(icon);
    wrapper.appendChild(tooltipText);
    return wrapper;
}

// Обновление состояния кнопки "Далее"
export function updateNextButton(value) {
    const nextBtn = document.getElementById("nextBtn");
    nextBtn.disabled = !value;
    nextBtn.classList.toggle("active", !!value);
}

// Выбор опции
export function selectOption(element, value, questionName, answers) {
    console.log(`Выбран вариант: ${value} для вопроса "${questionName}"`);

    document.querySelectorAll(`[data-question-name="${questionName}"]`).forEach(opt => {
        opt.classList.remove("selected");
    });

    element.classList.add("selected");

    answers[questionName] = value;
    console.log("Текущие сохранённые ответы:", answers);

    const nextBtn = document.getElementById("nextBtn");
    nextBtn.disabled = false;
    nextBtn.classList.add("active");
}
