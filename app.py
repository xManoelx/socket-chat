from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Inicializar a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'  # Chave secreta para sessões

# Inicializar SocketIO com CORS habilitado
socketio = SocketIO(app, cors_allowed_origins="*")

# Rota principal - Renderiza a página inicial do chat
@app.route('/')
def index():
    return render_template('index.html')

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