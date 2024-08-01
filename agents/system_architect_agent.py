from agents.tools.tools import get_all_tools
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from agents.prompts.prompt_reader import SystemArchitectAgentPrompts


class SystemArchitectAgent(SystemArchitectAgentPrompts):
    def __init__(self):
        super().__init__()
        self.agent_executor = self.__initiate_agent_executor()

    def __initiate_agent_executor(self):
        memory = SqliteSaver.from_conn_string(":memory:")

        model = ChatMistralAI(model="mistral-large-latest", temperature=0.4)

        tools = get_all_tools()

        system_message = self.SYSTEM_MESSAGE

        return create_react_agent(model, tools, system_message, checkpointer=memory)

    def process_message(self, user_message, current_message_session_id):
        config = {"configurable": {"thread_id": current_message_session_id}}

        return self.agent_executor.invoke({"messages": [HumanMessage(content=user_message)]}, config)['messages'][-1].content
