from langchain_community.llms import Ollama
from agents.language_models.llm_base import BaseLLM
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_community.chat_message_histories import ChatMessageHistory


class Mistral(BaseLLM):
    def __init__(self, model_name: str = 'mistral:7b-instruct', is_local: bool = True):
        super().__init__(model_name, is_local)
        self.model = self._initiate_llm()

    def _initiate_llm(self):
        if self.is_local:
            return Ollama(model=self.model_name, temperature=0.2)
        else:
            return ChatMistralAI(model=self.model_name, temperature=0.2)

    def run(self, system_message: str, human_message: str, history: ChatMessageHistory,  **kwargs):
        request, history = self.create_request(system_message, human_message, history, **kwargs)

        if self.is_local:
            return self.model.invoke(request), history
        else:
            return self.model.invoke(request).content, history
