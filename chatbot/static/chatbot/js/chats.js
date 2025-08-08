const openChatBtn = document.getElementById("openChatBtn"); 
const chatWindow = document.getElementById("chatWindow");
const closeChatBtn = document.getElementById("closeChatBtn");
const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatform");
const messageInput = document.getElementById("messageInput");
const fileInput = document.getElementById("fileInput");

openChatBtn?.addEventListener('click', () => {
    chatWindow?.classList.remove("hidden");
}) ;  

closeChatBtn?.addEventListener('click', () => {
    chatWindow?.classList.add("hidden");
})

function appendMessage(sender, message){
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
    // Scroll chat container to the bottom so the latest message is visible 
    chatMessages.scrollTop = chatMessages.scrollHeight;
} 

// Scrollbar trigger logic on user input
let scrollbarTriggered = false;

messageInput?.addEventListener("input", () => {
    if (scrollbarTriggered) {
        const dummyDiv = document.createElement("div");
        dummyDiv.style.height = "320px";
        dummyDiv.style.visibility = "hidden";
        chatMessages.appendChild(dummyDiv);

        chatMessages.scrollTop = chatMessages.scrollHeight;

        scrollbarTriggered = true;
    }
});

// Handle chat form submission (JSON to chat API) 
chatForm.onsubmit = async (e) => {
    e.preventDefault();
    const message = messageInput.value.trim();
    console.log("User Message:", message)
    if(!message) return;

    appendMessage("user", message);
    messageInput.value = "";

    let option = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ message })
    };
    
    try{
        const response = await fetch("/bot/api/chat/", option);
    
        const data = await response.json();
        console.log("Data:", data)
        appendMessage("bot", data.response);
    } catch (err) {
        console.log("bot:", err.message);
        appendMessage("bot", "Failed to respond.");
    }
};

// Handle file upload (FormData to upload API)
fileInput.addEventListener("change", async function() {
    const file = this.file[0];
    if (file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("/bot/api/upload", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: formData,
        });

        const data = await res.json();

        if (data.status === "success") {
            appendMessage("bot", `File uploaded: ${file.name}`);
        } else {
            appendMessage("bot", `Upload failed: ${data.message || "Unknown error"}`);
            console.error("Upload error:", error);
        } 
    } catch (error) {
        appendMessage("bot", "Upload error");
        console.error("Upload error:", error);
    } finally {
        fileInput.value = "";
    }
})

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