document.getElementById("user-input").addEventListener("keydown", function(event) {
    // Check if Enter key (key code 13) is pressed
    if (event.key === "Enter") {
        event.preventDefault();  // Prevent the default action (like a line break)
        sendMessage();           // Call the sendMessage function
    }
});

function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    const chatWindow = document.getElementById("chat-window");
    
    // Display the user's message
    const userMessageDiv = document.createElement("div");
    userMessageDiv.classList.add("message", "user-message");
    userMessageDiv.innerHTML = `<div class="bubble">${userInput}</div>`;
    chatWindow.appendChild(userMessageDiv);
    
    // Scroll to the bottom of the chat window
    chatWindow.scrollTop = chatWindow.scrollHeight;

    document.getElementById("user-input").value = "";

    // Send the user's message to the backend (AI Assistant)
    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Display the AI's response
        const aiMessageDiv = document.createElement("div");
        aiMessageDiv.classList.add("message", "ai-message");
        aiMessageDiv.innerHTML = `<div class="bubble">${data.response}</div>`;
        chatWindow.appendChild(aiMessageDiv);
        
        // Scroll to the bottom of the chat window
        chatWindow.scrollTop = chatWindow.scrollHeight;
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener("keydown", function(event) {
    // Ensure that the input box is focused when a key is pressed
    document.getElementById("user-input").focus();
});
