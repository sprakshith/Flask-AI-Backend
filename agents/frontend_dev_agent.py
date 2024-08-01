import os
import re
from agents.language_models.llm_base import BaseLLM
from agents.prompts.prompt_reader import FrontendDeveloperAgentPrompts
from langchain.output_parsers import PydanticOutputParser
from agents.code_writer.code_writer import FlaskAppWriter, FrontendCodeWriter
from agents.code_optimizer.code_optimizer import CodeOptimizer
from agents.output_models.models import ListOfFrontendPages
from agents.prompts.prompt_reader import BackendDeveloperAgentPrompts
from database.utils import UserStoryUtils, FrontendPageUtils, ProjectUtils
from database.utils import APIEndpointSchemasUtils, APIEndpointCodeUtils
from langchain_community.chat_message_histories import ChatMessageHistory

ALL_PROJECTS_PATH = os.getenv("ALL_PROJECTS_PATH")


class FrontendDeveloperAgent(FrontendDeveloperAgentPrompts):
    def __init__(self, model: BaseLLM, project_id: int):
        super().__init__()
        self.model = model
        self.project_id = project_id
        self.history = ChatMessageHistory()

    def design_frontend(self):
        system_message = self.FRONTEND_DESIGN_SYSTEM_MESSAGE
        human_message = self.FRONTEND_DESIGN_HUMAN_MESSAGE

        parser = PydanticOutputParser(pydantic_object=ListOfFrontendPages)

        all_user_stories = UserStoryUtils.get_user_stories_by_project_id(self.project_id)
        user_stories = "\n\n\n".join([user_story.description for user_story in all_user_stories])

        response, _ = self.model.run(system_message, human_message, None, user_stories=user_stories, format_instructions=parser.get_format_instructions())

        frontend_designs = parser.parse(response).pages

        for frontend_design in frontend_designs:
            FrontendPageUtils.create_frontend_page(self.project_id, frontend_design.name, frontend_design.purpose)

    def generate_front_end_code(self):
        frontend_pages = FrontendPageUtils.get_frontend_pages_by_project_id(self.project_id)

        all_user_stories = UserStoryUtils.get_user_stories_by_project_id(self.project_id)
        user_stories = "\n\n\n".join([user_story.description for user_story in all_user_stories])

        all_api_endpoints = APIEndpointCodeUtils.get_api_endpoint_codes_by_project_id(self.project_id)
        api_endpoints = "\n\n\n".join([CodeOptimizer(api_endpoint.code).optimize_functions() for api_endpoint in all_api_endpoints])

        system_message_html = self.GENERATE_HTML_SYSTEM_MESSAGE
        human_message_html = self.GENERATE_HTML_HUMAN_MESSAGE

        system_message_css = self.GENERATE_CSS_SYSTEM_MESSAGE
        human_message_css = self.GENERATE_CSS_HUMAN_MESSAGE

        system_message_js = self.GENERATE_JS_SYSTEM_MESSAGE
        human_message_js = self.GENERATE_JS_HUMAN_MESSAGE

        for frontend_page in frontend_pages:
            response, _ = self.model.run(system_message_html, human_message_html, None, user_stories=user_stories, purpose=frontend_page.purpose)
            html_body_code = self.__extract_code(response, 'html')

            response, _ = self.model.run(system_message_css, human_message_css, None, user_stories=user_stories, html_body_code=html_body_code)
            css_code = self.__extract_code(response, 'css')

            response, _ = self.model.run(system_message_js, human_message_js, None, user_stories=user_stories,
                                         api_endpoints=api_endpoints, html_body_code=html_body_code, purpose=frontend_page.purpose)
            js_code = self.__extract_code(response, 'javascript')

            FrontendPageUtils.update_frontend_page(frontend_page.id, frontend_page.name, frontend_page.purpose, html_body_code, css_code, js_code)

    def __extract_code(self, response: str, code_type: str):
        try:
            match = re.search(f'```{code_type}\n(.*?)```', response, re.DOTALL)

            if match:
                code = match.group(1)
                return code
            else:
                if type(response) == str:
                    return response
        except Exception as e:
            pass

        return f"No {code_type.upper()} code found in the response!"
