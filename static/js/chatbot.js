let currentQuestion = 0;
let userResponses = [];

const questions = [
    { question: "What would you like assistance with?", options: ["Health", "Education"] },
    { question: "Are you below the poverty line (BPL)?", options: ["Yes", "No"] },
    { question: "What is your caste category?", options: ["OBC", "SC/ST", "General"] },
    { question: "Would you like to explore schemes or charities?", options: ["Schemes", "Charities"] }
];

function toggleChat() {
    const chatContainer = document.getElementById("chat-container");
    chatContainer.style.display = chatContainer.style.display === "none" || chatContainer.style.display === "" ? "block" : "none";
    if (chatContainer.style.display === "block" && currentQuestion === 0) {
        askQuestion(currentQuestion);
    }
}

function askQuestion(questionIndex) {
    const chatBox = document.getElementById("chat-box");
    if (questionIndex < questions.length) {
        chatBox.innerHTML += `<div class="bot-message">${questions[questionIndex].question}</div>`;
        const buttonContainer = document.getElementById("button-container");
        buttonContainer.innerHTML = "";
        questions[questionIndex].options.forEach(option => {
            const button = document.createElement("button");
            button.classList.add("btn", "btn-info", "m-2");
            button.innerHTML = option;
            button.onclick = () => handleResponse(option);
            buttonContainer.appendChild(button);
        });
        chatBox.scrollTop = chatBox.scrollHeight;
    } else {
        evaluateResponses();
    }
}

function handleResponse(response) {
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<div class="user-message">${response}</div>`;
    userResponses.push(response);
    currentQuestion++;
    setTimeout(() => askQuestion(currentQuestion), 500);
}

function evaluateResponses() {
    const chatBox = document.getElementById("chat-box");
    const [category, bplStatus, casteCategory, preference] = userResponses;
    let result = "";

    if (category.toLowerCase() === "health" && bplStatus.toLowerCase() === "yes" && preference.toLowerCase() === "schemes") {
        result = "You may qualify for Ayushman Bharat scheme. For more details, please visit our health section.";
    } else if (category.toLowerCase() === "education" && casteCategory.toLowerCase() === "obc" && preference.toLowerCase() === "schemes") {
        result = "You may qualify for education schemes under OBC. Check out our education page for more.";
    } else if (category.toLowerCase() === "education" && casteCategory.toLowerCase() === "sc/st" && preference.toLowerCase() === "schemes") {
        result = "You may qualify for education schemes under SC/ST. Please check out our education section.";
    } else {
        result = `Sorry, I couldn't find a relevant scheme or charity for your situation. Please visit our <a href="contactus.html">Contact Us</a> page for more assistance.`;
    }

    chatBox.innerHTML += `<div class="bot-message">${result}</div>`;
    document.getElementById("button-container").innerHTML = "";
    chatBox.scrollTop = chatBox.scrollHeight;
}