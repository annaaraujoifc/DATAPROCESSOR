# main.py
from leitor import carregar_clientes, carregar_transacoes, carregar_config
from validador import validar_cliente, validar_transacao, separar_registros
from transformador import transformar_clientes, transformar_transacoes
from processador import calcular_total_aprovado, calcular_media_idade, clientes_por_cidade

print("=== DataProcessor CLI ===")
print()

# --- LEITURA ---
print("[LEITURA]")

clientes_raw = carregar_clientes("data/clientes.csv")
print(f"  clientes.csv ............. {len(clientes_raw)} registros")

transacoes_raw = carregar_transacoes("data/transacoes.csv")
print(f"  transacoes.csv ........... {len(transacoes_raw)} registros")

config = carregar_config("data/config.json")
print(f"  config.json .............. OK")
print()

# --- VALIDAÇÃO ---
print("[VALIDAÇÃO]")

clientes_validos, clientes_invalidos = separar_registros(
    clientes_raw, validar_cliente
)
ids_validos = {c["id"] for c in clientes_validos}

transacoes_validas, transacoes_invalidas = separar_registros(
    transacoes_raw, validar_transacao,
    ids_clientes=ids_validos, config=config
)

print(f"  Clientes válidos: {len(clientes_validos)} / {len(clientes_raw)}")
print(f"  Transações válidas: {len(transacoes_validas)} / {len(transacoes_raw)}")
print()

# Detalhar erros de clientes
print("  Clientes rejeitados:")
for item in clientes_invalidos:
    r = item["registro"]
    erros = ", ".join(item["erros"])
    print(f"    ID {r['id']} — {r['nome']}: {erros}")
print()

# Detalhar erros de transações
print("  Transações rejeitadas:")
for item in transacoes_invalidas:
    r = item["registro"]
    erros = ", ".join(item["erros"])
    print(f"    ID {r['id']}: {erros}")
print()

# --- TRANSFORMAÇÃO ---
print("[TRANSFORMAÇÃO]")

clientes = transformar_clientes(clientes_validos)
transacoes = transformar_transacoes(transacoes_validas)

print(f"  {len(clientes)} clientes normalizados")
print(f"  {len(transacoes)} transações normalizadas")
print()

# --- RELATÓRIO ---
print("[RELATÓRIO]")

total_aprovado = calcular_total_aprovado(transacoes)
media_idade = calcular_media_idade(clientes)
por_cidade = clientes_por_cidade(clientes)

print(f"  Total aprovado: R$ {total_aprovado:.2f}")
print(f"  Média de idade: {media_idade:.1f}")
print("  Clientes por cidade:")
for cidade, qtd in por_cidade.items():
    print(f"    {cidade}: {qtd}")
