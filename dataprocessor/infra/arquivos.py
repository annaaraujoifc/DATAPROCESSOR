import csv,json
from pathlib import Path
from ..core.entidades import Cliente,Transacao

def _para_int(valor: str,padrao: int|None=None)->int|None:
    try:return int(valor)
    except (TypeError,ValueError):return padrao
def _para_float(valor: str,padrao: float|None=None)->float|None:
    try:return float(valor)
    except (TypeError,ValueError):return padrao
def carregar_clientes(caminho: str|Path)->list[Cliente]:
    with Path(caminho).open(encoding="utf-8",newline="") as arquivo:
        leitor=csv.DictReader(arquivo)
        return [Cliente(_para_int(l.get("id","")),l.get("nome","").strip(),l.get("email","").strip(),_para_int(l.get("idade","")),l.get("cidade","").strip(),l.get("data_cadastro","").strip()) for l in leitor]
def carregar_transacoes(caminho: str|Path)->list[Transacao]:
    with Path(caminho).open(encoding="utf-8",newline="") as arquivo:
        leitor=csv.DictReader(arquivo)
        return [Transacao(_para_int(l.get("id","")),_para_int(l.get("cliente_id","")),_para_float(l.get("valor","")),l.get("categoria","").strip(),l.get("data","").strip(),l.get("status","").strip()) for l in leitor]
def carregar_config(caminho: str|Path)->dict:
    with Path(caminho).open(encoding="utf-8") as arquivo:return json.load(arquivo)
