matches = [
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

def add_matches(db, Partida):
    if not Partida.query.first(): 
        for horario, time_a, time_b in matches:
            partida = Partida(horario=horario, time_a=time_a, time_b=time_b)
            db.session.add(partida)
        db.session.commit()