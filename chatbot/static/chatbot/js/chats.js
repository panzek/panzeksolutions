const openChatBtn = document.getElementById("openChatBtn"); 
const chatWindow = document.getElementById("chatWindow");
const closeChatBtn = document.getElementById("closeChatBtn");
const chatMessages = document.getElementById("chatMessages");
const chatform = document.getElementById("chatform");
const messageInput = document.getElementById("messageInput")

openChatBtn?.addEventListener('click', () => {
    chatWindow?.classList.remove("hidden");
}) ;  

closeChatBtn?.addEventListener('click', () => {
    chatWindow?.classList.add("hidden");
})