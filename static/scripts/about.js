// about.js - Script da página sobre

// Função para carregar usuários online
function loadOnlineUsers() {
    fetch('/api/users')
        .then(response => response.json())
        .then(data => {
            const onlineNowElement = document.getElementById('online-now');
            if (onlineNowElement) {
                onlineNowElement.textContent = data.count_total;
            }
        })
        .catch(() => {
            const onlineNowElement = document.getElementById('online-now');
            if (onlineNowElement) {
                onlineNowElement.textContent = '0';
            }
        });
}

// Carregar na inicialização
loadOnlineUsers();

// Atualizar a cada 10 segundos
setInterval(loadOnlineUsers, 10000);

// Simular outras estatísticas (você pode criar APIs reais para isso)
const totalUsersElement = document.getElementById('total-users');
const totalMessagesElement = document.getElementById('total-messages');

if (totalUsersElement) {
    totalUsersElement.textContent = Math.floor(Math.random() * 50) + 10;
}

if (totalMessagesElement) {
    totalMessagesElement.textContent = Math.floor(Math.random() * 1000) + 100;
}