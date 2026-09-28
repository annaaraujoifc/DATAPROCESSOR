from pathlib import Path

from ..infra.fontes import FonteDadosArquivos
from ..infra.relatorios import criar_gerador
from ..services.processamento import executar_processamento


FORMATOS_VALIDOS = {"texto", "json", "csv"}


def _ler_entrada(prompt: str, padrao: str = "") -> str:
    try:
        valor = input(prompt)
    except EOFError:
        print()
        return padrao
    return valor.strip() if valor is not None else padrao


def _ler_caminho_arquivo(
    prompt: str, padrao: str, *, exigir_existencia: bool = False
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


def _ler_caminhos() -> tuple[str, str, str]:
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
    return caminho_clientes, caminho_transacoes, caminho_config


def processar(caminhos: tuple[str, str, str] | None = None):
    if caminhos is None:
        caminhos = _ler_caminhos()

    try:
        fonte = FonteDadosArquivos(*caminhos)
        resultado = executar_processamento(fonte)
    except (OSError, ValueError, KeyError) as erro:
        print(f"[ERRO] Não foi possível processar: {erro}")
        return None

    print(f"Clientes válidos: {len(resultado.clientes)}")
    print(f"Transações válidas: {len(resultado.transacoes)}")
    return resultado


def exibir_relatorio(resultado):
    formato = _ler_entrada("Formato (texto/json/csv) [texto]: ", "texto") or "texto"

    if formato not in FORMATOS_VALIDOS:
        print(f"Formato inválido: '{formato}'.")
        return

    print(criar_gerador(formato).render(resultado))


def salvar_relatorio(resultado):
    formato = _ler_entrada("Formato (texto/json/csv) [texto]: ", "texto") or "texto"

    if formato not in FORMATOS_VALIDOS:
        print(f"Formato inválido: '{formato}'.")
        return

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
    ultimos_caminhos = None

    while True:
        print("\n=== DataProcessor — Menu ===")
        print("1. Processar dados")
        print("2. Exibir relatório")
        print("3. Salvar relatório em arquivo")
        print("4. Reprocessar com os últimos caminhos usados")
        print("5. Sair")

        opcao = _ler_entrada("Escolha uma opção: ")
        opcoes_validas = {"1", "2", "3", "4", "5"}

        if opcao not in opcoes_validas:
            print(f"Opção inválida: '{opcao}'. Escolha 1, 2, 3, 4 ou 5.")
            continue

        if opcao == "1":
            caminhos = _ler_caminhos()
            novo_resultado = processar(caminhos)

            if novo_resultado is not None:
                resultado = novo_resultado
                ultimos_caminhos = caminhos

        elif opcao == "2":
            if resultado is None:
                print("Nenhum dado processado ainda. Escolha a opção 1 primeiro.")
                continue

            exibir_relatorio(resultado)

        elif opcao == "3":
            if resultado is None:
                print("Nenhum dado processado ainda. Escolha a opção 1 primeiro.")
                continue

            salvar_relatorio(resultado)

        elif opcao == "4":
            if ultimos_caminhos is None:
                print("Nenhum processamento bem-sucedido ainda. Escolha a opção 1 primeiro.")
                continue

            novo_resultado = processar(ultimos_caminhos)

            if novo_resultado is not None:
                resultado = novo_resultado

        elif opcao == "5":
            break

    return 0


if __name__ == "__main__":
    raise SystemExit(menu_principal())
