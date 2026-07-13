from .leitor import carregar_clientes, carregar_transacoes, carregar_config
from .validador import validar_cliente, validar_transacao, separar_registros
from .transformador import transformar_clientes, transformar_transacoes
from .processador import calcular_total_aprovado, calcular_media_idade

def executar_pipeline(caminho_clientes, caminho_transacoes, caminho_config):
    clientes_raw = carregar_clientes(caminho_clientes)
    transacoes_raw = carregar_transacoes(caminho_transacoes)
    config = carregar_config(caminho_config)

    clientes_validos_raw, clientes_invalidos = separar_registros(
        clientes_raw, validar_cliente
    )
    ids_validos = {c["id"] for c in clientes_validos_raw}

    transacoes_validas_raw, transacoes_invalidas = separar_registros(
        transacoes_raw, validar_transacao, ids_clientes=ids_validos, config=config
    )

    clientes_processados = transformar_clientes(clientes_validos_raw)
    transacoes_processadas = transformar_transacoes(transacoes_validas_raw)

    total_aprovado = calcular_total_aprovado(transacoes_processadas)
    media_idade = calcular_media_idade(clientes_processados)

    return {
        "clientes_raw": clientes_raw,
        "transacoes_raw": transacoes_raw,
        "clientes_processados": clientes_processados,
        "clientes_invalidos": clientes_invalidos,
        "transacoes_processadas": transacoes_processadas,
        "transacoes_invalidas": transacoes_invalidas,
        "metricas": {
            "total_aprovado": total_aprovado,
            "media_idade": media_idade,
        },
    }

def imprimir_relatorio(resultado):
    clientes_processados = resultado["clientes_processados"]
    clientes_raw = resultado["clientes_raw"]
    clientes_invalidos = resultado["clientes_invalidos"]
    transacoes_processadas = resultado["transacoes_processadas"]
    transacoes_raw = resultado["transacoes_raw"]
    transacoes_invalidas = resultado["transacoes_invalidas"]
    total_aprovado = resultado["metricas"]["total_aprovado"]
    media_idade = resultado["metricas"]["media_idade"]

    print("=== RELATÓRIO FINAL — DataProcessor ===\n")

    print(f"CLIENTES PROCESSADOS ({len(clientes_processados)} válidos de {len(clientes_raw)})")
    for c in clientes_processados:
        print(f"  ID {c['id']} | {c['nome']} | {c['email']} | {c['idade']} anos | {c['cidade']}")

    print(f"\nCLIENTES REJEITADOS ({len(clientes_invalidos)})")
    for item in clientes_invalidos:
        r = item["registro"]
        erros = ", ".join(item["erros"])
        print(f"  ID {r.get('id', '?')} — {r.get('nome', 'Desconhecido')}: {erros}")

    print(f"\nTRANSAÇÕES PROCESSADAS ({len(transacoes_processadas)} válidas de {len(transacoes_raw)})")
    for t in transacoes_processadas:
        print(f"  ID {t['id']} | cliente {t['cliente_id']} | R$ {t['valor']:.2f} | {t['categoria']} | {t['status']}")

    print(f"\nTRANSAÇÕES REJEITADAS ({len(transacoes_invalidas)})")
    for item in transacoes_invalidas:
        r = item["registro"]
        erros = ", ".join(item["erros"])
        print(f"  ID {r.get('id', '?')} — {erros}")

    print("\nMÉTRICAS")
    print(f"  Total aprovado: R$ {total_aprovado:.2f}")
    print(f"  Média de idade (válidos): {media_idade:.1f}")