from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from utils.db import config_database, create_tables, clear_partida_table, clear_resultado_table
from utils.table_functions import calculate_table
import json

# Configuração da aplicação
app = Flask(__name__)
app.secret_key = "rachaIPC"
config_database(app)
db = SQLAlchemy(app)

# Criação das tabelas Resultado e Partida
Resultado, Partida, Time = create_tables(db)

# Página inicial com partidas pendentes
@app.route('/')
def index():
    TIMES = [time.team_name for time in Time.query.all()]
    
    if len(TIMES) == 0:
        TIMES = False

    partidas_pendentes = Partida.query.filter_by(resultado_id=None).all()
    return render_template('index.html', times=TIMES, partidas=partidas_pendentes)

# Rota para adicionar resultado de uma partida
@app.route('/adicionar_resultado', methods=['POST'])
def adicionar_resultado():
    time1 = request.form['time1']
    time2 = request.form['time2']
    gols1 = int(request.form['gols1'])
    gols2 = int(request.form['gols2'])

    if time1 == time2:
        return redirect(url_for('index'))  # Não permite confronto do mesmo time

    novo_resultado = Resultado(time1=time1, time2=time2, gols1=gols1, gols2=gols2)
    db.session.add(novo_resultado)
    db.session.commit()

    partida = Partida.query.filter_by(time_a=time1, time_b=time2, resultado_id=None).first()
    if partida:
        partida.resultado_id = novo_resultado.id
        db.session.commit()

    return redirect(url_for('index'))

# Rota para visualizar a tabela de classificação
@app.route('/tabela')
def tabela():
    classificacao = calculate_table(Resultado)
    return render_template('tabela.html', classificacao=classificacao)

# Rota para visualizar todas as partidas
@app.route('/partidas')
def ver_partidas():
    partidas = Partida.query.all()
    return render_template('partidas.html', partidas=partidas)

# Rota para limpar resultados
@app.route('/limparResultados', methods=['GET', 'POST'])
def limpar_resultados():
    if request.method == 'POST':
        clear_resultado_table(db, Resultado)
        return redirect(url_for('tabela'))
    return render_template('clear_scoreboard.html')

# Rota para limpar partidas
@app.route('/limparPartidas', methods=['GET', 'POST'])
def limpar_partidas():
    if request.method == 'POST':
        clear_partida_table(db, Partida)
        return redirect(url_for('ver_partidas'))
    return render_template('clear_matches.html')

@app.route('/adicionarPartidas', methods=['GET', 'POST'])
def add_matches_view():
    if request.method == 'POST':
        partidas_json = request.form.get('partidas')
        partidas = json.loads(partidas_json)

        for partida in partidas:
            nova_partida = Partida(
                horario=partida['horario'],
                time_a=partida['time_a'],
                time_b=partida['time_b']
            )
            db.session.add(nova_partida)
        db.session.commit()
    return render_template('add_matches.html')

@app.route('/criarTime', methods=['GET', 'POST'])
def create_team_view():
    if request.method == "POST":
        new_team_name = request.form['team-name']
        new_team = Time(team_name=new_team_name)
        
        existing_team = db.session.query(Time).filter(Time.team_name == new_team_name).first()
        
        if existing_team:
            flash("TEAM ALREADY EXISTS!")
        else:
            flash("TEAM CREATED!")
            db.session.add(new_team)
            db.session.commit()

        return redirect(url_for('create_team_view'))

    context = {
            'team_list': Time.query.all(),
    }

    return render_template('create_team.html', context=context)

@app.route('/removerTime', methods=["POST"])
def remove_team():
    team_to_remove = request.form['team_name']
    team = db.session.query(Time).filter(Time.team_name == team_to_remove).first()

    if team:
        db.session.delete(team)
        db.session.commit()
        flash(f"Time {team_to_remove} removido com sucesso!")
    else:
        flash(f"Time {team_to_remove} não encontrado!")

    context = {
            'team_list': Time.query.all()
    }

    return redirect(url_for('create_team_view'))
# Execução da aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
