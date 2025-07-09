const openChatBtn = document.getElementById("openChatBtn"); 
const chatWindow = document.getElementById("chatWindow");
const closeChatBtn = document.getElementById("closeChatBtn");
const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatform");
const messageInput = document.getElementById("messageInput")

openChatBtn?.addEventListener('click', () => {
    chatWindow?.classList.remove("hidden");
}) ;  

closeChatBtn?.addEventListener('click', () => {
    chatWindow?.classList.add("hidden");
})

function appendMessage(sender, message){
// const appendMessage = (sender, message) => {
    // create new div
    const msgDiv = document.createElement("div");
    // and give it some content
    msgDiv.className = sender === "user"? "text-right" : "text-left";
    // add style to the newly created div
    msgDiv.innerHTML = `
        <span class="badge ${sender === "user" ? "badge-primary" : "badge-accent"}">${sender}</span>
        <div class="chat-bubble">${message}</div>
    `;
    // add the newly created div and its content to the DOM
    chatMessages.appendChild(msgDiv);
    // Scroll this chat container all the way to the bottom so the latest message is visible 
    // when a message is added for smooth user experience
    chatMessages.scrollTop = chatMessages.scrollHeight;
} 

chatForm.onsubmit = async (e) => {
    e.preventDefault();
    const message = messageInput.value.trim();
    console.log("User Message:", message)
    if(!message) return;

    appendMessage("user", message);
    messageInput.value = "";

    try{
        const response = await fetch("/bot/chat/", 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ message })
        })
        
        const data = await response.json();
        console.log("Data:", data)
        appendMessage("bot", data.response);
    } catch (err) {
        console.log("bot:", err.message);
        appendMessage("bot", "Failed to respond.");
    }
};

function getCookie(name) {
    let cookieValue = null;
    if(document.cookie && document.cookie !== ""){
        const cookies = document.cookie.split(";");
        for(let cookie of cookies){
            cookie = cookie.trim();
            if(cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};