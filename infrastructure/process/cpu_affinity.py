from __future__ import annotations
import psutil
class CpuAffinity:
    @staticmethod
    def limit(max_cpus: int=2)->list[int]:
        process=psutil.Process(); available=process.cpu_affinity() if hasattr(process,'cpu_affinity') else list(range(psutil.cpu_count() or 1)); selected=available[:max(1,min(max_cpus,2))]
        if hasattr(process,'cpu_affinity'): process.cpu_affinity(selected)
        return selected
