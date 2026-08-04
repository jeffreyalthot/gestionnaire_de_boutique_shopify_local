from decimal import Decimal
import httpx
class BankOfCanadaRateProvider:
    async def rate(self,source: str,target: str) -> Decimal:
        if source==target: return Decimal("1")
        series=f"FX{source}{target}"
        url=f"https://www.bankofcanada.ca/valet/observations/{series}/json?recent=1"
        async with httpx.AsyncClient(timeout=15) as client:
            response=await client.get(url); response.raise_for_status(); payload=response.json()
        observations=payload.get("observations",[])
        if not observations: raise RuntimeError(f"Taux {series} indisponible.")
        return Decimal(str(observations[-1][series]["v"]))
