from flask import Flask, render_template, request, redirect, url_for
from utils.db import config_database, create_tables, clear_partida_table,clear_resultado_table
from utils.table_functions import calculate_table
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
config_database(app)
db = SQLAlchemy(app)

# Times pré-cadastrados
times = ["Relâmpago", "Fogo", "Esmeralda", "Dourada", "Imperial"]

Resultado, Partida = create_tables(db)

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

        partida = Partida.query.filter_by(time_a=time1, time_b=time2, resultado_id=None).first()
        if partida:
            partida.resultado_id = novo_resultado.id
            db.session.commit()

    return redirect(url_for('index'))

# Ver tabela de classificação
@app.route('/tabela')
def tabela():
    classificacao = calculate_table(Resultado)
    return render_template('tabela.html', classificacao=classificacao)

# Ver todas as partidas
@app.route('/partidas')
def ver_partidas():
    partidas = Partida.query.all()
    return render_template('partidas.html', partidas=partidas)

@app.route('/limparResultados', methods=['GET', 'POST'])
def limpar_resultados():
    if request.method == 'POST':
        clear_resultado_table(db, Resultado)
        return redirect('/tabela')
    return render_template('clear_scoreboard.html')

@app.route('/limparPartidas', methods=['GET', 'POST'])
def limpar_partidas():
    if request.method == 'POST':
        clear_partida_table(db, Partida)
        return redirect("/partidas")
    return render_template('clear_matches.html')

# Inicialização
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Popular a tabela de partidas apenas se estiver vazia
        if not Partida.query.first():
            jogos = [
                ("20:00", "Fogo", "Dourada"),         # 1 Fogo, Dourada
                ("20:08", "Esmeralda", "Fogo"),       # 2 Esmeralda, Fogo (Fogo 2 seguidas)
                ("20:16", "Dourada", "Esmeralda"),    # 3 Dourada, Esmeralda (Dourada 2 seguidas)
                ("20:24", "Relâmpago", "Dourada"),    # 4 Relâmpago, Dourada (Dourada 3? Não, intervalo)
                ("20:32", "Relâmpago", "Fogo"),       # 5 Relâmpago, Fogo (Fogo 3? Não, intervalo)
                ("20:40", "Esmeralda", "Relâmpago"),  # 6 Esmeralda, Relâmpago (Relâmpago 2 seguidas)
                ("20:48", "Fogo", "Esmeralda"),       # 7 Fogo, Esmeralda (Fogo 2 seguidas)
                ("20:56", "Dourada", "Fogo"),         # 8 Dourada, Fogo (Fogo 3? Não, intervalo)
                ("21:04", "Relâmpago", "Esmeralda"),  # 9 Relâmpago, Esmeralda (Relâmpago 3? Não, intervalo)
                ("21:12", "Fogo", "Relâmpago"),       # 10 Fogo, Relâmpago (Fogo 2 seguidas)
                ("21:20", "Esmeralda", "Dourada"),    # 11 Esmeralda, Dourada
                ("21:28", "Dourada", "Relâmpago"),    # 12 Dourada, Relâmpago
            ]
            for horario, time_a, time_b in jogos:
                partida = Partida(horario=horario, time_a=time_a, time_b=time_b)
                db.session.add(partida)
            db.session.commit()

    app.run(debug=True)
