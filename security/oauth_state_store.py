from __future__ import annotations

import hashlib, secrets
from datetime import datetime, timedelta, timezone
from infrastructure.database.engine import Database, utcnow


class OAuthStateStore:
    def __init__(self, db: Database, ttl_seconds: int=600) -> None: self.db=db; self.ttl=max(60,ttl_seconds)
    @staticmethod
    def _hash(state: str) -> str: return hashlib.sha256(state.encode()).hexdigest()
    def issue(self, provider: str, redirect_uri: str="") -> str:
        state=secrets.token_urlsafe(32); expires=(datetime.now(timezone.utc)+timedelta(seconds=self.ttl)).isoformat()
        self.db.execute("INSERT INTO oauth_states(state_hash,provider,redirect_uri,created_at,expires_at) VALUES(?,?,?,?,?)",(self._hash(state),provider,redirect_uri,utcnow(),expires)); return state
    def consume(self, state: str, provider: str) -> bool:
        now=utcnow(); return self.db.execute("UPDATE oauth_states SET consumed_at=? WHERE state_hash=? AND provider=? AND consumed_at IS NULL AND expires_at>=?",(now,self._hash(state),provider,now))==1
