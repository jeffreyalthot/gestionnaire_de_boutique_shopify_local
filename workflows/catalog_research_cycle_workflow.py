from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class CatalogResearchCycleWorkflow(BaseWorkflow):
    name = 'catalog_research_cycle'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('build_search_plan', self._step_0_build_search_plan, mutating=False, approval_required=False),
            WorkflowStep('discover_candidates', self._step_1_discover_candidates, mutating=False, approval_required=False),
            WorkflowStep('score_candidates', self._step_2_score_candidates, mutating=False, approval_required=False),
            WorkflowStep('persist_shortlist', self._step_3_persist_shortlist, mutating=True, approval_required=False),
        )

    def _step_0_build_search_plan(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'queries': tuple(ctx.get('queries', ())), 'candidate_limit': int(ctx.get('candidate_limit', 100))}

    def _step_1_discover_candidates(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'candidates_discovered': int(ctx.get('candidate_count', 0))}

    def _step_2_score_candidates(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'candidates_scored': int(ctx.get('candidates_discovered', 0))}

    def _step_3_persist_shortlist(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'shortlisted': min(int(ctx.get('candidates_scored', 0)), int(ctx.get('shortlist_limit', 20)))}

