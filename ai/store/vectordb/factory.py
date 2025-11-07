from typing import Literal
from .interface import BaseVectorDB
from .providers import ChromaDB


class VectorDBFactory:
    def __init__(self, settings):
        self.settings = settings

    def create(self, provider: Literal["chroma"]) -> BaseVectorDB:
        if provider.lower() == "chroma":
            return ChromaDB(settings=self.settings)
        else:
            raise ValueError(f"Unknown provider: {provider}")
