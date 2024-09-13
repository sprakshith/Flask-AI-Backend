import os
from openai import OpenAI
from langchain_community.llms import Ollama
from agents.language_models.llm_base import BaseLLM
from langchain_community.chat_message_histories import ChatMessageHistory


class OpenAIClient(BaseLLM):
    def __init__(self, model_name: str, api_key: str, base_url: str):
        super().__init__(model_name, False)
        self.api_key = api_key
        self.base_url = base_url
        self.model = self._initiate_llm()

    def _initiate_llm(self):
        return OpenAI(api_key=self.api_key, base_url=self.base_url)

    def run(self, system_message: str, human_message: str, history: ChatMessageHistory,  **kwargs):
        request, history = self.create_request(system_message, human_message, history, **kwargs)

        if 'temperature' not in kwargs:
            kwargs['temperature'] = 0.2

        messages = [{"role": "system", "content": request[0].content}]

        for index, message in enumerate(request[1:]):
            if index % 2 == 0:
                messages.append({"role": "user", "content": message.content})
            else:
                messages.append({"role": "assistant", "content": message.content})

        response = self.model.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=kwargs['temperature'],
            max_tokens=8192
        )

        return response.choices[0].message.content, history
