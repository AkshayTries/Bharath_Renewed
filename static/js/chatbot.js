let currentQuestion = 0;
let userResponses = [];

function toggleChat() {
    const chatContainer = document.getElementById("chat-container");
    chatContainer.style.display = chatContainer.style.display === "none" || chatContainer.style.display === "" ? "block" : "none";
}

function sendMessage(userMessage) {
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<div class="user-message">${userMessage}</div>`;

    fetch('/respond', {  // Send user input to Flask backend
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<div class="bot-message">${data.response}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error("Error:", error));
}

function askQuestion() {
    const buttonContainer = document.getElementById("button-container");
    buttonContainer.innerHTML = "";

    const inputField = document.createElement("input");
    inputField.setAttribute("type", "text");
    inputField.setAttribute("id", "user-input");
    inputField.classList.add("form-control", "m-2");

    const sendButton = document.createElement("button");
    sendButton.innerText = "Send";
    sendButton.classList.add("btn", "btn-success", "m-2");
    sendButton.onclick = () => {
        const userInput = document.getElementById("user-input").value;
        if (userInput.trim() !== "") {
            sendMessage(userInput);
            document.getElementById("user-input").value = "";
        }
    };

    buttonContainer.appendChild(inputField);
    buttonContainer.appendChild(sendButton);
}

document.addEventListener("DOMContentLoaded", () => {
    askQuestion();
});
