from __future__ import annotations
import json
from pathlib import Path
from typing import Any
class ContractValidationError(ValueError):pass
class AlibabaContractValidator:
    def __init__(self,directory: Path|None=None)->None:self.directory=directory or Path(__file__).with_name('contracts')
    def validate(self,name: str,payload: Any)->dict[str,Any]:
        schema=json.loads((self.directory/f'{name}.schema.json').read_text(encoding='utf-8'))
        if not isinstance(payload,dict):raise ContractValidationError('Objet attendu.')
        missing=[k for k in schema.get('required',[]) if k not in payload]
        if missing:raise ContractValidationError(f"Champs manquants: {', '.join(missing)}")
        for key,spec in schema.get('properties',{}).items():
            if key not in payload:continue
            expected=spec.get('type'); value=payload[key]
            mapping={'string':str,'number':(int,float),'integer':int,'array':list,'object':dict,'boolean':bool}
            if expected in mapping and (isinstance(value,bool) and expected in {'number','integer'} or not isinstance(value,mapping[expected])):raise ContractValidationError(f'Type invalide: {key}')
        return payload
