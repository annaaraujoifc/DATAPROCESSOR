from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    caminho_clientes: str
    caminho_transacoes: str
    caminho_config: str


def carregar_configuracao_padrao():
    return AppConfig(
        caminho_clientes="data/clientes.csv",
        caminho_transacoes="data/transacoes.csv",
        caminho_config="data/config.json",
    )