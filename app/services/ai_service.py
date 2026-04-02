from functools import lru_cache
import os

from huggingface_hub import InferenceClient

class AiService:
    def __init__(self):
        self._client: InferenceClient = InferenceClient(
                    provider="hf-inference",
                    api_key=os.environ["HF_TOKEN"],
            )
        self._model = os.getenv("HF_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    
    @lru_cache(maxsize=128)
    def encode_skill_name(self, skill_name: str) -> list[float]:
        embedding = self._client.feature_extraction(text=skill_name, model = self._model)
        return embedding.tolist()