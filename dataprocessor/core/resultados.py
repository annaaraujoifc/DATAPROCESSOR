from dataclasses import asdict, dataclass
from typing import Any
from .entidades import Cliente, Transacao

@dataclass(frozen=True)
class RegistroInvalido:
    registro: Cliente | Transacao
    erros: tuple[str, ...]
    @property
    def identificacao(self) -> str:
        return self.registro.identificacao if isinstance(self.registro, Cliente) else f"#{self.registro.id}"

@dataclass(frozen=True)
class ResultadoProcessamento:
    clientes: tuple[Cliente, ...]
    transacoes: tuple[Transacao, ...]
    clientes_invalidos: tuple[RegistroInvalido, ...]
    transacoes_invalidas: tuple[RegistroInvalido, ...]
    media_idade: float
    total_aprovado: float
    def to_dict(self) -> dict[str, Any]:
        return {"clientes":[asdict(c) for c in self.clientes],"transacoes":[asdict(t) for t in self.transacoes],"clientes_invalidos":[{"registro":asdict(i.registro),"erros":list(i.erros)} for i in self.clientes_invalidos],"transacoes_invalidas":[{"registro":asdict(i.registro),"erros":list(i.erros)} for i in self.transacoes_invalidas],"metricas":{"media_idade":self.media_idade,"total_aprovado":self.total_aprovado}}
