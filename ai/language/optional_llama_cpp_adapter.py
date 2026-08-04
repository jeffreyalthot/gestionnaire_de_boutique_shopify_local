from pathlib import Path
class OptionalLlamaCppAdapter:
    def __init__(self,model_path: Path,context_size: int=256) -> None:
        try:
            from llama_cpp import Llama
        except ImportError as exc:
            raise RuntimeError("Installez llama-cpp-python uniquement si le micro-LLM est activé.") from exc
        self.model=Llama(model_path=str(model_path),n_ctx=context_size,n_threads=1,verbose=False)
    def complete(self,prompt: str,max_tokens: int=128) -> str:
        result=self.model(prompt,max_tokens=max_tokens,temperature=0.2,top_p=0.9)
        return str(result["choices"][0]["text"]).strip()
