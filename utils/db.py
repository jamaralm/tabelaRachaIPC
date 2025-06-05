def config_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rachaipc_user:8gSyegzmA2lEnxg9XgbJNWdiAQGxQxXT@dpg-d0sckfre5dus73elh450-a.oregon-postgres.render.com/rachaipc'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def create_tables(db):
    class Resultado(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        time1 = db.Column(db.String(50), nullable=False)
        time2 = db.Column(db.String(50), nullable=False)
        gols1 = db.Column(db.Integer, nullable=False)
        gols2 = db.Column(db.Integer, nullable=False)

    class Partida(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        horario = db.Column(db.String(10), nullable=False)
        time_a = db.Column(db.String(50), nullable=False)
        time_b = db.Column(db.String(50), nullable=False)
        resultado_id = db.Column(db.Integer, db.ForeignKey('resultado.id'), nullable=True)

        resultado = db.relationship('Resultado', backref='partida', uselist=False)
    
    class Time(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        team_name = db.Column(db.String(50), nullable=False)
        team_total_matches = db.Column(db.Integer, nullable=True)
        team_total_goals = db.Column(db.Integer, nullable=True)
        team_total_wins = db.Column(db.Integer, nullable=True)
        team_total_losses = db.Column(db.Integer, nullable=True)
        
        def __init__(self, team_name):
            self.team_name = team_name

    return Resultado, Partida, Time

'''
    CRUD TABLE FUNCTIONS
'''

def clear_partida_table(db, Partida):
    try:
        db.session.query(Partida).delete()
        db.session.commit()
        print("Tabela PARTIDA limpa com sucesso!")
    except Exception as e:
        db.session.rollback()
        print(f"EXCEPTION: {e}")

def clear_resultado_table(db, Resultado):
    try:
        db.session.query(Resultado).delete()
        db.session.commit()
        print("Tabela PARTIDA limpa com sucesso!")
    except Exception as e:
        db.session.rollback()
        print(f"EXCEPTION: {e}")

def clear_time_table(db, Time):
    try:
        db.session.query(Time).delete()
        db.session.commit()
        print("Tabela TIME limpa com sucesso!")
    except Exception as e:
        db.session.rollback()
        print(f"EXCEPTION: {e}")
