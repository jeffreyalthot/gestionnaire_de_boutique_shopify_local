from __future__ import annotations
class MediaRightsMapper:
    def map(self,record: dict)->str:
        if record.get('authorized') is True:return 'authorized'
        if record.get('license') in {'supplier','commercial','owned'}:return 'authorized'
        if record.get('license') in {'restricted','editorial'}:return 'restricted'
        return 'unverified'
