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
                minDate: new Date().getFullYear() - 100 + "-01-01",
                defaultDate: answers[questionData.name] || null,
                onChange: function (selectedDates, dateStr) {
                    const today = new Date();
                    const birthDate = new Date(dateStr);
                    const age = today.getFullYear() - birthDate.getFullYear();
                    const monthDiff = today.getMonth() - birthDate.getMonth();
                    const isTooYoung = age < 14 || (age === 14 && monthDiff < 0) || (age === 14 && monthDiff === 0 && today.getDate() < birthDate.getDate());
            
                    if (isTooYoung) {
                        alert("Минимальный возраст — 14 лет");
                        input._flatpickr.clear(); 
                        answers[questionData.name] = null;
                        updateNextButton(false);
                    } else {
                        answers[questionData.name] = dateStr;
                        updateNextButton(dateStr);
                    }
                }
            });
            return;
        }
    
        const errorDiv = document.createElement("div");
        errorDiv.classList.add("error-message");
    
        if (questionData.name === "height") {
            input.placeholder = "Указать рост в см";
            input.dataset.min = 120;
            input.dataset.max = 280;
            errorDiv.innerHTML = `<i class="ri-error-warning-line"></i> Рост должен быть от 120 до 280 см`;
        } else if (questionData.name === "weight") {
            input.placeholder = "Указать вес в кг";
            input.dataset.min = 40;
            input.dataset.max = 300;
            errorDiv.innerHTML = `<i class="ri-error-warning-line"></i> Вес должен быть от 40 до 300 кг`;
        } else if (questionData.name === "steps_per_day") {
            input.placeholder = "Шагов в день";
            input.dataset.min = 0;
            input.dataset.max = 50000;
            errorDiv.innerHTML = `<i class="ri-error-warning-line"></i> Введите число от 0 до 50000`;
        } else if (questionData.name === "sleep_hours") {
            input.placeholder = "Часов сна в день";
            input.dataset.min = 0;
            input.dataset.max = 24;
            errorDiv.innerHTML = `<i class="ri-error-warning-line"></i> Введите число от 0 до 24`;
        }
    
        errorDiv.style.display = "none";
    
        input.value = answers[questionData.name] || "";
    
        input.oninput = () => {
            const val = Number(input.value);
            const min = Number(input.dataset.min);
            const max = Number(input.dataset.max);
    
            const isValid =
                !isNaN(val) &&
                (min === undefined || val >= min) &&
                (max === undefined || val <= max);
    
            if (isValid || (!min && !max)) {
                answers[questionData.name] = input.value;
                errorDiv.style.display = "none";
            } else {
                delete answers[questionData.name];
                errorDiv.style.display = "block";
            }
    
            updateNextButton(isValid || (!min && !max));
        };
    
        container.appendChild(input);
        container.appendChild(errorDiv);
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
