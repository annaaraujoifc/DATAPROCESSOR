import argparse,logging
from pathlib import Path
from .infra.fontes import FonteDadosArquivos
from .infra.relatorios import criar_gerador
from .services.processamento import executar_processamento

def configurar_parser():
 p=argparse.ArgumentParser(description="Processa clientes e transações.");p.add_argument("--clientes",required=True);p.add_argument("--transacoes",required=True);p.add_argument("--config",required=True);p.add_argument("--formato",choices=("texto","json","csv"),default="texto");p.add_argument("--output",type=Path,default=Path("output"));return p
def main(argv=None):
 a=configurar_parser().parse_args(argv);a.output.mkdir(parents=True,exist_ok=True);logging.basicConfig(filename=a.output/"dataprocessor.log",level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s")
 try:
  r=executar_processamento(FonteDadosArquivos(a.clientes,a.transacoes,a.config));relatorio=criar_gerador(a.formato).render(r);nome="relatorio.txt" if a.formato=="texto" else f"relatorio.{a.formato}";(a.output/nome).write_text(relatorio,encoding="utf-8");print(relatorio,end="");return 0
 except (OSError,ValueError,KeyError) as erro:logging.exception("Falha no processamento");print(f"[ERRO] {erro}");return 1
