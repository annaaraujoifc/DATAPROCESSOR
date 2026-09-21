from collections.abc import Iterable
from .entidades import Cliente, Transacao

def media_idade(clientes: Iterable[Cliente]) -> float:
    idades = [c.idade for c in clientes if c.idade is not None and c.idade > 0]
    return sum(idades) / len(idades) if idades else 0

def total_aprovado(transacoes: Iterable[Transacao]) -> float:
    return sum(t.valor for t in transacoes if t.esta_aprovada and t.valor is not None and t.valor > 0)
