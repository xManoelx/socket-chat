from app import app
from models import db, Room

# Inicializar banco de dados e criar salas padrão
def init_database():
    with app.app_context():
        # Criar tabelas
        db.create_all()
        
        # Verificar se as salas já existem
        if Room.query.count() == 0:
            # Criar salas padrão
            rooms_data = [
                {
                    'name': 'geral',
                    'display_name': 'Chat Geral',
                    'description': 'Converse com todos os usuários online'
                },
                {
                    'name': 'programacao',
                    'display_name': 'Programação',
                    'description': 'Discussões sobre desenvolvimento'
                },
                {
                    'name': 'games',
                    'display_name': 'Games',
                    'description': 'Chat sobre jogos e gaming'
                }
            ]
            
            for room_data in rooms_data:
                room = Room(**room_data)
                db.session.add(room)
            
            db.session.commit()
            print("Banco de dados inicializado com salas padrão!")
        else:
            print("Banco de dados já existe!")

if __name__ == '__main__':
    init_database()