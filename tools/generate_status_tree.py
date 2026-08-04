from __future__ import annotations
import argparse,ast,json
from dataclasses import asdict,dataclass
from pathlib import Path

LEGEND={"✅":"COMPLET — implémentation substantielle et syntaxe valide","🧪":"TEST — fichier de test exécutable","🛠":"DÉVELOPPÉ — logique réelle présente, approfondissement encore possible","🔗":"INTÉGRATION — contrat/connecteur/configuration relié au runtime","📚":"DOCUMENTATION — documentation ou procédure opérationnelle","📦":"ARTEFACT — paquet généré ou fichier de distribution","📁":"DONNÉES — répertoire de données, cache ou fichier sentinelle","⚠":"À APPROFONDIR — fichier très court ou contenant une implémentation minimale","❌":"ERREUR — syntaxe invalide ou fichier illisible"}
@dataclass(frozen=True,slots=True)
class FileStatus:
    path:str;status:str;label:str;lines:int;code_lines:int;reason:str

def classify(root: Path,p: Path)->FileStatus:
    rel=p.relative_to(root).as_posix();suffix=p.suffix.lower();lines=code=0;reason=""
    try:text=p.read_text(encoding="utf-8",errors="strict");rows=text.splitlines();lines=len(rows);code=sum(bool(r.strip()) and not r.lstrip().startswith("#") for r in rows)
    except (UnicodeDecodeError,OSError):text=""
    if "tests/" in f"{rel}/" or p.name.startswith("test_"):symbol,label="🧪","TEST";reason="test automatisé"
    elif suffix==".py":
        try:tree=ast.parse(text)
        except SyntaxError:symbol,label="❌","ERREUR";reason="syntaxe Python invalide"
        else:
            definitions=sum(isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) for node in tree.body)
            assignments=sum(isinstance(node,(ast.Assign,ast.AnnAssign)) for node in tree.body)
            imports=sum(isinstance(node,(ast.Import,ast.ImportFrom)) for node in tree.body)
            has_unfinished=any(isinstance(node,ast.Pass) or (isinstance(node,ast.Constant) and node.value is Ellipsis) for node in ast.walk(tree)) or "NotImplementedError" in text
            if p.name=="__init__.py":symbol,label="🔗","INTÉGRATION";reason="surface de paquet"
            elif code>=35:symbol,label="✅","COMPLET";reason="module substantiel"
            elif has_unfinished and definitions==0:symbol,label="⚠","À APPROFONDIR";reason="implémentation incomplète"
            elif code>=8 or definitions or assignments:symbol,label="🛠","DÉVELOPPÉ";reason="logique ou adaptateur fonctionnel"
            elif imports:symbol,label="🔗","INTÉGRATION";reason="pont de compatibilité"
            else:symbol,label="⚠","À APPROFONDIR";reason="module minimal"
    elif suffix in {".cpp",".h",".hpp",".cxx"}:symbol,label=("✅","COMPLET") if code>=25 else ("🛠","DÉVELOPPÉ");reason="composant natif"
    elif suffix in {".yaml",".yml",".json",".toml",".graphql",".sql",".xml"}:symbol,label="🔗","INTÉGRATION";reason="contrat ou configuration"
    elif suffix in {".md",".rst",".txt"} and p.name not in {"VERSION"}:symbol,label="📚","DOCUMENTATION";reason="documentation"
    elif suffix in {".whl",".zip"}:symbol,label="📦","ARTEFACT";reason="distribution"
    elif p.name==".gitkeep" or "data/" in f"{rel}/":symbol,label="📁","DONNÉES";reason="donnée ou sentinelle"
    else:symbol,label="🔗","INTÉGRATION";reason="ressource du projet"
    return FileStatus(rel,symbol,label,lines,code,reason)

def generate(root: Path,output: Path,json_output: Path|None=None)->dict[str,object]:
    statuses={s.path:s for s in (classify(root,p) for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts and ".pytest_cache" not in p.parts)}
    counts={}
    for s in statuses.values():counts[s.status]=counts.get(s.status,0)+1
    out=["LÉGENDE DES STATUTS DE DÉVELOPPEMENT"]+[f"{k} {v}" for k,v in LEGEND.items()]+["",f"RACINE: {root.name}",f"FICHIERS: {len(statuses)}",""]
    def walk(path: Path,prefix=""):
        entries=sorted([x for x in path.iterdir() if x.name not in {"__pycache__",".pytest_cache"}],key=lambda x:(not x.is_dir(),x.name.lower()))
        for index,item in enumerate(entries):
            last=index==len(entries)-1;connector="└── " if last else "├── ";rel=item.relative_to(root).as_posix()
            if item.is_dir():out.append(prefix+connector+item.name+"/");walk(item,prefix+("    " if last else "│   "))
            else:
                s=statuses[rel];out.append(prefix+connector+f"{item.name}  {s.status} {s.label} | code={s.code_lines} lignes={s.lines}")
    walk(root);output.write_text("\n".join(out)+"\n",encoding="utf-8")
    report={"root":root.name,"files":len(statuses),"counts":counts,"legend":LEGEND,"files_status":[asdict(s) for s in statuses.values()]}
    if json_output:json_output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return report

def main():
    parser=argparse.ArgumentParser();parser.add_argument("root",nargs="?",default=".");parser.add_argument("--output",default="PROJECT_TREE_STATUS.txt");parser.add_argument("--json",default="PROJECT_FILE_STATUS.json");args=parser.parse_args();root=Path(args.root).resolve();generate(root,Path(args.output),Path(args.json))
if __name__=="__main__":main()
