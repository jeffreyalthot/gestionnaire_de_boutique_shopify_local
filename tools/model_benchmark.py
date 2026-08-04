from time import perf_counter
from ai.models.product_ranker import product_rank
def run(iterations: int=100000) -> dict[str,float]:
    features={"quality":0.9,"supplier":0.8,"margin":0.5,"stock":0.7,"delivery":0.8,"demand":0.6}
    started=perf_counter()
    for _ in range(iterations): product_rank(features)
    elapsed=perf_counter()-started
    return {"iterations":iterations,"seconds":elapsed,"per_second":iterations/max(elapsed,1e-9)}
if __name__=="__main__": print(run())
