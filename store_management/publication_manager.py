from store_management.mutation_plan import MutationPlan
class PublicationManager:
    def plan(self,product_ids: list[str],channel_ids: list[str],publish: bool=True) -> tuple[dict[str,object],...]:
        products=tuple(dict.fromkeys(x.strip() for x in product_ids if x.strip()));channels=tuple(dict.fromkeys(x.strip() for x in channel_ids if x.strip()))
        return tuple(MutationPlan("publication","publish" if publish else "unpublish",{"product_id":p,"channel_id":c,"publish":bool(publish)},approval_required=bool(publish)).to_dict() for p in products for c in channels)
