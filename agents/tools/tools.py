import os
from database.utils import *
from dotenv import load_dotenv
from langchain.agents import tool
from database.utils import ProjectUtils
from agents.backend_dev_agent import BackendDeveloperAgent
from agents.frontend_dev_agent import FrontendDeveloperAgent
from agents.language_models.llm_deepseek import DeepseekCoder
from agents.database_architect_agent import DatabaseArchitectAgent
from agents.code_writer.code_writer import ProjectInitiator, FlaskAppWriter, ModelClassesWriter


CURRENT_PROJECT_ID = 0

PROJECT = ProjectUtils.get_project_by_name(os.getenv('CURRENT_PROJECT_NAME'))

if PROJECT is not None:
    CURRENT_PROJECT_ID = PROJECT.id


@tool
def check_for_current_project_status_and_next_steps() -> str:
    """Fetches the status of the user's current project.

    Args:
        None

    Returns:
        str: The status of the user's current project. And what to do next.
    """

    return ProjectStatusUtils.get_current_status_and_next_step(CURRENT_PROJECT_ID)


@tool
def design_schema() -> str:
    """Designs the schema for the current project.

    Args:
        None

    Returns:
        str: The status of the user's current project. And what to do next.
    """

    dbaa_model = DeepseekCoder(model_name='deepseek-coder', is_local=False)
    dbaa = DatabaseArchitectAgent(dbaa_model, 1)
    dbaa.design_schema()

    return ProjectStatusUtils.get_current_status_and_next_step(CURRENT_PROJECT_ID)


@tool
def generate_model_classes() -> str:
    """Generates the model classes for the current project.

    Args:
        None

    Returns:
        str: The status of the user's current project. And what to do next.
    """

    dbaa_model = DeepseekCoder(model_name='deepseek-coder', is_local=False)
    dbaa = DatabaseArchitectAgent(dbaa_model, 1)
    dbaa.generate_models()

    return ProjectStatusUtils.get_current_status_and_next_step(CURRENT_PROJECT_ID)


@tool
def design_api_endpoints_schema() -> str:
    """Designs the API endpoints schema for the current project.

    Args:
        None

    Returns:
        str: The status of the user's current project. And what to do next.
    """

    bda_model = DeepseekCoder(model_name='deepseek-coder', is_local=False)
    bda = BackendDeveloperAgent(bda_model, 1)
    bda.design_api_endpoints()

    return ProjectStatusUtils.get_current_status_and_next_step(CURRENT_PROJECT_ID)


@tool
def generate_api_endpoints_code() -> str:
    """Generates the API endpoints code for the current project.

    Args:
        None

    Returns:
        str: The status of the user's current project. And what to do next.
    """

    bda_model = DeepseekCoder(model_name='deepseek-coder', is_local=False)
    bda = BackendDeveloperAgent(bda_model, 1)
    bda.generate_api_endpoints()
    bda.generate_requirements()

    return ProjectStatusUtils.get_current_status_and_next_step(CURRENT_PROJECT_ID)


@tool
def design_and_generate_complete_frontend_code():
    """Designs and generates the complete frontend code for the current project.

    Args:
        None

    Returns:
        str: The status of the user's current project. And what to do next.
    """

    fda_model = DeepseekCoder(model_name='deepseek-coder', is_local=False)
    fda = FrontendDeveloperAgent(fda_model, 1)
    fda.design_frontend()
    fda.generate_front_end_code()

    return ProjectStatusUtils.get_current_status_and_next_step(CURRENT_PROJECT_ID)


@tool
def initiate_project_and_write_complete_code():
    """Initiates the project and writes the complete code.

    Args:
        None

    Returns:
        str: Instructions for the user to run the project.
    """

    pi = ProjectInitiator(1)
    pi.initiate_project()
    pi.write_models_py()
    pi.write_app_py()
    pi.write_requirements_txt()
    pi.write_frontend_code()

    is_windows = os.name == 'nt'
    is_unix = os.name == 'posix'

    if is_windows:
        return f"All Set!\nYou can now proceed to this location `{pi.get_project_path()}`. And run the below commands in order:\n\n1. `venv\\Scripts\\activate`\n2. `pip install -r requirements.txt`\n3. `python app.py`"
    elif is_unix:
        return f"All Set!\nYou can now proceed to this location `{pi.get_project_path()}`. And run the below commands in order:\n\n1. `source venv/bin/activate`\n2. `pip install -r requirements.txt`\n3. `python app.py`"


@tool
def display_model_classes() -> str:
    """Returns the model classes for the current project.

    Args:
        None

    Returns:
        str: The schema design which is a SQL Code.
    """

    all_model_classes = ModelClassUtils.get_model_classes_by_project_id(1)
    model_classes = "\n\n\n".join([model_class.code for model_class in all_model_classes])

    model_classes_writer = ModelClassesWriter(model_classes)

    return model_classes_writer.get_complete_code()


@tool
def display_flask_app_code() -> str:
    """Returns the Flask App code for the current project.

    Args:
        None

    Returns:
        str: The Flask App code.
    """

    all_api_endpoints = APIEndpointCodeUtils.get_api_endpoint_codes_by_project_id(1)
    api_endpoints = "\n\n\n".join([api_endpoint.code for api_endpoint in all_api_endpoints])

    flask_app_writer = FlaskAppWriter(api_endpoints)

    return flask_app_writer.get_complete_code()


def get_all_tools():

    tools = [
        check_for_current_project_status_and_next_steps,
        design_schema,
        generate_model_classes,
        design_api_endpoints_schema,
        generate_api_endpoints_code,
        design_and_generate_complete_frontend_code,
        initiate_project_and_write_complete_code,
        display_model_classes,
        display_flask_app_code
    ]

    return tools
