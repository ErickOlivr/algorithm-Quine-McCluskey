import time
import os
import glob
def expand_dont_cares(binary_str):
    if '-' not in binary_str:
        return [int(binary_str, 2)]
    
    idx = binary_str.index('-')
    
    branch_0 = binary_str[:idx] + '0' + binary_str[idx+1:]
    branch_1 = binary_str[:idx] + '1' + binary_str[idx+1:]
    
    return expand_dont_cares(branch_0) + expand_dont_cares(branch_1)


def parse_pla(filepath):
    num_vars = 0
    minterms = set()
    
    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                
                if not line or line.startswith('#'):
                    continue
                    
                if line.startswith('.i'):
                    num_vars = int(line.split()[1])
                    
                elif line.startswith(('.o', '.ilb', '.ob', '.type', '.p')):
                    continue
                    
                elif line.startswith('.e'):
                    break
                    
                else:
                    parts = line.split()
                    
                    if len(parts) >= 2 and parts[1] == '1':
                        entrada_binaria = parts[0]
          
                        expanded_terms = expand_dont_cares(entrada_binaria)
                        minterms.update(expanded_terms)
                        
    except FileNotFoundError:
        print(f"Erro: O arquivo {filepath} não foi encontrado.")
        return None, None
        
    return num_vars, list(minterms)
def combine_terms(term1,term2):
        diff_count = 0
        combined_result = ""
        
        for i in range(len(term1)):
            if term1[i] != term2[i]:
                diff_count += 1
                combined_result += "-";
            else:
                combined_result += term1[i];        
        if diff_count == 1:
            return combined_result
        return None
    
def find_prime_implicants(minterms,num_vars):
    current_terms = set([format(m,f'0{num_vars}b') for m in minterms])
    prime_implicants = set()
    
    while True:
        new_terms = set()
        combined_this_round = set()
        
        terms_list = list(current_terms)
        
        for i in range(len(terms_list)):
            for j in range(1 + i, len(terms_list)):
                combined = combine_terms(terms_list[i], terms_list[j])
                
                if combined:
                    new_terms.add(combined)
                    
                    combined_this_round.add(terms_list[i])
                    combined_this_round.add(terms_list[j])
                    
        uncombined = current_terms - combined_this_round
        prime_implicants.update(uncombined)
        
        if not new_terms:
            break
        
        current_terms = new_terms
        
    return prime_implicants


def covers(implicant, minterms_bin):
    for i in range(len(implicant)):
        if implicant[i] != '-' and implicant[i] != minterms_bin[i]:
            return False
    return True

def select_minimum_implicants(prime_implicants, minterms, num_vars):
    minterms_bin = [format(m, f'0{num_vars}b') for m in minterms]
    
    chart = {m: [] for m in minterms_bin}
    
    for imp in prime_implicants:
        for m in minterms_bin:
            if covers(imp, m):
                chart[m].append(imp)
    final_solution = set()
    covered_minterms = set()
    
    
    for m, implicants in chart.items():
        if len(implicants) == 1:
            essential_imp = implicants[0]
            final_solution.add(essential_imp)
            
            
            for minterm in minterms_bin:
                if covers(essential_imp, minterm):
                    covered_minterms.add(minterm)
                    
    remaining_minterms = set(minterms_bin) - covered_minterms
    
    while remaining_minterms:
        best_imp = None
        max_convered = 0
        
        for imp in prime_implicants:
            if imp in final_solution:
                continue
            
            covers_count = sum(1 for m in remaining_minterms if covers(imp, m))
            
            if covers_count > max_convered:
                max_convered = covers_count
                best_imp = imp
                
        if best_imp:
            final_solution.add(best_imp)
            for m in list(remaining_minterms):
                if covers(best_imp, m):
                    remaining_minterms.remove(m)
        else:
            break
    return final_solution

def format_expression(implicants, num_vars):
    if not implicants:
        return "0" 
    letras = [f"x{i}" for i in range(num_vars)]
    
    termos_formatados = []
    
    for imp in implicants:
        termo = ""
        for i in range(len(imp)):
            if imp[i] == '1':
                termo += letras[i]
            elif imp[i] == '0':
                termo += letras[i] + "'" 
                
        if termo == "":
            termo = "1"
            
        termos_formatados.append(termo)
        
   
    return " + ".join(termos_formatados)
    

# --- Testando o Benchmark Completo ---
pasta_benchmarks = r"benchmark\benchmark\*.train.pla"
arquivos_para_testar = glob.glob(pasta_benchmarks)

print(f"Encontrados {len(arquivos_para_testar)} ficheiros para testar.\n")

for caminho_arquivo in arquivos_para_testar:
    nome_ficheiro = os.path.basename(caminho_arquivo)
    print(f"--- A processar: {nome_ficheiro} ---")
    
    quantidade_variaveis, mintermos = parse_pla(caminho_arquivo)
    
    if quantidade_variaveis is not None:
        inicio = time.time()
        
        implicantes = find_prime_implicants(mintermos, quantidade_variaveis)
        solucao_bruta = select_minimum_implicants(implicantes, mintermos, quantidade_variaveis)
        expressao_final = format_expression(solucao_bruta, quantidade_variaveis)
        
        fim = time.time()
        tempo_decorrido = fim - inicio
        
        print(f"Variáveis: {quantidade_variaveis} | Mintermos: {len(mintermos)}")
        print(f"Solução bruta:  {solucao_bruta}")
        print(f"S = {expressao_final}")
        print(f"Tempo de Execução: {tempo_decorrido:.5f} segundos\n")