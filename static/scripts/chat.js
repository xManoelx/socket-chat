// chat.js - Script da página de chat específico

// Pegar dados do template (definidos no HTML)
const username = window.chatConfig.username;
const room = window.chatConfig.room;

console.log('DEBUG Chat JS - Username:', username);
console.log('DEBUG Chat JS - Room:', room);

// Conectar ao SocketIO
var socket = io.connect('http://' + document.domain + ':' + location.port);

console.log('DEBUG Chat JS - Socket conectando...');

// Quando conectar, entrar na sala
socket.on('connect', function() {
    console.log('DEBUG Chat JS - Socket conectado, entrando na sala...');
    socket.emit('join_room', {
        'username': username,
        'room': room
    });
});

// Quando sair da página, deixar a sala
window.addEventListener('beforeunload', function() {
    console.log('DEBUG Chat JS - Saindo da sala...');
    socket.emit('leave_room', {
        'username': username,
        'room': room
    });
});

// Carregar contagem inicial de usuários na sala
fetch(`/api/users/${room}`)
    .then(response => response.json())
    .then(data => {
        console.log('DEBUG Chat JS - Usuários na sala:', data);
        const roomUsersCount = document.getElementById('room-users-count');
        if (roomUsersCount) {
            roomUsersCount.textContent = data.count;
        }
    })
    .catch(error => console.error('Erro ao carregar usuários da sala:', error));

// Receber mensagens da sala
socket.on('message', function(data) {
    console.log('DEBUG Chat JS - Mensagem recebida:', data);
    if (data.room === room) {
        const messagesDiv = document.getElementById('messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';
        
        const time = data.timestamp || new Date().toLocaleTimeString('pt-BR', {
            hour: '2-digit', 
            minute: '2-digit'
        });
        
        messageDiv.innerHTML = `
            <div class="message-header">
                <span class="message-username">${data.username}</span>
                <span class="message-time">${time}</span>
            </div>
            <div class="message-text">${data.message}</div>
        `;
        
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        console.log('DEBUG Chat JS - Mensagem adicionada ao DOM');
    }
});

// Usuário entrou na sala
socket.on('user_joined', function(data) {
    console.log('DEBUG Chat JS - Usuário entrou:', data);
    if (data.room === room) {
        const roomUsersCount = document.getElementById('room-users-count');
        if (roomUsersCount) {
            roomUsersCount.textContent = data.users_in_room.length;
        }
        
        // Só mostrar mensagem se não for o próprio usuário
        if (data.username !== username) {
            const messagesDiv = document.getElementById('messages');
            const systemMessage = document.createElement('div');
            systemMessage.className = 'system-message';
            systemMessage.textContent = `${data.username} entrou na sala`;
            messagesDiv.appendChild(systemMessage);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
    }
});

// Usuário saiu da sala
socket.on('user_left', function(data) {
    console.log('DEBUG Chat JS - Usuário saiu:', data);
    if (data.room === room) {
        const roomUsersCount = document.getElementById('room-users-count');
        if (roomUsersCount) {
            roomUsersCount.textContent = data.users_in_room.length;
        }
        
        const messagesDiv = document.getElementById('messages');
        const systemMessage = document.createElement('div');
        systemMessage.className = 'system-message';
        systemMessage.textContent = `${data.username} saiu da sala`;
        messagesDiv.appendChild(systemMessage);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
});

// Enviar mensagem
document.getElementById('messageForm').onsubmit = function(e) {
    console.log('DEBUG Chat JS - Formulário de mensagem enviado');
    e.preventDefault();
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    console.log('DEBUG Chat JS - Mensagem para enviar:', message);
    
    if (message) {
        const messageData = {
            'username': username,
            'message': message,
            'room': room
        };
        console.log('DEBUG Chat JS - Enviando dados:', messageData);
        
        socket.emit('message', messageData);
        messageInput.value = '';
        console.log('DEBUG Chat JS - Mensagem enviada, campo limpo');
    } else {
        console.log('DEBUG Chat JS - Mensagem vazia, não enviando');
    }
};