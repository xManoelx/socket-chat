from flask import Flask, render_template, jsonify
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
    return render_template('index.html')

# Rota do chat - Renderiza a página do chat
@app.route('/chat')
def chat():
    return render_template('chat.html')

# Rota de login - Renderiza a página de login
@app.route('/login')
def login():
    return render_template('login.html')

# Rota about - Renderiza a página sobre
@app.route('/about')
def about():
    return render_template('about.html')

# Rota para obter número de usuarios online
@app.route('/api/users')
def api_users():
    return jsonify({
        'users': online_users,
        'count': len(online_users)
    })

# Rota para obter salas de chat
@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

# Rota de logout - Renderiza a página de logout
@app.route('/logout')
def logout():
    return render_template('logout.html')

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