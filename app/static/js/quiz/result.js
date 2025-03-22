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
