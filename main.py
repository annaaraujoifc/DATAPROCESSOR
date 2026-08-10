from dataprocessor.config import carregar_configuracao_padrao
from dataprocessor.services.processamento import executar_processamento


def main():
    app_config = carregar_configuracao_padrao()
    resultado = executar_processamento(app_config)

    print("=== DataProcessor CLI ===")
    print(f"Clientes válidos: {len(resultado['clientes'])}")
    print(f"Clientes inválidos: {len(resultado['clientes_invalidos'])}")
    print(f"Transações válidas: {len(resultado['transacoes'])}")
    print(f"Transações inválidas: {len(resultado['transacoes_invalidas'])}")
    print(f"Média de idade: {resultado['metricas']['media_idade']:.1f}")
    print(f"Total aprovado: R$ {resultado['metricas']['total_aprovado']:.2f}")


if __name__ == "__main__":
    main()