document.addEventListener("DOMContentLoaded", function () {
    const chatInput = document.getElementById("user-query");
    const askButton = document.getElementById("ask-btn");
    const responseBox = document.getElementById("response-box");
    const greeting = document.getElementById("greeting");
    const researchOptions = document.querySelector(".research-options");
    const chatContainer = document.querySelector(".chat-container");
    const body = document.body;

    function sendQuery() {
        const userQuery = chatInput.value.trim();
        if (!userQuery) return;

        // Hide greeting and research buttons
        greeting.style.display = "none";
        researchOptions.style.display = "none";

        // Make background and UI elements more minimalistic after input
        body.style.background = "#121417";
        chatContainer.style.border = "none";
        chatContainer.style.background = "transparent";

        // Show user query
        responseBox.innerHTML = `<strong>You:</strong> ${userQuery}`;
        responseBox.classList.remove("hidden");

        chatInput.value = ""; // Clear input field

        // Show loading message
        responseBox.innerHTML += `<br><strong>Socrates:</strong> Thinking... ⏳`;

        fetch("/ask_gemini", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: userQuery })
        })
        .then(response => response.json())
        .then(data => {
            let responseContent = `<strong>You:</strong> ${userQuery}<br><strong>Socrates:</strong> ${data.response}`;
            if (data.steps) {
                responseContent += `<br><br><strong>Steps Executed:</strong><br>${data.steps}`;
            }
            responseBox.innerHTML = responseContent;
        })
        .catch(error => {
            responseBox.innerHTML = `<strong>You:</strong> ${userQuery}<br><strong>Socrates:</strong> Error fetching response.`;
        });
    }

    askButton.addEventListener("click", sendQuery);
    chatInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendQuery();
        }
    });
});


// create a new organisation with name as namakkal and slug as prem and a new member with name as vijay and email as vijay@gmail.com
