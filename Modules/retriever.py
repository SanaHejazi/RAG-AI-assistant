import numpy as np
from typing import List, Tuple
from Modules.Embedder import EmbeddingEngine

class Retriever:
    def __init__(self, engine: EmbeddingEngine, k: int = 4):
        if engine is None:
            raise ValueError("Embedding engine must not be None")
        self.engine = engine
        self.k = k

    def search(self, query: str) -> List[Tuple[str, float]]:

        q_emb = np.asarray(self.engine.embed_text(query), dtype=np.float32)
        if q_emb.ndim == 1:
            q_emb = q_emb[np.newaxis, :]            
        q_emb = np.ascontiguousarray(q_emb)       

        distances, indices = self.engine.index.search(q_emb, self.k)

        hits: List[Tuple[str, float]] = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx == -1:
                continue
            hits.append((self.engine.documents[idx], float(dist)))
        return hits
