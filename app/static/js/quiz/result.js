import { showRegisterForm } from "../auth/register.js";
import { genderMap, goalMap } from "../utils/maps.js";

// Обработка результатов
export async function processResults(answers) {
    console.log("Отправка данных для расчёта...");
    console.log("Проверка сохранённых ответов перед отправкой:", answers);

    const formattedAnswers = {
        gender: genderMap[answers["gender"]] || "UNKNOWN",
        birthday_date: answers["birthday_date"] || "",
        height: Number(answers["height"]) || 0,
        weight: Number(answers["weight"]) || 0,
        goal: goalMap[answers["goal"]] || "UNKNOWN",
        bad_habits: answers["bad_habits"] || "",
        steps_per_day: Number(answers["steps_per_day"]) || 0,
        sleep_hours: Number(answers["sleep_hours"]) || 0,
        water_intake: answers["water_intake"] || "",
        hormone_issues: answers["hormone_issues"] || ""
    };

    try {
        const response = await fetch("/questions/calculate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formattedAnswers)
        });

        if (!response.ok) throw new Error(`Ошибка расчёта: ${response.status}`);

        const results = await response.json();
        console.log("Рассчитанные данные:", results);

        await saveTestResult(formattedAnswers);
        showResults(results);
    } catch (error) {
        console.error("Ошибка при обработке результатов:", error);
    }
}

async function saveTestResult(data) {
    console.log("Сохранение результатов теста...");

    try {
        const response = await fetch("/questions/save_test_result/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error(`Ошибка сохранения: ${response.status}`);

        const responseData = await response.json();
        console.log("Тест успешно сохранён! Session ID:", responseData.session_id);
    } catch (error) {
        console.error("Ошибка при сохранении теста:", error);
    }
}

function showResults(results) {
    document.querySelector('.back-home-card')?.classList.add('hidden');
    const main = document.getElementById("quiz-container");
    main.innerHTML = `
    <div class="results-card">
        <h2 class="results-title">Ваши результаты</h2>
        <div class="results-list">
            <div class="result-item"><span>Калорийность:</span> ${results["Калорийность"]} ккал</div>
            <div class="result-item"><span>Белки:</span> ${results["Белки (г)"]} г</div>
            <div class="result-item"><span>Жиры:</span> ${results["Жиры (г)"]} г</div>
            <div class="result-item"><span>Углеводы:</span> ${results["Углеводы (г)"]} г</div>
            <div class="result-item"><span>ИМТ:</span> ${results["ИМТ"]}</div>
            <div class="result-item"><span>Вода:</span> ${results["Рекомендуемое потребление воды (л)"]} л</div>
        </div>
        <button id="registerBtn" class="register-btn">Зарегистрироваться</button>
    </div>
`;

    document.getElementById("registerBtn").addEventListener("click", () => {
        document.querySelector('.back-home-card')?.classList.add('hidden');
        showRegisterForm();
    });
}
