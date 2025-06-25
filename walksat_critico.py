# versão melhorada do walksat com foco em cláusulas críticas
# algoritmo começa igual: sorteia valores true ou false para as variáveis
# verifica quais cláusulas estão falsas (insatisfeitas)

# além disso, ele mantém um contador de quantas vezes cada cláusula ficou insatisfeita
# se uma cláusula continuar falsa muitas vezes, ela se torna "crítica"
# essas cláusulas críticas ganham prioridade nas próximas escolhas

# na escolha da cláusula:
# 🔹 com probabilidade p_critico (ex: 0.7):
# escolhe uma cláusula crítica (mais problemática) aleatoriamente
# 🔸 com probabilidade (1 - p_critico):
# escolhe qualquer cláusula falsa aleatoriamente

# depois, a resolução da cláusula é igual ao algoritmo original:
# com chance p: escolhe uma variável aleatória da cláusula e inverte
# com chance (1 - p): testa cada variável da cláusula e inverte a que melhora mais

# essa estratégia permite atacar os pontos fracos da fórmula
# priorizando as partes que mais impedem a satisfação

import random
from walksat_padrao import evaluate  # reutiliza a função de avaliação

# versão modificada do walksat que dá prioridade a cláusulas críticas
def walkSAT_critico(formula, num_vars, max_flips=10000, p=0.5, p_critico=0.7, critico_treshold=5):
    # inicia atribuição aleatória
    assignment = [random.choice([True, False]) for _ in range(num_vars)]
    
    # conta quantas vezes cada cláusula foi insatisfeita
    clause_unsat_count = {i: 0 for i in range(len(formula))}
    
    for _ in range(max_flips):
        unsat = []
        crit = []

        # percorre todas as cláusulas
        for idx, clause in enumerate(formula):
            satisfied = any((assignment[abs(lit) - 1] if lit > 0 else not assignment[abs(lit) - 1]) for lit in clause)
            if not satisfied:
                unsat.append((idx, clause))  # adiciona à lista de cláusulas insatisfeitas
                clause_unsat_count[idx] += 1  # incrementa contagem
                if clause_unsat_count[idx] >= critico_treshold:
                    crit.append((idx, clause))  # marca como crítica se passar do limiar

        # se todas as cláusulas foram satisfeitas, retorna a solução
        if not unsat:
            return assignment

        # escolhe uma cláusula crítica ou uma aleatória das insatisfeitas
        idx, clause = random.choice(crit if crit and random.random() < p_critico else unsat)

        # escolhe uma variável da cláusula
        if random.random() < p:
            var_to_flip = abs(random.choice(clause)) - 1
        else:
            best_var = None
            best_score = -1
            for lit in clause:
                var = abs(lit) - 1
                assignment[var] = not assignment[var]
                score = evaluate(formula, assignment)
                assignment[var] = not assignment[var]
                if score > best_score:
                    best_score = score
                    best_var = var
            var_to_flip = best_var

        # aplica a troca definitiva
        assignment[var_to_flip] = not assignment[var_to_flip]

    return None  # não encontrou solução no limite de flips
