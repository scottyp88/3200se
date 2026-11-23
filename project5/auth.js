const apiUrlUsers = "http://127.0.0.1:5001/users";
const apiUrlLogin = "http://127.0.0.1:5001/login";

const ucf = document.querySelector('#user-creation-form');
ucf.addEventListener('submit', function(e) {
    e.preventDefault()
    const fname = document.querySelector('#user-name').value;
    const lname = document.querySelector('#user-lname').value;
    const email = document.querySelector('#user-email').value;
    const pswrd = document.querySelector('#user-pass').value;
    createUser(fname, lname, email, pswrd);
});

const ulf = document.querySelector('#user-login-form');
ulf.addEventListener('submit', function(e) {
    e.preventDefault()
    const email = document.querySelector('#login-user-email').value;
    const pswrd = document.querySelector('#login-user-pass').value;
    loginUser(email, pswrd);
    
});

async function createUser(fname, lname, email, pswrd) {
    try {
        const response = await fetch(apiUrlUsers, {method: "POST", headers: { "Content-Type": "application/json"}, body: JSON.stringify({ fname, lname, email, pswrd})});
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error);
        }
        alert("Account created successfully!");
        ucf.reset();
        
        
    }
    catch (error){
        alert(error.message);
    }    
}

async function loginUser(email, pswrd) {
    try {
        const response = await fetch(apiUrlLogin, {method: "POST", headers: { "Content-Type": "application/json"},credentials: "include", body: JSON.stringify({email, pswrd})});
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error);
        }
        window.location.href = "rifles.html";
    }
    catch (error){
        alert(error.message);
    }
}
