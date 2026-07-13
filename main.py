from dataprocessor.pipeline import executar_pipeline, imprimir_relatorio

def main():
    resultado = executar_pipeline(
        "data/clientes.csv",
        "data/transacoes.csv",
        "data/config.json",
    )
    imprimir_relatorio(resultado)

if __name__ == "__main__":
    main()