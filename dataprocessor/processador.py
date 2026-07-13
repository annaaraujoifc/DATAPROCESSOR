# processador.py


def calcular_total_aprovado(transacoes):
    return sum(
        t["valor"]
        for t in transacoes
        if t.get("status") == "aprovado" and t.get("valor") is not None
    )


def calcular_media_idade(clientes):
    idades = [c["idade"] for c in clientes if c.get("idade") is not None]
    if not idades:
        return 0
    return sum(idades) / len(idades)


def calcular_minimo(transacoes):
    valores = [t["valor"] for t in transacoes if t.get("valor") is not None]
    return min(valores) if valores else 0


def calcular_maximo(transacoes):
    valores = [t["valor"] for t in transacoes if t.get("valor") is not None]
    return max(valores) if valores else 0


def clientes_por_cidade(clientes):
    contagem = {}
    for c in clientes:
        cidade = c.get("cidade", "Desconhecida")
        contagem[cidade] = contagem.get(cidade, 0) + 1
    return contagem
