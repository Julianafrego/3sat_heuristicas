# mix de aleatoriedade com busca local
# algoritmo sorteia valores, true or false, para as variaveis
#verifica quais clausulas estão falsas
#escolhe clausula falsa aleatória

# apos isso, ele tem 2 formas para solucionar isso.
# 🔹 1. Com probabilidade p (ex: p = 0.5):
# Faz uma escolha aleatória dentro da cláusula.
# e troca o seu valor
# 🔸 2. Com probabilidade (1 - p) (ex: 0.5):
# testa cada variável da cláusula para ver qual delas, 
# se invertida, melhora mais o número de cláusulas verdadeiras.

# a escolha entre as duas formas é feita por sorteio probabilístico
# gera um num decimal entre 0 e 1, dita-se a probabilistica p
# p é a chance de de ser utilizado o modo aleatorio,
# ex. p= 1, 100% aleatorio, p=0.6 60% chance de ser aleatorio
# random.random() < p, 
# se valor sorteado for menor que p usa-se modo aleatorio
# se maior modo inteligente

import random

# avalia quantas cláusulas estão satisfeitas com a atribuição atual
def evaluate(formula, assignment):
    satisfied = 0
    for clause in formula:
        # se algum literal da cláusula é verdadeiro, a cláusula está satisfeita
        if any((assignment[abs(lit) - 1] if lit > 0 else not assignment[abs(lit) - 1]) for lit in clause):
            satisfied += 1
    return satisfied

# algoritmo walksat padrão
def walkSAT(formula, num_vars, max_flips=10000, p=0.5):
    # gera uma atribuição inicial aleatória de verdadeiros ou falsos para cada variável
    assignment = [random.choice([True, False]) for _ in range(num_vars)]
    
    for _ in range(max_flips):
        # seleciona as cláusulas que não estão satisfeitas com a atribuição atual
        unsat_clauses = [clause for clause in formula if not any(
            (assignment[abs(lit) - 1] if lit > 0 else not assignment[abs(lit) - 1]) for lit in clause)]

        # se não há cláusulas insatisfeitas, encontrou uma solução
        if not unsat_clauses:
            return assignment

        # escolhe uma cláusula insatisfeita aleatoriamente
        clause = random.choice(unsat_clauses)

        # com probabilidade p, escolhe uma variável aleatória da cláusula
        if random.random() < p:
            var_to_flip = abs(random.choice(clause)) - 1
        else:
            # senão, escolhe a melhor variável da cláusula para flipar
            best_var = None
            best_score = -1
            for lit in clause:
                var = abs(lit) - 1
                assignment[var] = not assignment[var]  # inverte temporariamente
                score = evaluate(formula, assignment)  # avalia quantas cláusulas ficaram satisfeitas
                assignment[var] = not assignment[var]  # desfaz a inversão
                if score > best_score:
                    best_score = score
                    best_var = var
            var_to_flip = best_var

        # aplica a troca definitiva na variável escolhida
        assignment[var_to_flip] = not assignment[var_to_flip]

    return None  # se não encontrou solução após max_flips

