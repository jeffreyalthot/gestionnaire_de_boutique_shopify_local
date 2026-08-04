from __future__ import annotations

import hashlib
from uuid import uuid4
from infrastructure.database.engine import Database, utcnow


class CredentialRotation:
    def __init__(self, db: Database) -> None: self.db=db
    def register(self, provider: str, key_name: str, secret: str) -> str:
        fingerprint=hashlib.sha256(secret.encode()).hexdigest(); row_id=str(uuid4())
        with self.db.transaction() as conn:
            conn.execute("UPDATE credential_versions SET status='retired',retired_at=? WHERE provider=? AND key_name=? AND status='active'",(utcnow(),provider,key_name))
            conn.execute("INSERT INTO credential_versions(id,provider,key_name,fingerprint,status,created_at) VALUES(?,?,?,?,?,?)",(row_id,provider,key_name,fingerprint,"active",utcnow()))
        return row_id
