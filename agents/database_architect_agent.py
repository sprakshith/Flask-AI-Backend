import os
import re
import time
from agents.language_models.llm_base import BaseLLM
from agents.code_writer.code_writer import ModelClassesWriter
from agents.prompts.prompt_reader import DatabaseArchitectAgentPrompts
from langchain_community.chat_message_histories import ChatMessageHistory
from database.utils import SchemaDesignUtils, ModelClassUtils, UserStoryUtils, ProjectUtils

ALL_PROJECTS_PATH = os.getenv("ALL_PROJECTS_PATH")


class DatabaseArchitectAgent(DatabaseArchitectAgentPrompts):
    def __init__(self, model: BaseLLM, project_id: int):
        super().__init__()
        self.model = model
        self.project_id = project_id
        self.history = ChatMessageHistory()

    def design_schema(self):
        all_user_stories = UserStoryUtils.get_user_stories_by_project_id(self.project_id)

        for index, user_story in enumerate(all_user_stories):
            latest_schema_design = SchemaDesignUtils.get_latest_schema_design_by_project_id(self.project_id)
            latest_version = 0 if latest_schema_design is None else latest_schema_design.version
            script = latest_schema_design.script if latest_schema_design is not None else "Schema not yet designed!"

            kwargs = {
                "user_story": user_story.description,
                "latest_schema_design": script
            }

            system_message = self.SCHEMA_DESIGN_SYSTEM_MESSAGE

            human_message = self.SCHEMA_DESIGN_HUMAN_MESSAGE if index == 0 else self.SCHEMA_CONTINUATION_HUMAN_MESSAGE

            response, self.history = self.model.run(system_message, human_message, self.history, **kwargs)

            self.history.add_ai_message(response)

            SchemaDesignUtils.create_schema_design(self.project_id, version=latest_version + 1, script=self.__extract_code(response, "sql"))

            time.sleep(0.25)

    def generate_models(self):
        script = SchemaDesignUtils.get_latest_schema_design_by_project_id(self.project_id).script

        all_create_statements = self.__get_create_statements_as_list(script)

        for create_statement in all_create_statements:
            system_message = self.MODEL_GENERATION_SYSTEM_MESSAGE
            human_message = self.MODEL_GENERATION_HUMAN_MESSAGE

            response, _ = self.model.run(system_message, human_message, None, sql_script=create_statement)

            ModelClassUtils.create_model_class(self.project_id, script=create_statement, code=self.__extract_code(response, "python"))

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

    @staticmethod
    def __get_create_statements_as_list(script):
        pattern = r"CREATE TABLE[\s\S]+?;"
        create_statements = re.findall(pattern, script)
        return create_statements
