const apiUrl = "http://127.0.0.1:5001/messages";
async function loadMessages(){
    const response = await fetch(apiUrl);
    const messages = await response.json();
    console.log(messages);


    const list = document.getElementById("message-list");
    list.replaceChildren();
    for (const message of messages) {
        const item = document.createElement("li");
        item.textContent = message;
        list.appendChild(item);
    }
}
loadMessages();
const form = document.getElementById("message-form");
form.addEventListener("submit", async function(event){
    event.preventDefault();
    const message = document.getElementById("message").value;
    const response = await fetch(apiUrl, {
        method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({ message: message})
    });
    if (response.ok) {
        await loadMessages();
    document.getElementById("message").value = "";
    } else {
        alert("Your message could not be saved.");
    }
}); 