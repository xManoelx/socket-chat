from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, join_room, leave_room

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'  # Chave secreta para sessões

# Inicializa SocketIO com CORS habilitado
socketio = SocketIO(app, cors_allowed_origins="*")

# Lista para armazenar usuários online
online_users = []

# Dicionário para armazenar usuários por sala
users_by_room = {
    'geral': [],
    'programacao': [],
    'games': []
}

# Rota principal - Renderiza a página inicial do chat
@app.route('/')
def index():
    return render_template('pages/index.html')

# Rota homepage - Renderiza a página principal após login
@app.route('/homepage')
def homepage():
    username = request.args.get('user')
    if not username:
        return render_template('pages/login.html')  # Redireciona para login se não tiver usuário
    return render_template('pages/homepage.html', username=username)

# Rota de login - Renderiza a página de login
@app.route('/login')
def login():
    return render_template('pages/login.html')

# Rota about - Renderiza a página sobre
@app.route('/about')
def about():
    return render_template('pages/about.html')

# Rota API - Retorna lista de usuários online
@app.route('/api/users')
def api_users():
    return jsonify({
        'users_total': online_users,
        'count_total': len(online_users),
        'users_by_room': users_by_room,
        'count_by_room': {room: len(users) for room, users in users_by_room.items()}
    })

# Nova rota para API de usuários de uma sala específica
@app.route('/api/users/<sala>')
def api_users_sala(sala):
    users_in_room = users_by_room.get(sala, [])
    return jsonify({
        'sala': sala,
        'users': users_in_room,
        'count': len(users_in_room)
    })

# Rota rooms - Renderiza a página de salas de chat
@app.route('/rooms')
def rooms():
    return render_template('pages/rooms.html')

# Rota logout - Desloga o usuário
@app.route('/logout')
def logout():
    return render_template('pages/logout.html')

# Rotas para chats específicos
@app.route('/chat/<sala>')
def chat_sala(sala):
    username = request.args.get('user')
    if not username:
        return render_template('pages/login.html')
    return render_template('pages/chat.html', username=username, sala=sala)

#######################################################

@socketio.on('user_online')
def handle_user_online(data):
    username = data['username']
    
    # Adicionar à lista geral se não estiver
    if username not in online_users:
        online_users.append(username)
        print(f'{username} está online na homepage')
        
        # Notificar todos sobre a atualização
        socketio.emit('users_updated', {
            'users_total': online_users,
            'count_total': len(online_users),
            'users_by_room': users_by_room,
            'count_by_room': {room: len(users) for room, users in users_by_room.items()}
        })

@socketio.on('user_offline')
def handle_user_offline(data):
    username = data['username']
    
    # Remover da lista geral
    if username in online_users:
        online_users.remove(username)
        print(f'{username} saiu da homepage')
        
        # Remover de todas as salas também
        for room in users_by_room:
            if username in users_by_room[room]:
                users_by_room[room].remove(username)
        
        # Notificar todos sobre a atualização
        socketio.emit('users_updated', {
            'users_total': online_users,
            'count_total': len(online_users),
            'users_by_room': users_by_room,
            'count_by_room': {room: len(users) for room, users in users_by_room.items()}
        })

@socketio.on('join_room')
def handle_join_room(data):
    username = data['username']
    room = data['room']
    
    # Adicionar usuário à sala
    join_room(room)
    
    # Adicionar à lista geral se não estiver
    if username not in online_users:
        online_users.append(username)
    
    # Adicionar à sala específica se não estiver
    if room in users_by_room and username not in users_by_room[room]:
        users_by_room[room].append(username)
    
    print(f'{username} entrou na sala {room}')
    
    # Notificar todos na sala
    emit('user_joined', {
        'username': username, 
        'room': room,
        'users_in_room': users_by_room.get(room, [])
    }, room=room)

@socketio.on('leave_room')
def handle_leave_room(data):
    username = data['username']
    room = data['room']
    
    # Remover usuário da sala
    leave_room(room)
    
    # Remover da sala específica
    if room in users_by_room and username in users_by_room[room]:
        users_by_room[room].remove(username)
    
    # Verificar se o usuário ainda está em alguma sala
    user_in_any_room = any(username in users for users in users_by_room.values())
    if not user_in_any_room and username in online_users:
        online_users.remove(username)
    
    print(f'{username} saiu da sala {room}')
    
    # Notificar todos na sala
    emit('user_left', {
        'username': username, 
        'room': room,
        'users_in_room': users_by_room.get(room, [])
    }, room=room)

@socketio.on('message')
def handle_message(data):
    room = data.get('room', 'geral')
    message = data['message']
    username = data['username']
    
    print(f'Mensagem na sala {room} de {username}: {message}')
    
    # Enviar mensagem apenas para usuários na mesma sala
    emit('message', {
        'username': username,
        'message': message,
        'room': room
    }, room=room)

# Evento disparado quando um usuário se conecta
@socketio.on('connect')
def handle_connect():
    print('Usuário conectado')

# Evento disparado quando um usuário se desconecta
@socketio.on('disconnect')
def handle_disconnect():
    print('Usuário desconectado')
    # Nota: Aqui seria ideal ter uma forma de identificar qual usuário desconectou
    # Para remover da lista, mas isso requer uma implementação mais avançada de sessões

# Executar a aplicação com SocketIO
if __name__ == '__main__':
    print("ChatApp iniciado")
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)