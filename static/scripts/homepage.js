// homepage.js - Script da página homepage

const username = document.querySelector('#current-user').textContent || 
                 document.querySelector('.user-info span:first-child').textContent.replace('Usuário: ', '');

// Conectar ao SocketIO
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Quando conectar, notificar que o usuário está online na homepage
socket.on('connect', function() {
    socket.emit('user_online', {'username': username});
});

// Quando desconectar (fechar aba/navegador)
window.addEventListener('beforeunload', function() {
    socket.emit('user_offline', {'username': username});
});

// Função para carregar usuários online
function loadOnlineUsers() {
    fetch('/api/users')
        .then(response => response.json())
        .then(data => {
            // Atualizar total de usuários (apenas o número)
            const totalCountElement = document.getElementById('total-count');
            if (totalCountElement) {
                totalCountElement.textContent = data.count_total;
            }
            
            // Atualizar contadores por sala
            Object.entries(data.count_by_room).forEach(([room, count]) => {
                const countElement = document.getElementById(room + '-count');
                if (countElement) {
                    countElement.textContent = `${count} usuários online`;
                }
            });
        })
        .catch(error => console.error('Erro ao carregar usuários:', error));
}

// Escutar atualizações de usuários em tempo real
socket.on('users_updated', function(data) {
    const totalCountElement = document.getElementById('total-count');
    if (totalCountElement) {
        totalCountElement.textContent = data.count_total;
    }
    
    Object.entries(data.count_by_room).forEach(([room, count]) => {
        const countElement = document.getElementById(room + '-count');
        if (countElement) {
            countElement.textContent = `${count} usuários online`;
        }
    });
});

// Carregar usuários na inicialização
loadOnlineUsers();

// Atualizar a cada 30 segundos (backup)
setInterval(loadOnlineUsers, 30000);