from dataprocessor.pipeline import executar_pipeline

def main():
    resultado = executar_pipeline(
        "data/clientes.csv",
        "data/transacoes.csv",
        "data/config.json",
    )
    
    print("=== MODO DEBUG: REGISTROS INVÁLIDOS ===\n")
    
    print(f"CLIENTES INVÁLIDOS: {len(resultado['clientes_invalidos'])}")
    for item in resultado["clientes_invalidos"]:
        print(f"Registro bruto: {item['registro']}")
        print(f"Motivo(s) da falha: {item['erros']}\n")

    print(f"TRANSAÇÕES INVÁLIDAS: {len(resultado['transacoes_invalidas'])}")
    for item in resultado["transacoes_invalidas"]:
        print(f"Registro bruto: {item['registro']}")
        print(f"Motivo(s) da falha: {item['erros']}\n")

if __name__ == "__main__":
    main()