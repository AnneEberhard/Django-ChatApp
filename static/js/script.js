const activeUser = document.currentScript.getAttribute('data-username');
const csrfToken = document.currentScript.getAttribute('data-csrf-token');

async function sendMessage() {
    let fd = new FormData();
    let token = csrfToken;
    let user = activeUser;
   //let token = "{{ csrf_token}}";
   //let user = '{{ request.user.first_name }}';
    fd.append("textmessage", messageField.value);
    fd.append("csrfmiddlewaretoken", token);
    try {
      renderSendingMessage(messageField.value, user);
      await fetch("/chat/", {
        method: "POST",
        body: fd,
      });
      renderSentMessage(messageField.value, user);
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

  function renderSentMessage(newMessageText, user) {
    const formattedDate = getCurrentFormattedDate();
    document.getElementById('deleteMessage').remove();
    messageContainer.innerHTML += `
    <div id="deleteMessage">
    <span class="colorGrey">[${formattedDate}] </span>${user}: <i>${newMessageText}</i>
    </div>`;
  }

  function renderMessageNotSent(newMessageText, user) {
    const formattedDate = getCurrentFormattedDate();
    document.getElementById('deleteMessage').remove();
    messageContainer.innerHTML += `
    <div id="deleteMessage">
    <span class="colorGrey">[${formattedDate}] </span>${user}: <i class="colorRed">${newMessageText}, Message not sent</i>
    </div>`;
  }