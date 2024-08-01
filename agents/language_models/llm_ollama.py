from langchain_community.llms import Ollama
from agents.language_models.llm_base import BaseLLM


class OllamaLLM(BaseLLM):
    def __init__(self, model_name):
        super().__init__(model_name, is_local=True)
        self.model = self._initiate_llm()

    def _initiate_llm(self):
        return Ollama(model=self.model_name, temperature=0.2)

    def run(self, system_message: str, human_message: str, **kwargs):
        request = self.create_request(system_message, human_message, **kwargs)
        return self.model.invoke(request)
