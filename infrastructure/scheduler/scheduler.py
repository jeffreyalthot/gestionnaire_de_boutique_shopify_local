from __future__ import annotations
import asyncio,logging
from dataclasses import dataclass
from datetime import datetime,timezone
from time import monotonic
from infrastructure.scheduler.job_registry import JobRegistry,ScheduledJob
logger=logging.getLogger(__name__)
@dataclass(slots=True)
class JobRuntime:
    runs:int=0;failures:int=0;skipped_overlap:int=0;running:bool=False;last_started:str="";last_finished:str="";last_duration_seconds:float=0;last_error:str=""
class AsyncScheduler:
    def __init__(self,registry: JobRegistry) -> None:self.registry=registry;self.stop_event=asyncio.Event();self.runtime={name:JobRuntime() for name in registry.jobs}
    async def _runner(self,job: ScheduledJob) -> None:
        if not job.run_immediately:
            try:await asyncio.wait_for(self.stop_event.wait(),timeout=job.interval_seconds);return
            except asyncio.TimeoutError:pass
        state=self.runtime.setdefault(job.name,JobRuntime())
        while not self.stop_event.is_set():
            if state.running:state.skipped_overlap+=1
            else:
                state.running=True;state.last_started=datetime.now(timezone.utc).isoformat();started=monotonic()
                try:await job.action();state.runs+=1;state.last_error=""
                except asyncio.CancelledError:raise
                except Exception as exc:state.failures+=1;state.last_error=f"{type(exc).__name__}: {exc}"[:1000];logger.exception("Échec du travail planifié %s",job.name)
                finally:state.running=False;state.last_duration_seconds=round(monotonic()-started,6);state.last_finished=datetime.now(timezone.utc).isoformat()
            try:await asyncio.wait_for(self.stop_event.wait(),timeout=job.interval_seconds)
            except asyncio.TimeoutError:continue
    async def run(self) -> None:
        tasks=[asyncio.create_task(self._runner(job),name=f"job:{job.name}") for job in self.registry.jobs.values()]
        try:await self.stop_event.wait()
        finally:
            for task in tasks:task.cancel()
            await asyncio.gather(*tasks,return_exceptions=True)
    def snapshot(self) -> dict[str,dict[str,object]]:return {name:{field:getattr(state,field) for field in state.__dataclass_fields__} for name,state in self.runtime.items()}
    def stop(self) -> None:self.stop_event.set()
