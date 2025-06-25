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

