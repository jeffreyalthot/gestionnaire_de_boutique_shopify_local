from store_management.menu_manager import MenuManager
from store_management.mutation_plan import MutationPlan
class NavigationManager(MenuManager):
    def plan(self,title: str,items: list[dict[str,object]],max_depth: int=3) -> MutationPlan:
        issues=self.validate(items,max_depth)
        return MutationPlan("navigation","upsert",{"title":title.strip(),"items":items},safe=not issues,approval_required=True,warnings=issues)
