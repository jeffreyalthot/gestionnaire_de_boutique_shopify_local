from __future__ import annotations
import os
class ThreadLimiter:
    VARIABLES=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
    @classmethod
    def apply(cls,threads: int=1)->dict[str,str]:
        value=str(max(1,min(threads,2)))
        for key in cls.VARIABLES: os.environ[key]=value
        return {key:os.environ[key] for key in cls.VARIABLES}
