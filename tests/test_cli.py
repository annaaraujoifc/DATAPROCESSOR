import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from dataprocessor.interfaces.menu import processar_caminhos


class CliTestCase(unittest.TestCase):
    def test_cli_salva_relatorio_json_e_log(self):
        projeto = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as pasta:
            saida = Path(pasta)
            processo = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataprocessor",
                    "--clientes",
                    str(projeto / "data/clientes.csv"),
                    "--transacoes",
                    str(projeto / "data/transacoes.csv"),
                    "--config",
                    str(projeto / "data/config.json"),
                    "--formato",
                    "json",
                    "--output",
                    str(saida),
                ],
                cwd=projeto,
                capture_output=True,
                text=True,
            )

            self.assertEqual(processo.returncode, 0, processo.stderr)
            relatorio = json.loads(
                (saida / "relatorio.json").read_text(encoding="utf-8")
            )
            self.assertEqual(relatorio["metricas"]["total_aprovado"], 150.50)
            self.assertTrue((saida / "dataprocessor.log").exists())

    def test_menu_interativo_sai_sem_erro(self):
        projeto = Path(__file__).resolve().parents[1]
        processo = subprocess.run(
            [sys.executable, "-m", "dataprocessor.interfaces.menu"],
            cwd=projeto,
            input="5\n",
            capture_output=True,
            text=True,
        )

        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertIn("=== DataProcessor — Menu ===", processo.stdout)

    def test_menu_rejeita_diretorio_e_pede_arquivo_valido(self):
        projeto = Path(__file__).resolve().parents[1]
        processo = subprocess.run(
            [
                sys.executable,
                "-m",
                "dataprocessor.interfaces.menu",
            ],
            cwd=projeto,
            input=(
                "1\n"
                "data\n"
                f"{projeto / 'data/clientes.csv'}\n"
                "data\n"
                f"{projeto / 'data/transacoes.csv'}\n"
                "data\n"
                f"{projeto / 'data/config.json'}\n"
                "5\n"
            ),
            capture_output=True,
            text=True,
        )

        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertIn("é um diretório. Informe o caminho do arquivo.", processo.stdout)
        self.assertIn("Clientes válidos:", processo.stdout)

    def test_menu_impede_relatorio_antes_do_processamento(self):
        projeto = Path(__file__).resolve().parents[1]
        processo = subprocess.run(
            [sys.executable, "-m", "dataprocessor.interfaces.menu"],
            cwd=projeto,
            input="2\n5\n",
            capture_output=True,
            text=True,
        )

        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertIn(
            "Nenhum dado processado ainda. Escolha a opção 1 primeiro.",
            processo.stdout,
        )

    def test_menu_rejeita_opcao_invalida(self):
        projeto = Path(__file__).resolve().parents[1]
        processo = subprocess.run(
            [sys.executable, "-m", "dataprocessor.interfaces.menu"],
            cwd=projeto,
            input="9\n5\n",
            capture_output=True,
            text=True,
        )

        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertIn("Opção inválida: '9'.", processo.stdout)

    def test_menu_mantem_resultado_apos_falha_de_processamento(self):
        projeto = Path(__file__).resolve().parents[1]
        processo = subprocess.run(
            [sys.executable, "-m", "dataprocessor.interfaces.menu"],
            cwd=projeto,
            input=(
                "1\n"
                "arquivo-inexistente.csv\n"
                "data/transacoes.csv\n"
                "data/config.json\n"
                "1\n"
                "data/clientes.csv\n"
                "data/transacoes.csv\n"
                "data/config.json\n"
                "1\n"
                "arquivo-inexistente.csv\n"
                "data/transacoes.csv\n"
                "data/config.json\n"
                "2\n"
                "xml\n"
                "5\n"
            ),
            capture_output=True,
            text=True,
        )

        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertIn("[ERRO] Não foi possível processar:", processo.stdout)
        self.assertIn("Clientes válidos:", processo.stdout)
        self.assertIn("Formato inválido: 'xml'.", processo.stdout)

    def test_menu_reprocessa_com_ultimos_caminhos(self):
        projeto = Path(__file__).resolve().parents[1]
        processo = subprocess.run(
            [sys.executable, "-m", "dataprocessor.interfaces.menu"],
            cwd=projeto,
            input=(
                "1\n"
                "data/clientes.csv\n"
                "data/transacoes.csv\n"
                "data/config.json\n"
                "4\n"
                "5\n"
            ),
            capture_output=True,
            text=True,
        )

        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertGreaterEqual(processo.stdout.count("Clientes válidos:"), 2)


    def test_processar_caminhos_tem_mesmo_total_aprovado_da_cli(self):
        projeto = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as pasta:
            processo = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataprocessor",
                    "--clientes",
                    str(projeto / "data/clientes.csv"),
                    "--transacoes",
                    str(projeto / "data/transacoes.csv"),
                    "--config",
                    str(projeto / "data/config.json"),
                    "--formato",
                    "json",
                    "--output",
                    pasta,
                ],
                cwd=projeto,
                capture_output=True,
                text=True,
            )

            self.assertEqual(processo.returncode, 0, processo.stderr)
            relatorio = json.loads(
                (Path(pasta) / "relatorio.json").read_text(encoding="utf-8")
            )
            resultado = processar_caminhos(
                str(projeto / "data/clientes.csv"),
                str(projeto / "data/transacoes.csv"),
                str(projeto / "data/config.json"),
            )

            self.assertEqual(
                resultado.total_aprovado,
                relatorio["metricas"]["total_aprovado"],
            )


if __name__ == "__main__":
    unittest.main()
