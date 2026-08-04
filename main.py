from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Shopify-Alibaba Terminal Orchestrator")
    p.add_argument("--validate", action="store_true", help="Valide la configuration, la base et la sécurité.")
    p.add_argument("--once", action="store_true", help="Exécute un cycle puis quitte.")
    p.add_argument("--no-dashboard", action="store_true", help="Désactive le dashboard terminal.")
    p.add_argument("--no-api", action="store_true", help="Désactive le serveur HTTP interne.")
    p.add_argument(
        "--native-terminal",
        action="store_true",
        help="Lance le terminal C++17 à faible consommation de ressources.",
    )
    p.add_argument(
        "--native-live",
        action="store_true",
        help="Demande le mode natif live; les actions sensibles exigent toujours une approbation.",
    )
    return p


def native_executable() -> Path | None:
    executable_name = "shopify_alibaba_terminal.exe" if __import__("os").name == "nt" else "shopify_alibaba_terminal"
    candidates = (
        PROJECT_ROOT / "build" / "windows-msys2-mingw64" / executable_name,
        PROJECT_ROOT / "build" / "portable-release" / executable_name,
        PROJECT_ROOT / "build" / "native-validation" / executable_name,
        PROJECT_ROOT / "build" / "native-max" / executable_name,
    )
    return next((candidate for candidate in candidates if candidate.is_file()), None)


def run_native_terminal(live: bool) -> int:
    executable = native_executable()
    if executable is None:
        print(
            "Exécutable natif introuvable. Sous MSYS2 MINGW64, exécutez :\n"
            "  bash scripts/windows/build_msys2_mingw64.sh",
        )
        return 3
    mode = "--live" if live else "--dry-run"
    plan_directory = PROJECT_ROOT / "data" / "native_plans" / "pending"
    return subprocess.run(
        [str(executable), mode, "--plan-dir", str(plan_directory)],
        cwd=PROJECT_ROOT,
        check=False,
    ).returncode


async def async_main(args: argparse.Namespace) -> int:
    if args.native_terminal or args.native_live:
        return await asyncio.to_thread(run_native_terminal, args.native_live)

    from app.bootstrap import bootstrap
    from app.startup_checks import run_startup_checks

    app = bootstrap()
    if args.validate:
        result = run_startup_checks(app.settings, app.container.db, PROJECT_ROOT)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        await app.container.close()
        return 0 if result["ok"] else 2
    if args.once:
        print(json.dumps(await app.run_once(), ensure_ascii=False, indent=2, default=str))
        await app.container.close()
        return 0
    await app.run(with_dashboard=not args.no_dashboard, with_api=not args.no_api)
    return 0


def cli() -> None:
    raise SystemExit(asyncio.run(async_main(parser().parse_args())))


if __name__ == "__main__":
    cli()
