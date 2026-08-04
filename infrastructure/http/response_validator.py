from __future__ import annotations
from typing import Any
class ResponseValidationError(ValueError): pass
class ResponseValidator:
    def require_mapping(self,value: Any,required: tuple[str,...]=())->dict[str,Any]:
        if not isinstance(value,dict): raise ResponseValidationError('Objet JSON attendu.')
        missing=[key for key in required if key not in value]
        if missing: raise ResponseValidationError(f"Champs manquants: {', '.join(missing)}")
        return value
