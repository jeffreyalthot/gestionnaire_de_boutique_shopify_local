from pathlib import Path
import hashlib,json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve(); manifest=json.loads((root/"MANIFEST.json").read_text(encoding="utf-8")); errors=[]
for item in manifest["files"]:
    p=root/item["path"]
    if not p.is_file(): errors.append(f"missing:{item['path']}"); continue
    if hashlib.sha256(p.read_bytes()).hexdigest()!=item["sha256"]: errors.append(f"hash:{item['path']}")
print({"ok":not errors,"files":len(manifest["files"]),"errors":errors[:20]})
raise SystemExit(0 if not errors else 1)
