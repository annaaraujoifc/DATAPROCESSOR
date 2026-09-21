from abc import ABC,abstractmethod
from pathlib import Path
from ..core.entidades import Cliente,Transacao
from .arquivos import carregar_clientes,carregar_config,carregar_transacoes
class FonteDados(ABC):
    @abstractmethod
    def carregar_clientes(self)->list[Cliente]:...
    @abstractmethod
    def carregar_transacoes(self)->list[Transacao]:...
    @abstractmethod
    def carregar_config(self)->dict:...
class FonteDadosArquivos(FonteDados):
    def __init__(self,caminho_clientes: str|Path,caminho_transacoes: str|Path,caminho_config: str|Path):self.caminho_clientes=caminho_clientes;self.caminho_transacoes=caminho_transacoes;self.caminho_config=caminho_config
    def carregar_clientes(self):return carregar_clientes(self.caminho_clientes)
    def carregar_transacoes(self):return carregar_transacoes(self.caminho_transacoes)
    def carregar_config(self):return carregar_config(self.caminho_config)
class FonteDadosMemoria(FonteDados):
    def __init__(self,clientes=(),transacoes=(),config=None):self._clientes=tuple(clientes);self._transacoes=tuple(transacoes);self._config=dict(config or {})
    def carregar_clientes(self):return list(self._clientes)
    def carregar_transacoes(self):return list(self._transacoes)
    def carregar_config(self):return dict(self._config)
