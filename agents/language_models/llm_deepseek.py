import os
from openai import OpenAI
from langchain_community.llms import Ollama
from agents.language_models.llm_base import BaseLLM
from langchain_community.chat_message_histories import ChatMessageHistory

DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]
BASE_URL = "https://api.deepseek.com/v1"


class DeepseekCoder(BaseLLM):
    def __init__(self, model_name: str = 'deepseek-coder:6.7b-instruct', is_local: bool = True):
        super().__init__(model_name, is_local)
        self.model = self._initiate_llm()

    def _initiate_llm(self):
        if self.is_local:
            return Ollama(model=self.model_name, temperature=0.2)
        else:
            return OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_URL)

    def run(self, system_message: str, human_message: str, history: ChatMessageHistory,  **kwargs):
        request, history = self.create_request(system_message, human_message, history, **kwargs)

        if self.is_local:
            return self.model.invoke(request), history
        else:
            return self.__run_using_openai_client(request), history

    def __run_using_openai_client(self, request, **kwargs):
        if 'temperature' not in kwargs:
            kwargs['temperature'] = 0.2

        messages = [{"role": "system", "content": request[0].content}]

        for index, message in enumerate(request[1:]):
            if index % 2 == 0:
                messages.append({"role": "user", "content": message.content})
            else:
                messages.append({"role": "assistant", "content": message.content})

        response = self.model.chat.completions.create(
            model="deepseek-coder",
            messages=messages,
            temperature=kwargs['temperature']
        )

        return response.choices[0].message.content
