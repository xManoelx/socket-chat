from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from models import db, User, Room, Message, UserRoom
from datetime import datetime, timezone, timedelta

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'  # Chave secreta para sessões
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Funções de autenticação

# Autentica ou cria usuário
def authenticate_user(username):
    if not username or len(username.strip()) < 2:
        return False, "Nome de usuário deve ter pelo menos 2 caracteres"
    
    username = username.strip()
    
    # Verificar se o usuário já existe
    user = User.query.filter_by(username=username).first()
    
    if user:
        # Usuário existe, fazer login
        user.is_online = True
        user.last_seen = datetime.utcnow()
    else:
        # Criar novo usuário
        user = User(username=username, is_online=True)
        db.session.add(user)
    
    try:
        db.session.commit()
        login_user(user)
        return True, "Login realizado com sucesso"
    except Exception as e:
        db.session.rollback()
        return False, f"Erro ao fazer login: {str(e)}"

# Desloga usuário atual
def logout_current_user():
    if current_user.is_authenticated:
        current_user.is_online = False
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        logout_user()

# Retorna lista de usuários online
def get_online_users():
    return User.query.filter_by(is_online=True).all()

# Retorna usuários online em uma sala específica
def get_users_in_room(room_name):
    room = Room.query.filter_by(name=room_name).first()
    print(f"DEBUG get_users_in_room: sala {room_name}, room encontrada: {room}")
    
    if not room:
        return []
    
    user_rooms = UserRoom.query.filter_by(room_id=room.id).all()
    print(f"DEBUG: UserRoom entries: {len(user_rooms)}")
    
    users = [ur.user for ur in user_rooms if ur.user.is_online]
    print(f"DEBUG: usuarios online na sala: {[u.username for u in users]}")
    
    return users

# Adiciona usuário a uma sala
def user_join_room(username, room_name):
    user = User.query.filter_by(username=username).first()
    room = Room.query.filter_by(name=room_name).first()
    
    if not user or not room:
        return False
    
    # Verificar se já está na sala
    existing = UserRoom.query.filter_by(user_id=user.id, room_id=room.id).first()
    if existing:
        return True
    
    # Adicionar à sala
    user_room = UserRoom(user_id=user.id, room_id=room.id)
    db.session.add(user_room)
    
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

# Remove usuário de uma sala
def user_leave_room(username, room_name):
    user = User.query.filter_by(username=username).first()
    room = Room.query.filter_by(name=room_name).first()
    
    if not user or not room:
        return False
    
    user_room = UserRoom.query.filter_by(user_id=user.id, room_id=room.id).first()
    if user_room:
        db.session.delete(user_room)
        db.session.commit()
    
    return True

# Função para converter UTC para horário brasileiro
def get_brazil_time():
    # UTC-3 (horário padrão do Brasil)
    brazil_tz = timezone(timedelta(hours=-3))
    return datetime.now(brazil_tz)

def utc_to_brazil_time(utc_time):
    brazil_tz = timezone(timedelta(hours=-3))
    return utc_time.replace(tzinfo=timezone.utc).astimezone(brazil_tz)

# Rota principal - Renderiza a página inicial do chat
@app.route('/')
def index():
    return render_template('pages/index.html')

# Rota homepage - Renderiza a página principal após login
@app.route('/homepage')
@login_required
def homepage():
    return render_template('pages/homepage.html', username=current_user.username)

# Rota de login - Renderiza a página de login e processa o formulário
@app.route('/login', methods=['GET', 'POST'])
def login():
    print(f"Login route - Method: {request.method}")
    
    if request.method == 'POST':
        username = request.form.get('username')
        print(f"Username recebido: {username}")
        
        success, message = authenticate_user(username)
        print(f"Authenticate result: {success}, {message}")
        
        if success:
            flash(message, 'success')
            print("Redirecionando para homepage...")
            return redirect(url_for('homepage'))
        else:
            flash(message, 'error')
            print(f"Erro no login: {message}")
    
    return render_template('pages/login.html')

# Rota about - Renderiza a página sobre
@app.route('/about')
def about():
    return render_template('pages/about.html')

# Rota API - Retorna lista de usuários online
@app.route('/api/users')
def api_users():
    online_users = get_online_users()
    users_by_room = {}
    
    # Buscar usuários por sala
    rooms = Room.query.all()
    for room in rooms:
        users_in_room = get_users_in_room(room.name)
        users_by_room[room.name] = [user.username for user in users_in_room]
    
    return jsonify({
        'users_total': [user.username for user in online_users],
        'count_total': len(online_users),
        'users_by_room': users_by_room,
        'count_by_room': {room: len(users) for room, users in users_by_room.items()}
    })

# Nova rota para API de usuários de uma sala específica
@app.route('/api/users/<sala>')
def api_users_sala(sala):
    users_in_room = get_users_in_room(sala)
    return jsonify({
        'sala': sala,
        'users': [user.username for user in users_in_room],
        'count': len(users_in_room)
    })

# Rota rooms - Renderiza a página de salas de chat
@app.route('/rooms')
@login_required
def rooms():
    rooms_list = Room.query.all()
    return render_template('pages/rooms.html', rooms=rooms_list)

# Rota logout - Desloga o usuário
@app.route('/logout')
@login_required
def logout():
    logout_current_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

# Rotas para chats específicos
@app.route('/chat/<sala>')
@login_required
def chat_sala(sala):

    # Verificar se a sala existe
    room = Room.query.filter_by(name=sala).first()
    if not room:
        flash('Sala não encontrada!', 'error')
        return redirect(url_for('homepage'))
    
    # Buscar histórico de mensagens da sala (últimas 50)
    messages = Message.query.filter_by(room_id=room.id).order_by(Message.timestamp.desc()).limit(50).all()
    messages = list(reversed(messages))  # Mais antigas primeiro
    
    return render_template('pages/chat.html', 
                         username=current_user.username, 
                         sala=sala, 
                         room_display=room.display_name,
                         messages=messages)

#######################################################

@socketio.on('user_online')
def handle_user_online(data):
    username = data['username']
    user = User.query.filter_by(username=username).first()
    
    if user:
        user.is_online = True
        user.last_seen = datetime.utcnow()
        db.session.commit()
        print(f'{username} está online na homepage')
        
        # Notificar todos sobre a atualização
        emit_users_update()

@socketio.on('user_offline')
def handle_user_offline(data):
    username = data['username']
    user = User.query.filter_by(username=username).first()
    
    if user:
        user.is_online = False
        user.last_seen = datetime.utcnow()
        # Remover de todas as salas
        UserRoom.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        print(f'{username} saiu da homepage')
        
        # Notificar todos sobre a atualização
        emit_users_update()

@socketio.on('join_room')
def handle_join_room(data):
    username = data['username']
    room_name = data['room']
    
    print(f"DEBUG: {username} tentando entrar na sala {room_name}")
    
    # Adicionar usuário à sala no SocketIO
    join_room(room_name)
    
    # PRIMEIRO: Garantir que o usuário está online
    user = User.query.filter_by(username=username).first()
    if user:
        user.is_online = True
        user.last_seen = datetime.utcnow()
        db.session.commit()
        print(f"DEBUG: {username} marcado como online")
    
    # Adicionar no banco de dados
    success = user_join_room(username, room_name)
    print(f"DEBUG: user_join_room result: {success}")
    
    if success:
        users_in_room = get_users_in_room(room_name)
        print(f"DEBUG: usuarios na sala {room_name}: {[user.username for user in users_in_room]}")
        
        # Notificar todos na sala
        emit('user_joined', {
            'username': username, 
            'room': room_name,
            'users_in_room': [user.username for user in users_in_room]
        }, room=room_name)
        
        # Atualizar contadores globais
        emit_users_update()

@socketio.on('leave_room')
def handle_leave_room(data):
    username = data['username']
    room_name = data['room']
    
    # Remover usuário da sala no SocketIO
    leave_room(room_name)
    
    # Remover do banco de dados
    user_leave_room(username, room_name)
    users_in_room = get_users_in_room(room_name)
    print(f'{username} saiu da sala {room_name}')
    
    # Notificar todos na sala
    emit('user_left', {
        'username': username, 
        'room': room_name,
        'users_in_room': [user.username for user in users_in_room]
    }, room=room_name)
    
    # Atualizar contadores globais
    emit_users_update()

@socketio.on('message')
def handle_message(data):
    room_name = data.get('room', 'geral')
    message_content = data['message']
    username = data['username']
    
    # Buscar usuário e sala no banco
    user = User.query.filter_by(username=username).first()
    room = Room.query.filter_by(name=room_name).first()
    
    if user and room:
        # Salvar mensagem no banco
        message = Message(
            content=message_content,
            user_id=user.id,
            room_id=room.id,
            timestamp=get_brazil_time()  # ← Usar horário brasileiro
        )
        db.session.add(message)
        db.session.commit()
        
        print(f'Mensagem na sala {room_name} de {username}: {message_content}')
        
        # Enviar mensagem apenas para usuários na mesma sala
        emit('message', {
            'username': username,
            'message': message_content,
            'room': room_name,
            'timestamp': message.timestamp.strftime('%H:%M')
        }, room=room_name)

# Função auxiliar para emitir atualizações de usuários
def emit_users_update():
    online_users = get_online_users()
    users_by_room = {}
    
    rooms = Room.query.all()
    for room in rooms:
        users_in_room = get_users_in_room(room.name)
        users_by_room[room.name] = [user.username for user in users_in_room]
    
    socketio.emit('users_updated', {
        'users_total': [user.username for user in online_users],
        'count_total': len(online_users),
        'users_by_room': users_by_room,
        'count_by_room': {room: len(users) for room, users in users_by_room.items()}
    })

# Evento disparado quando um usuário se conecta
@socketio.on('connect')
def handle_connect():
    print('Usuário conectado')

# Evento disparado quando um usuário se desconecta
@socketio.on('disconnect')
def handle_disconnect():
    print('Usuário desconectado')

# Executar a aplicação com SocketIO
if __name__ == '__main__':
    print("ChatApp iniciado")
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)