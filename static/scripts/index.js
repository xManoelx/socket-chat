// index.js - Script da landing page

// Carregar número de usuários online
function loadOnlineUsers() {
    fetch('/api/users')
        .then(response => response.json())
        .then(data => {
            const onlineUsersElement = document.getElementById('online-users');
            if (onlineUsersElement) {
                onlineUsersElement.textContent = data.count_total;
            }
        })
        .catch(() => {
            const onlineUsersElement = document.getElementById('online-users');
            if (onlineUsersElement) {
                onlineUsersElement.textContent = '0';
            }
        });
}

loadOnlineUsers();
setInterval(loadOnlineUsers, 30000); // Atualizar a cada 30 segundos

// Animação das mensagens do preview
const messages = [
    { user: 'João', text: 'Olá pessoal!' },
    { user: 'Maria', text: 'Como vocês estão?' },
    { user: 'Pedro', text: 'Tudo bem! Loving this chat!' },
    { user: 'Ana', text: 'Alguém quer jogar?' },
    { user: 'Carlos', text: 'Vou estudar Python hoje' }
];

let currentMessage = 0;

function rotateMessages() {
    const messagesContainer = document.querySelector('.preview-messages');
    if (!messagesContainer) return;
    
    messagesContainer.innerHTML = '';
    
    for (let i = 0; i < 3; i++) {
        const msgIndex = (currentMessage + i) % messages.length;
        const msg = messages[msgIndex];
        
        const msgDiv = document.createElement('div');
        msgDiv.className = 'preview-message';
        msgDiv.innerHTML = `
            <span class="msg-user">${msg.user}:</span>
            <span class="msg-text">${msg.text}</span>
        `;
        messagesContainer.appendChild(msgDiv);
    }
    
    currentMessage = (currentMessage + 1) % messages.length;
}

// Rotacionar mensagens a cada 3 segundos
setInterval(rotateMessages, 3000);