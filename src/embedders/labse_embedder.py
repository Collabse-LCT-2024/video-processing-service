from typing import List

import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch


class LabseEmbedder:
    def __init__(self, model_name: str = "cointegrated/LaBSE-en-ru"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = AutoModel.from_pretrained(model_name).to(self.device)

    def _tokenize_batch(self, texts: List[str]) -> dict:
        return self.tokenizer(
            texts, padding=True, truncation=True, max_length=64, return_tensors="pt"
        )

    def _embed(self, encoded_input: dict) -> torch.Tensor:
        with torch.no_grad():
            model_output = self.model(
                **{k: v.to(self.device) for k, v in encoded_input.items()}
            )
            embeddings = model_output.pooler_output
            embeddings = torch.nn.functional.normalize(embeddings)
        return embeddings

    def embed(self, texts: List[str]) -> np.ndarray:
        encoded_input = self._tokenize_batch(texts)
        embeddings = self._embed(encoded_input)
        return embeddings.cpu().numpy().mean(dim=0)
