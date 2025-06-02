from collections import defaultdict

# Função para calcular a tabela de classificação
def calculate_table(Resultado):
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
