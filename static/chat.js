document.addEventListener("DOMContentLoaded", function() {
    // Display greeting message when the page loads
    var chatLog = document.getElementById("chat-log");
    var greetingMessage = document.createElement("div");
    greetingMessage.className = "bot-message";
    chatLog.appendChild(greetingMessage);

    // Typing effect for the greeting message
    var greetingText = "Hello! I'm your EnglishFirm chatbot. How can I assist you today?";
    typeEffect(greetingMessage, greetingText);

    // Scroll to the bottom of the chat log after greeting message
    scrollToBottom();
});

document.getElementById("chat-form").addEventListener("submit", function(event) {
    event.preventDefault();

    var userInput = document.getElementById("user-input").value;
    var chatLog = document.getElementById("chat-log");

    // Add user input to the chat log
    var userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = userInput;
    chatLog.appendChild(userMessage);

    // Scroll to the bottom of the chat log after user input
    scrollToBottom();

    // Send the user input to the server
    fetch("/get_response", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "user_input=" + encodeURIComponent(userInput)
    })
    .then(response => response.json())
    .then(data => {
        // Create bot message element
        var botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        chatLog.appendChild(botMessage);

        // Typing effect for bot response
        typeEffect(botMessage, data.response);

        // Scroll to the bottom of the chat log after bot response
        scrollToBottom();
    });

    // Clear the input field
    document.getElementById("user-input").value = "";
});

// Function for typing effect
function typeEffect(element, text) {
    var index = 0;
    var speed = 5; // Typing speed in milliseconds

    function type() {
        if (index < text.length) {
            element.textContent += text.charAt(index);
            index++;
            setTimeout(type, speed);
        }
    }

    type(); // Start typing
}

// Function to automatically scroll to the bottom of the chat log
function scrollToBottom() {
    var chatLog = document.getElementById("chat-log");
    chatLog.scrollTop = chatLog.scrollHeight;
}
