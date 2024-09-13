from langchain_anthropic import ChatAnthropic
from agents.language_models.llm_base import BaseLLM
from langchain_community.chat_message_histories import ChatMessageHistory


class Anthropic(BaseLLM):
    def __init__(self, model_name):
        super().__init__(model_name, False)
        self.model = self._initiate_llm()

    def _initiate_llm(self):
        return ChatAnthropic(model=self.model_name, temperature=0.2)

    def run(self, system_message: str, human_message: str, history: ChatMessageHistory,  **kwargs):
        request, history = self.create_request(system_message, human_message, history, **kwargs)
        return self.model.invoke(request).content, history
