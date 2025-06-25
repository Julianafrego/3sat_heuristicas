import time
import csv
import statistics
import matplotlib.pyplot as plt

from walksat_padrao import walkSAT
from walksat_critico import walkSAT_critico

# executa múltiplos testes para cada algoritmo
def run_tests_log(formula, num_vars, algorithm, num_runs=10, **kwargs):
    successes = 0
    total_time = 0
    times = []

    for _ in range(num_runs):
        start = time.time()    
        result = algorithm(formula, num_vars, **kwargs) # executa o algoritmo 
        end = time.time()
        elapsed = end - start
        times.append(elapsed)
        total_time += elapsed
        if result is not None:   # se algoritmo n retornou solucao vazia, aumenta 1 sucesso
            successes += 1

    avg_time = total_time / num_runs # calcula tempo medio
    desvio = statistics.stdev(times) if num_runs > 1 else 0.0 # calcula desvio padrao, p/ mais de uma execucao

    print(f"{algorithm.__name__} | sucesso: {successes}/{num_runs} | tempo médio: {avg_time:.4f}s | desvio: {desvio:.4f}s")
    return {
        "algorithm": algorithm.__name__,
        "successes": successes,
        "num_runs": num_runs,
        "avg_time": avg_time,
        "stdev": desvio,
        "all_times": times
    }

# gera instância aleatoria do problema 3-sat
def gerar_instancia_3sat(num_vars, num_clausulas):
    import random
    formula = []   # lista de clausulas
    for _ in range(num_clausulas):
        clause = []  # uma clausula com 3 literais
        while len(clause) < 3:
            lit = random.randint(1, num_vars)  # sorteia variavel
            lit = lit if random.random() < 0.5 else -lit   # chance de 50% dela ser negativa
            if lit not in clause and -lit not in clause:  # evita repeticao de variavel ou seu inverso
                clause.append(lit)
        formula.append(clause)   # add clausula a formula
    return formula

# parametros dos testes
tamanhos_variaveis = [100, 200, 300]
num_clauses_ratio = 4
num_execucoes = 10
resultados = []

# executa os testes para cada tamanho de instância
for n_vars in tamanhos_variaveis:
    n_clauses = n_vars * num_clauses_ratio
    formula = gerar_instancia_3sat(n_vars, n_clauses)
    print(f"\n== {n_vars} variáveis / {n_clauses} cláusulas ==")

    # executa walksat padrão
    r1 = run_tests_log(formula, n_vars, walkSAT, num_runs=num_execucoes, max_flips=10000, p=0.5)
    r1["n_vars"] = n_vars
    resultados.append(r1)

    # executa walksat crítico
    r2 = run_tests_log(formula, n_vars, walkSAT_critico, num_runs=num_execucoes, max_flips=5000, p=0.5, p_critico=0.7, critico_treshold=5)
    r2["n_vars"] = n_vars
    resultados.append(r2)

# salva os resultados em um arquivo csv
with open("avaliacao_resultados.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["algoritmo", "variáveis", "sucessos", "num_runs", "tempo médio", "desvio padrão", "todos os tempos"])
    for r in resultados:
        writer.writerow([r["algorithm"], r["n_vars"], r["successes"], r["num_runs"], r["avg_time"], r["stdev"], r["all_times"]])

print("\narquivo 'avaliacao_resultados.csv' gerado com sucesso!")

# gera grafico comparando os tempos médios
labels = [str(r["n_vars"]) for r in resultados if r["algorithm"] == "walkSAT"]
walksat_avg = [r["avg_time"] for r in resultados if r["algorithm"] == "walkSAT"]
critico_avg = [r["avg_time"] for r in resultados if r["algorithm"] == "walkSAT_critico"]

x = range(len(labels))
plt.figure(figsize=(10, 5))
plt.bar(x, walksat_avg, width=0.4, label="walksat", align='center')
plt.bar([i + 0.4 for i in x], critico_avg, width=0.4, label="walksat crítico", align='center')
plt.xticks([i + 0.2 for i in x], labels)
plt.xlabel("número de variáveis")
plt.ylabel("tempo médio (s)")
plt.title("comparação de tempo médio - walksat vs. walksat crítico")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_comparativo.png")
plt.show()
