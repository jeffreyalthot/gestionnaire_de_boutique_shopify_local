$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root
$Python = if (Test-Path ".venv\Scripts\python.exe") { ".venv\Scripts\python.exe" } else { "python" }
& $Python main.py --validate
& $Python -m compileall -q .
& $Python -m pytest -q
if (Get-Command cmake -ErrorAction SilentlyContinue) {
  cmake -S . -B build\windows-validation -G Ninja -DCMAKE_BUILD_TYPE=Release
  cmake --build build\windows-validation --parallel 2
  ctest --test-dir build\windows-validation --output-on-failure -j 2
}
