import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from dataprocessor.interfaces.menu import processar_caminhos


class ProcessarCaminhosTestCase(unittest.TestCase):
    def test_processa_dataset_padrao(self):
        resultado = processar_caminhos(
            "data/clientes.csv",
            "data/transacoes.csv",
            "data/config.json",
        )
        self.assertEqual(resultado.total_aprovado, 150.50)

    def test_processar_caminhos_e_main_produzem_mesmo_total_aprovado(self):
        resultado_menu = processar_caminhos(
            "data/clientes.csv",
            "data/transacoes.csv",
            "data/config.json",
        )

        with tempfile.TemporaryDirectory() as diretorio:
            processo = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataprocessor",
                    "--clientes",
                    "data/clientes.csv",
                    "--transacoes",
                    "data/transacoes.csv",
                    "--config",
                    "data/config.json",
                    "--formato",
                    "json",
                    "--output",
                    diretorio,
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(processo.returncode, 0, processo.stderr)

            relatorio = json.loads(
                Path(diretorio, "relatorio.json").read_text(encoding="utf-8")
            )

        self.assertEqual(
            resultado_menu.total_aprovado,
            relatorio["metricas"]["total_aprovado"],
        )


if __name__ == "__main__":
    unittest.main()
