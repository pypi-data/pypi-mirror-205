from typing import List, Dict

import numpy as np
import requests
from pydantic import root_validator

from simplechain.stack.text_embedders.base import TextEmbedder
from simplechain.utils import get_from_dict_or_env


class TextEmbedderAI21(TextEmbedder):
    model_name = "text-embedding-ada-002"

    @root_validator()
    def validate_environment(self, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        ai21_api_key = get_from_dict_or_env(
            values, "ai21_api_key", "AI21_API_KEY"
        )

        values["ai21_api_key"] = ai21_api_key
        self.ai21_api_key = ai21_api_key

        return values

    def embed(self, text: str) -> np.ndarray:
        # Assumes the text is less than 2000 characters
        text = text.replace("\n", " ")
        text = text[:2000]
        response = requests.post('https://api.ai21.com/studio/v1/experimental/embed',
                                 json={'texts': [text]},
                                 headers={'Authorization': f'Bearer {self.ai21_api_key}'})
        embedding = response.json()['results'][0]['embedding']
        return np.array(embedding)

    def embed_all(self, texts: List[str]) -> List[np.ndarray]:
        # Breaks the strings with 2000+ characters into smaller strings
        for i, s in enumerate(texts):
            if len(s) > 2000:
                texts.pop(i)
                for j in range(0, len(s), 2000):
                    texts.insert(i + j, s[j:j + 2000])

        # Post 200 strings at a time
        import requests

        results = []
        texts = [text.replace("\n", " ") for text in texts]
        for i in range(0, len(texts), 200):
            response = requests.post('https://api.ai21.com/studio/v1/experimental/embed',
                                     json={'texts': texts[i:i + 200]},
                                     headers={'Authorization': f'Bearer {self.ai21_api_key}'})
            embeddings = list(map(lambda x: x["embedding"], response.json()['results']))
            results.extend(embeddings)
        return results
