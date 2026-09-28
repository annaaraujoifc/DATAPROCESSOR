import unittest

from dataprocessor.core.entidades import Cliente, Transacao


class EntidadesTestCase(unittest.TestCase):
    def test_cliente_exibe_identificacao_derivada(self):
        cliente = Cliente(5, "Pedro Santos", "", 38, "Sao Paulo", "2023-02-30")
        self.assertEqual(cliente.identificacao, "#5 Pedro Santos")

    def test_transacao_informa_se_foi_aprovada(self):
        transacao = Transacao(1, 1, 150.50, "eletronicos", "2023-05-10", "aprovado")
        self.assertTrue(transacao.esta_aprovada)

    def test_entidades_sao_imutaveis(self):
        cliente = Cliente(1, "Joao", "joao@email.com", 30, "Joinville", "2023-01-01")
        with self.assertRaises(AttributeError):
            cliente.nome = "Outro nome"


if __name__ == "__main__":
    unittest.main()
