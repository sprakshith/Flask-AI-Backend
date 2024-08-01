import os
import re
from agents.language_models.llm_base import BaseLLM
from langchain.output_parsers import PydanticOutputParser
from agents.code_writer.code_writer import FlaskAppWriter
from agents.code_optimizer.code_optimizer import CodeOptimizer
from agents.output_models.models import ListOfFlaskAPIEndpoints
from agents.prompts.prompt_reader import BackendDeveloperAgentPrompts
from database.utils import ModelClassUtils, UserStoryUtils, ProjectUtils, ApplicationRequirementsUtils
from database.utils import APIEndpointSchemasUtils, APIEndpointCodeUtils
from langchain_community.chat_message_histories import ChatMessageHistory

ALL_PROJECTS_PATH = os.getenv("ALL_PROJECTS_PATH")


class BackendDeveloperAgent(BackendDeveloperAgentPrompts):
    def __init__(self, model: BaseLLM, project_id: int):
        super().__init__()
        self.model = model
        self.project_id = project_id
        self.history = ChatMessageHistory()

    def design_api_endpoints(self):
        system_message = self.API_ENDPOINTS_DESIGN_SYSTEM_MESSAGE
        human_message = self.API_ENDPOINTS_DESIGN_HUMAN_MESSAGE

        parser = PydanticOutputParser(pydantic_object=ListOfFlaskAPIEndpoints)

        model_classes = ModelClassUtils.get_model_classes_by_project_id(self.project_id)
        model_classes = [CodeOptimizer(model_class.code).optimize_classes() for model_class in model_classes]
        model_classes = "\n\n\n".join(model_classes)

        user_stories = UserStoryUtils.get_user_stories_by_project_id(self.project_id)

        for user_story in user_stories:
            response, _ = self.model.run(system_message, human_message, None, user_story=user_story.description, model_classes=model_classes, format_instructions=parser.get_format_instructions())

            endpoints = parser.parse(response).endpoints

            for endpoint in endpoints:
                APIEndpointSchemasUtils.create_api_endpoint_schema(project_id=self.project_id, user_story_count=user_story.user_story_count, json_schema_design=endpoint.json(indent=4))

    def generate_api_endpoints(self):
        system_message = self.API_ENDPOINTS_GENERATION_SYSTEM_MESSAGE
        human_message = self.API_ENDPOINTS_GENERATION_HUMAN_MESSAGE

        model_classes = ModelClassUtils.get_model_classes_by_project_id(self.project_id)
        model_classes = [CodeOptimizer(model_class.code).optimize_classes() for model_class in model_classes]
        model_classes = "\n\n\n".join(model_classes)

        user_stories = UserStoryUtils.get_user_stories_by_project_id(self.project_id)

        for user_story in user_stories:
            api_endpoints = APIEndpointSchemasUtils.get_api_endpoint_schemas_by_project_id_and_user_story_count(self.project_id, user_story.user_story_count)

            for api_endpoint in api_endpoints:
                response, _ = self.model.run(system_message, human_message, None, user_story=user_story.description, json_schema_design=api_endpoint.json_schema_design, model_classes=model_classes)

                python_code = self.__extract_code(response, 'python')

                APIEndpointCodeUtils.create_api_endpoint_code(project_id=self.project_id, user_story_count=user_story.user_story_count, api_endpoint_schema_id=api_endpoint.id, code=python_code)

    def generate_requirements(self):
        system_message = self.GENERATE_REQUIREMENTS_SYSTEM_MESSAGE
        human_message = self.GENERATE_REQUIREMENTS_HUMAN_MESSAGE

        imports = "from flask import Flask, render_template\n"
        imports += "from flask_cors import CORS\n"

        model_classes = ModelClassUtils.get_model_classes_by_project_id(self.project_id)
        model_classes = "\n\n\n".join([model_class.code for model_class in model_classes])

        all_api_endpoints = APIEndpointCodeUtils.get_api_endpoint_codes_by_project_id(self.project_id)
        api_endpoints = "\n\n\n".join([api_endpoint.code for api_endpoint in all_api_endpoints])

        all_imports = CodeOptimizer(f"{imports}\n\n\n{model_classes}\n\n\n{api_endpoints}").optimize_imports()

        response, _ = self.model.run(system_message, human_message, None, all_imports=all_imports)

        requirements = self.__extract_code(response, 'requirements')

        ApplicationRequirementsUtils.create_application_requirements(project_id=self.project_id, requirements=requirements)

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
