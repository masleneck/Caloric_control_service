export let questions = [];

export async function loadQuestions() {
    try {
        const response = await fetch('/test');  
        if (!response.ok) {
            throw new Error('Ошибка загрузки вопросов');
        }
        questions = await response.json();  
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

