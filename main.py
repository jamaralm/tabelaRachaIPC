from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///partidas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Times pré-cadastrados
times = ["Relâmpago", "Fogo", "Esmeralda", "Dourada", "Imperial"]

# Modelo de resultado
class Resultado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time1 = db.Column(db.String(50), nullable=False)
    time2 = db.Column(db.String(50), nullable=False)
    gols1 = db.Column(db.Integer, nullable=False)
    gols2 = db.Column(db.Integer, nullable=False)

# Modelo de partida
class Partida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.String(10), nullable=False)
    time_a = db.Column(db.String(50), nullable=False)
    time_b = db.Column(db.String(50), nullable=False)
    resultado_id = db.Column(db.Integer, db.ForeignKey('resultado.id'), nullable=True)

    resultado = db.relationship('Resultado', backref='partida', uselist=False)

# Função para calcular a tabela de classificação
def calcular_tabela():
    partidas = Resultado.query.all()

    tabela = defaultdict(lambda: {
        "P": 0, "J": 0, "V": 0, "E": 0, "D": 0,
        "GP": 0, "GC": 0, "SG": 0
    })

    for r in partidas:
        t1, t2 = r.time1, r.time2
        g1, g2 = r.gols1, r.gols2

        tabela[t1]['J'] += 1
        tabela[t2]['J'] += 1
        tabela[t1]['GP'] += g1
        tabela[t1]['GC'] += g2
        tabela[t2]['GP'] += g2
        tabela[t2]['GC'] += g1

        if g1 > g2:
            tabela[t1]['V'] += 1
            tabela[t2]['D'] += 1
            tabela[t1]['P'] += 3
        elif g2 > g1:
            tabela[t2]['V'] += 1
            tabela[t1]['D'] += 1
            tabela[t2]['P'] += 3
        else:
            tabela[t1]['E'] += 1
            tabela[t2]['E'] += 1
            tabela[t1]['P'] += 1
            tabela[t2]['P'] += 1

    for time in tabela:
        tabela[time]['SG'] = tabela[time]['GP'] - tabela[time]['GC']

    return sorted(tabela.items(), key=lambda x: (x[1]['P'], x[1]['SG'], x[1]['GP']), reverse=True)

# Página inicial com partidas pendentes
@app.route('/')
def index():
    partidas_pendentes = Partida.query.filter_by(resultado_id=None).all()
    return render_template('index.html', times=times, partidas=partidas_pendentes)

# Adicionar resultado
@app.route('/adicionar_resultado', methods=['POST'])
def adicionar_resultado():
    time1 = request.form['time1']
    time2 = request.form['time2']
    gols1 = int(request.form['gols1'])
    gols2 = int(request.form['gols2'])

    if time1 != time2:
        novo_resultado = Resultado(time1=time1, time2=time2, gols1=gols1, gols2=gols2)
        db.session.add(novo_resultado)
        db.session.commit()

        # Associar resultado à partida correspondente
        partida = Partida.query.filter_by(time_a=time1, time_b=time2, resultado_id=None).first()
        if partida:
            partida.resultado_id = novo_resultado.id
            db.session.commit()

    return redirect(url_for('index'))

# Ver tabela de classificação
@app.route('/tabela')
def tabela():
    classificacao = calcular_tabela()
    return render_template('tabela.html', classificacao=classificacao)

# Ver todas as partidas
@app.route('/partidas')
def ver_partidas():
    partidas = Partida.query.all()
    return render_template('partidas.html', partidas=partidas)

# Inicialização
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Popular a tabela de partidas apenas se estiver vazia
        if not Partida.query.first():
            jogos = [
                # Turno 1
                ("20:00", "Fogo", "Dourada"),
                ("20:08", "Fogo", "Dourada"),
                ("20:16", "Esmeralda", "Dourada"),
                ("20:24", "Esmeralda", "Relâmpago"),
                ("20:32", "Fogo", "Relâmpago"),
                ("20:40", "Esmeralda", "Fogo"),
                ("20:48", "Dourada", "Relâmpago"),
                ("20:56", "Esmeralda", "Dourada"),
                # Turno 2
                ("21:04", "Dourada", "Fogo"),
                ("21:12", "Dourada", "Fogo"),
                ("21:20", "Dourada", "Esmeralda"),
                ("21:28", "Relâmpago", "Esmeralda"),
                ("21:36", "Relâmpago", "Fogo"),
                ("21:44", "Fogo", "Esmeralda"),
                ("21:52", "Relâmpago", "Dourada"),
                ("22:00", "Dourada", "Esmeralda"),
            ]
            for horario, time_a, time_b in jogos:
                partida = Partida(horario=horario, time_a=time_a, time_b=time_b)
                db.session.add(partida)
            db.session.commit()

    app.run(debug=True)
