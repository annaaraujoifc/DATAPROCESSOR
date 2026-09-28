import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


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
            input="4\n",
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
                "4\n"
            ),
            capture_output=True,
            text=True,
        )

        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertIn("é um diretório. Informe o caminho do arquivo.", processo.stdout)


if __name__ == "__main__":
    unittest.main()
