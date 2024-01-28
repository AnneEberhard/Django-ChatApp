const activeUser = document.currentScript.getAttribute('data-username');
const csrfToken = document.currentScript.getAttribute('data-csrf-token');

async function sendMessage() {
    let fd = new FormData();
    let token = csrfToken;
    let user = activeUser;
    fd.append("textmessage", messageField.value);
    fd.append("csrfmiddlewaretoken", token);
    try {
      renderSendingMessage(messageField.value, user);
      let response = await fetch("/chat/", {
        method: "POST",
        body: fd,
      });
      let jsonText = await response.json();
      let json = JSON.parse(jsonText);
      renderSentMessage(json['fields']['text'], json['fields']['author'], json['fields']['created_at']);
    } catch (e) {
      console.log("Error:", e);
      renderMessageNotSent(messageField.value, user);
    }
  }

  function getCurrentFormattedDate() {
    const options = { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric' 
    };
    const currentDate = new Date();
    const formattedDate = currentDate.toLocaleDateString('en-US', options);
    const monthWithDot = formattedDate.replace(/^(\w+)( \d+, \d+)$/, '$1.$2');
    return monthWithDot;
  }


  function renderSendingMessage(newMessageText, user) {
    const formattedDate = getCurrentFormattedDate();
    messageContainer.innerHTML += `
      <div id="deleteMessage">
        <span class="colorGrey">[${formattedDate}] </span>${user}: <i class="colorGrey">${newMessageText}</i>
      </div>`;
  }

  function renderSentMessage(newMessageText, user, createdAt) {
    const formattedDate = getCurrentFormattedDate(new Date(createdAt));
    document.getElementById('deleteMessage').remove();
    messageContainer.innerHTML += `
    <div>
    <span class="colorGrey">[${formattedDate}] </span>${user}: <i>${newMessageText}</i>
    </div>`;
    messageField.value = '';
  }

  function renderMessageNotSent(newMessageText, user) {
    const formattedDate = getCurrentFormattedDate();
    document.getElementById('deleteMessage').remove();
    messageContainer.innerHTML += `
    <div>
    <span class="colorGrey">[${formattedDate}] </span>${user}: <i class="colorRed">${newMessageText} (Message not sent)</i>
    </div>`;
  }


  async function handleLogin() {
    let username = document.getElementById('username').value;  
    let password = document.getElementById('password').value;  
    let fd = new FormData();
    let token = csrfToken;
    fd.append("username", username);
    fd.append("password", password);
    fd.append("csrfmiddlewaretoken", token);
    disableFields();
    try {
      let response = await fetch("/login/", {
        method: "POST",
        body: fd,
      });
      let json = await response.json();
      if (json.success) {
        window.location.href = json.redirect; 
      } else {
        loginFailed();
      }
    } catch (e) {
      console.log("Error:", e);
    }
    enableFields();
  }


  function disableFields() {
    document.getElementById('username').disabled = true;
    document.getElementById('password').disabled = true;
    document.getElementById('username').classList.add('disabled');
    document.getElementById('password').classList.add('disabled');
  }

  function enableFields() {
    document.getElementById('username').disabled = false;
    document.getElementById('password').disabled = false;
    document.getElementById('username').classList.remove('disabled')
    document.getElementById('password').classList.remove('disabled')
  }

  function loginFailed() {
    document.getElementById('errorMessage').style.display = 'block';
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
  }