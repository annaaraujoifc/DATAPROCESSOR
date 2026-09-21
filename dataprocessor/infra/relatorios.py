from abc import ABC,abstractmethod
import csv,io,json
from ..core.resultados import ResultadoProcessamento
class GeradorRelatorio(ABC):
 @abstractmethod
 def render(self,resultado: ResultadoProcessamento)->str:...
class RelatorioTexto(GeradorRelatorio):
 def render(self,resultado):return "\n".join(["=== DataProcessor CLI ===","","[VALIDAÇÃO]",f"Clientes válidos: {len(resultado.clientes)}",f"Clientes inválidos: {len(resultado.clientes_invalidos)}",f"Transações válidas: {len(resultado.transacoes)}",f"Transações inválidas: {len(resultado.transacoes_invalidas)}","","[RELATÓRIO]",f"Média de idade: {resultado.media_idade:.1f}",f"Total aprovado: R$ {resultado.total_aprovado:.2f}"])
class RelatorioJson(GeradorRelatorio):
 def render(self,resultado):return json.dumps(resultado.to_dict(),ensure_ascii=False,indent=2)+"\n"
class RelatorioCsv(GeradorRelatorio):
 def render(self,resultado):
  arquivo=io.StringIO();escritor=csv.writer(arquivo,lineterminator="\n");escritor.writerow(("id","nome","email","idade","cidade","data_cadastro"))
  for c in resultado.clientes:escritor.writerow((c.id,c.nome,c.email,c.idade,c.cidade,c.data_cadastro))
  return arquivo.getvalue()
def criar_gerador(formato):return {"texto":RelatorioTexto,"json":RelatorioJson,"csv":RelatorioCsv}[formato]()
