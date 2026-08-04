from pathlib import Path
import shutil
from config.paths import ensure_runtime_directories,PROJECT_ROOT
def run() -> None:
    ensure_runtime_directories()
    env=PROJECT_ROOT/".env"
    if not env.exists(): shutil.copy2(PROJECT_ROOT/".env.example",env)
    print(f"Projet initialisé dans {PROJECT_ROOT}")
if __name__=="__main__": run()
