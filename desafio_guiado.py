from leitor import carregar_clientes
from validador import validar_cliente, separar_registros
from transformador import transformar_cliente


def rodar_desafio_guiado():

    clientes_raw = carregar_clientes("data/clientes.csv")

    clientes_validos, _ = separar_registros(clientes_raw, validar_cliente)

    print("=== TRANSFORMAÇÃO ===\n")

    for cliente_raw in clientes_validos:
        cliente_normalizado = transformar_cliente(cliente_raw)

        print("ANTES:")
        print(
            f'  nome: "{cliente_raw["nome"]}" | email: "{cliente_raw["email"]}" | cidade: "{cliente_raw["cidade"]}"'
        )

        print("\nDEPOIS:")
        print(
            f'  nome: "{cliente_normalizado["nome"]}" | email: "{cliente_normalizado["email"]}" | cidade: "{cliente_normalizado["cidade"]}"'
        )
        print("-" * 50)


if __name__ == "__main__":
    rodar_desafio_guiado()
