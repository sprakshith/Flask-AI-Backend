from dotenv import load_dotenv
from database.utils import ProjectUtils, UserStoryUtils
from agents.backend_dev_agent import BackendDeveloperAgent
from agents.code_writer.code_writer import ProjectInitiator
from agents.frontend_dev_agent import FrontendDeveloperAgent
from agents.language_models.llm_deepseek import DeepseekCoder
from agents.database_architect_agent import DatabaseArchitectAgent

load_dotenv()

dbaa_model = DeepseekCoder(model_name='deepseek-coder', is_local=False)
bda_model = DeepseekCoder(model_name='deepseek-coder', is_local=False)
fda_model = DeepseekCoder(model_name='deepseek-coder', is_local=False)

PROJECT_NAME = 'ToDoList'

ProjectUtils.create_project(PROJECT_NAME)
project = ProjectUtils.get_project_by_name(PROJECT_NAME)

print('Project initiated successfully!')

user_story_1_description = open(f'Projects/{PROJECT_NAME}/1.txt', 'r').read()
user_story_2_description = open(f'Projects/{PROJECT_NAME}/2.txt', 'r').read()

UserStoryUtils.create_user_story(project.id, 1, user_story_1_description)
UserStoryUtils.create_user_story(project.id, 2, user_story_2_description)

print('User Stories added successfully!')

dbaa = DatabaseArchitectAgent(dbaa_model, project.id)
dbaa.design_schema()
dbaa.generate_models()

print('Schema and Models generated successfully!')

bda = BackendDeveloperAgent(bda_model, project.id)
bda.design_api_endpoints()
bda.generate_api_endpoints()

print('API Endpoints designed and generated successfully!')

bda.generate_requirements()

print('Requirements generated successfully!')

fda = FrontendDeveloperAgent(fda_model, project.id)
fda.design_frontend()
fda.generate_front_end_code()

print('Frontend designed and generated successfully!')

pi = ProjectInitiator(project.id)
pi.initiate_project()

print('Project initiated successfully!')

pi.write_models_py()

print('Models written successfully!')

pi.write_app_py()

print('App written successfully!')

pi.write_requirements_txt()

print('Requirements written successfully!')

pi.write_frontend_code()

print('Frontend written successfully!')

print('Project completed successfully!')
