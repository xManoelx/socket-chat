// rooms.js - Script da página de salas

// Carregar estatísticas em tempo real
function loadRoomStats() {
    fetch('/api/users')
        .then(response => response.json())
        .then(data => {
            // Total de usuários online
            const totalOnlineElement = document.getElementById('total-online');
            if (totalOnlineElement) {
                totalOnlineElement.textContent = data.count_total;
            }
            
            // Usuários por sala
            Object.entries(data.count_by_room).forEach(([room, count]) => {
                const element = document.getElementById(`users-${room}`);
                if (element) {
                    element.textContent = count;
                }
                
                // Atualizar indicador de atividade
                const activityDot = document.getElementById(`activity-${room}`);
                const activityText = document.getElementById(`activity-text-${room}`);
                
                if (activityDot && activityText) {
                    if (count > 0) {
                        activityDot.className = 'activity-dot active';
                        activityText.textContent = 'Ativa';
                    } else {
                        activityDot.className = 'activity-dot inactive';
                        activityText.textContent = 'Inativa';
                    }
                }
            });
        })
        .catch(error => console.error('Erro ao carregar estatísticas:', error));
}

// Mostrar detalhes da sala
function showRoomDetails(roomName, displayName) {
    const modalTitle = document.getElementById('modalTitle');
    const roomModal = document.getElementById('roomModal');
    
    if (modalTitle) {
        modalTitle.textContent = `Detalhes - ${displayName}`;
    }
    
    if (roomModal) {
        roomModal.style.display = 'block';
    }
    
    // Carregar dados específicos da sala
    fetch(`/api/users/${roomName}`)
        .then(response => response.json())
        .then(data => {
            const modalUsers = document.getElementById('modalUsers');
            const modalActivity = document.getElementById('modalActivity');
            const modalMessages = document.getElementById('modalMessages');
            
            if (modalUsers) {
                modalUsers.textContent = data.count;
            }
            
            if (modalActivity) {
                modalActivity.textContent = new Date().toLocaleString('pt-BR');
            }
            
            if (modalMessages) {
                modalMessages.innerHTML = 
                    data.count > 0 ? 'Sala ativa com conversas em andamento' : 'Nenhuma atividade recente';
            }
        });
}

// Fechar modal
function closeModal() {
    const roomModal = document.getElementById('roomModal');
    if (roomModal) {
        roomModal.style.display = 'none';
    }
}

// Confirmar logout
function confirmLogout() {
    const logoutModal = document.getElementById('logoutModal');
    if (logoutModal) {
        logoutModal.style.display = 'block';
    }
}

function closeLogoutModal() {
    const logoutModal = document.getElementById('logoutModal');
    if (logoutModal) {
        logoutModal.style.display = 'none';
    }
}

function logout() {
    window.location.href = '/logout';
}

// Fechar modal clicando fora
window.onclick = function(event) {
    const roomModal = document.getElementById('roomModal');
    const logoutModal = document.getElementById('logoutModal');
    
    if (event.target === roomModal) {
        closeModal();
    }
    if (event.target === logoutModal) {
        closeLogoutModal();
    }
}

// Inicializar
loadRoomStats();
setInterval(loadRoomStats, 10000); // Atualizar a cada 10 segundos

// Simular mensagens do dia
const totalMessagesElement = document.getElementById('total-messages');
if (totalMessagesElement) {
    totalMessagesElement.textContent = Math.floor(Math.random() * 200) + 50;
}