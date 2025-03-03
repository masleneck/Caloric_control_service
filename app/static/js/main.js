import {init, nextQuestion, prevQuestion} from "./navigation.js";

document.getElementById("nextBtn").addEventListener("click", nextQuestion);
document.getElementById("prevBtn").addEventListener("click", prevQuestion);

init();