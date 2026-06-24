from leitor import carregar_clientes, carregar_transacoes, carregar_config
from validador import validar_cliente, validar_transacao, separar_registros
from transformador import transformar_clientes, transformar_transacoes
from processador import calcular_total_aprovado, calcular_media_idade


def gerar_relatorio_final():

    clientes_raw = carregar_clientes("data/clientes.csv")
    transacoes_raw = carregar_transacoes("data/transacoes.csv")
    config = carregar_config("data/config.json")

    clientes_validos_raw, clientes_invalidos = separar_registros(
        clientes_raw, validar_cliente
    )
    ids_validos = {c["id"] for c in clientes_validos_raw}

    transacoes_validas_raw, transacoes_invalidas = separar_registros(
        transacoes_raw, validar_transacao, ids_clientes=ids_validos, config=config
    )

    clientes_processados = transformar_clientes(clientes_validos_raw)
    transacoes_processadas = transformar_transacoes(transacoes_validas_raw)

    print("=== RELATÓRIO FINAL — DataProcessor ===\n")

    print(
        f"CLIENTES PROCESSADOS ({len(clientes_processados)} válidos de {len(clientes_raw)})"
    )
    for c in clientes_processados:
        print(
            f"  ID {c['id']} | {c['nome']} | {c['email']} | {c['idade']} anos | {c['cidade']}"
        )

    print(f"\nCLIENTES REJEITADOS ({len(clientes_invalidos)})")
    for item in clientes_invalidos:
        r = item["registro"]
        erros = ", ".join(item["erros"])
        print(f"  ID {r.get('id', '?')} — {r.get('nome', 'Desconhecido')}: {erros}")

    print(
        f"\nTRANSAÇÕES PROCESSADAS ({len(transacoes_processadas)} válidas de {len(transacoes_raw)})"
    )
    for t in transacoes_processadas:
        print(
            f"  ID {t['id']} | cliente {t['cliente_id']} | R$ {t['valor']:.2f} | {t['categoria']} | {t['status']}"
        )

    print(f"\nTRANSAÇÕES REJEITADAS ({len(transacoes_invalidas)})")
    for item in transacoes_invalidas:
        r = item["registro"]
        erros = ", ".join(item["erros"])
        print(f"  ID {r.get('id', '?')} — {erros}")

    print("\nMÉTRICAS")
    total_aprovado = calcular_total_aprovado(transacoes_processadas)
    media_idade = calcular_media_idade(clientes_processados)

    print(f"  Total aprovado: R$ {total_aprovado:.2f}")
    print(f"  Média de idade (válidos): {media_idade:.1f}")


if __name__ == "__main__":
    gerar_relatorio_final()
