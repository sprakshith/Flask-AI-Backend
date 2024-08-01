from abc import ABC, abstractmethod
from langchain.prompts.chat import (AIMessagePromptTemplate,
                                    ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain_community.chat_message_histories import ChatMessageHistory


class BaseLLM(ABC):
    def __init__(self, model_name: str, is_local: bool):
        self.model_name = model_name
        self.is_local = is_local

    @abstractmethod
    def _initiate_llm(self):
        pass

    def create_request(self, system_message: str, human_message: str, history: ChatMessageHistory,  **kwargs):

        request = None

        if history is None or len(history.messages) == 0:
            template_messages = [SystemMessagePromptTemplate.from_template(system_message), human_message]
            prompt_template = ChatPromptTemplate.from_messages(template_messages)
            request = prompt_template.format_prompt(**kwargs).to_messages()

            if history is not None:
                history.add_user_message(request[-1])
        else:
            template_messages = [SystemMessagePromptTemplate.from_template(system_message)]

            for count, message in enumerate(history.messages):
                if count % 2 == 0:
                    template_messages.append(HumanMessagePromptTemplate.from_template(message.content))
                else:
                    template_messages.append(AIMessagePromptTemplate.from_template(message.content))

            template_messages.append(human_message)

            prompt_template = ChatPromptTemplate.from_messages(template_messages)
            request = prompt_template.format_prompt(**kwargs).to_messages()

            history.add_user_message(request[-1])

        return prompt_template.format_prompt(**kwargs).to_messages(), history

    @abstractmethod
    def run(self, system_message: str, human_message: str, history: ChatMessageHistory,  **kwargs):
        pass
