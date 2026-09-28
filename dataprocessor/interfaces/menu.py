from pathlib import Path

from ..infra.fontes import FonteDadosArquivos
from ..infra.relatorios import criar_gerador
from ..services.processamento import executar_processamento


def _ler_entrada(prompt: str, padrao: str = "") -> str:
    try:
        valor = input(prompt)
    except EOFError:
        print()
        return padrao
    return valor.strip() if valor is not None else padrao


def _ler_caminho_arquivo(
    prompt: str, padrao: str, *, exigir_existencia: bool = True
) -> str:
    while True:
        valor = _ler_entrada(prompt, padrao)
        caminho = valor or padrao
        caminho_path = Path(caminho)

        if caminho_path.exists() and caminho_path.is_dir():
            print(f"Erro: '{caminho}' é um diretório. Informe o caminho do arquivo.")
            continue

        if exigir_existencia and not caminho_path.exists():
            print(f"Arquivo não encontrado: '{caminho}'. Informe um caminho válido.")
            continue

        return str(caminho_path)


def processar():
    caminho_clientes = _ler_caminho_arquivo(
        "Caminho do CSV de clientes [data/clientes.csv]: ",
        "data/clientes.csv",
    )
    caminho_transacoes = _ler_caminho_arquivo(
        "Caminho do CSV de transações [data/transacoes.csv]: ",
        "data/transacoes.csv",
    )
    caminho_config = _ler_caminho_arquivo(
        "Caminho do JSON de config [data/config.json]: ",
        "data/config.json",
    )

    fonte = FonteDadosArquivos(caminho_clientes, caminho_transacoes, caminho_config)
    resultado = executar_processamento(fonte)
    print(f"Clientes válidos: {len(resultado.clientes)}")
    print(f"Transações válidas: {len(resultado.transacoes)}")
    return resultado


def exibir_relatorio(resultado):
    formato = _ler_entrada("Formato (texto/json/csv) [texto]: ", "texto") or "texto"
    gerador = criar_gerador(formato)
    print(gerador.render(resultado))


def salvar_relatorio(resultado):
    formato = _ler_entrada("Formato (texto/json/csv) [texto]: ", "texto") or "texto"
    caminho = (
        _ler_entrada(
            "Caminho do arquivo [output/relatorio.txt]: ", "output/relatorio.txt"
        )
        or "output/relatorio.txt"
    )

    gerador = criar_gerador(formato)
    relatorio = gerador.render(resultado)

    caminho_saida = Path(caminho)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    caminho_saida.write_text(relatorio, encoding="utf-8")

    print(f"Relatório salvo em: {caminho_saida}")


def menu_principal() -> int:
    resultado = None

    try:
        while True:
            print("\n=== DataProcessor — Menu ===")
            print("1. Processar dados")
            print("2. Exibir relatório")
            print("3. Salvar relatório em arquivo")
            print("4. Sair")
            opcao = _ler_entrada("Escolha uma opção: ")

            if opcao == "1":
                resultado = processar()
            elif opcao == "2":
                exibir_relatorio(resultado)
            elif opcao == "3":
                salvar_relatorio(resultado)
            elif opcao == "4":
                break
            elif opcao == "":
                continue
            else:
                print("Opção inválida. Tente novamente.")
    except EOFError:
        print("\nEncerrando menu.")

    return 0


if __name__ == "__main__":
    raise SystemExit(menu_principal())
