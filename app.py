from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'  # Chave secreta para sessões

# Inicializa SocketIO com CORS habilitado
socketio = SocketIO(app, cors_allowed_origins="*")

# Lista para armazenar usuários online
online_users = []

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

@app.route('/api/users')
def api_users():
    return jsonify({
        'users': online_users,
        'count': len(online_users)
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

@socketio.on('message')
def handle_message(msg):
    print(f'Mensagem recebida: {msg}')
    emit('message', msg, broadcast=True)

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
    print("Chat iniciado")
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)