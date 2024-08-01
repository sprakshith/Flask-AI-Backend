import os
from agents.code_optimizer.code_optimizer import CodeOptimizer
from database.utils import ProjectUtils, ModelClassUtils, APIEndpointCodeUtils, FrontendPageUtils, ApplicationRequirementsUtils

ALL_PROJECTS_PATH = os.getenv("ALL_PROJECTS_PATH")

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class ModelClassesWriter:
    def __init__(self, model_classes: str):
        self.ALL_IMPORTS = self.__get_all_imports()
        self.ALL_VARIABLES = self.__get_all_variables()
        self.ALL_FUNCTIONS = self.__get_all_functions()

        self.model_classes = model_classes

    def __get_all_imports(self):
        imports = "import os\n"
        imports += "from sqlalchemy import create_engine\n"
        imports += "from sqlalchemy.orm import sessionmaker, declarative_base"

        return imports

    def __get_all_variables(self):
        variables = "Base = declarative_base()\n\n"
        variables += "dir_path = os.path.dirname(os.path.realpath(__file__))"

        return variables

    def __get_all_functions(self):
        functions = "def initiate_database():\n"
        functions += "    if not os.path.exists(os.path.join(dir_path, 'sqlite_db')):\n"
        functions += "        os.makedirs(os.path.join(dir_path, 'sqlite_db'))\n\n"
        functions += "    engine = create_engine(f'sqlite:///{dir_path}/sqlite_db/sqlite.db')\n\n"
        functions += "    Base.metadata.create_all(engine)"
        functions += "\n\n\n"
        functions += "def get_session():\n"
        functions += "    initiate_database()\n\n"
        functions += "    engine = create_engine(f'sqlite:///{dir_path}/sqlite_db/sqlite.db')\n"
        functions += "    Session = sessionmaker(bind=engine)\n\n"
        functions += "    return Session()"

        return functions

    def get_complete_code(self):
        unorganized_code = f"{self.ALL_IMPORTS}\n\n{self.ALL_FUNCTIONS}\n\n\n{self.model_classes}"

        code_optimizer = CodeOptimizer(unorganized_code)

        optimized_imports = code_optimizer.optimize_imports()
        optimized_functions = code_optimizer.optimize_functions()
        optimized_classes = code_optimizer.optimize_classes()

        organized_code = f"{optimized_imports}\n\n{self.ALL_VARIABLES}\n\n\n{optimized_classes}\n\n\n{optimized_functions}\n"

        return organized_code


class FlaskAppWriter:
    def __init__(self, api_endpoints: str):
        self.ALL_IMPORTS = self.__get_all_imports()
        self.ALL_VARIABLES = self.__get_all_variables()
        self.MAIN_FUNCTION = self.__get_main_function()

        self.api_endpoints = api_endpoints

    def __get_all_imports(self):
        imports = "from flask import Flask, render_template\n"
        imports += "from flask_cors import CORS\n"
        imports += "from database.models import get_session"

        return imports

    def __get_all_variables(self):
        variables = "app = Flask(__name__)\n"
        variables += "CORS(app)\n\n"
        variables += "session = get_session()"

        return variables

    def __get_main_function(self):
        main_function = "@app.route('/')\n"
        main_function += "def index():\n"
        main_function += "    return render_template('index.html')\n\n\n"
        main_function += "if __name__ == '__main__':\n"
        main_function += "    app.run(host='127.0.0.1', port=5000, debug=True)"

        return main_function

    def get_complete_code(self):
        unorganized_code = f"{self.ALL_IMPORTS}\n\n\n{self.api_endpoints}"

        code_optimizer = CodeOptimizer(unorganized_code)

        optimized_imports = code_optimizer.optimize_imports()
        optimized_functions = code_optimizer.optimize_functions()

        organized_code = f"{optimized_imports}\n\n{self.ALL_VARIABLES}\n\n\n{optimized_functions}\n\n\n{self.MAIN_FUNCTION}"

        return organized_code


class FrontendCodeWriter:
    def __init__(self, name, html_code: str):
        self.name = name
        self.html_code = html_code

    def get_complete_html_code(self):
        code = '<!DOCTYPE html>\n'
        code += '<html lang="en">\n'
        code += '    <head>\n'
        code += '        <meta charset="UTF-8">\n'
        code += '        <meta name="viewport" content="width=device-width, initial-scale=1.0">\n\n'
        code += f'        <title>{self.name}</title>\n\n'
        code += '        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">\n'
        code += f'        <link rel="stylesheet" href="{{{{ url_for(\'static\', filename=\'css/{self.name}.css\') }}}}">\n\n'
        code += '        <script src="https://code.jquery.com/jquery-3.7.1.js"></script>\n'
        code += '        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>\n'
        code += f'        <script src="{{{{ url_for(\'static\', filename=\'js/{self.name}.js\') }}}}"></script>\n'
        code += '    </head>\n\n'
        code += f'    {self.html_code}\n\n'
        code += '</html>'

        return code


class ProjectInitiator:
    def __init__(self, project_id: int):
        self.project_id = project_id

    def initiate_project(self):
        current_project_name = ProjectUtils.get_project_by_id(self.project_id).name
        current_project_path = os.path.join(ALL_PROJECTS_PATH, current_project_name)

        # Create project folder
        self.__create_directory(current_project_path)

        # Create database folder
        database_folder_path = os.path.join(current_project_path, "database")
        self.__create_directory(database_folder_path)

        # Create sqlite_db folder and sqlite.db file
        sqlite_db_folder_path = os.path.join(database_folder_path, "sqlite_db")
        self.__create_directory(sqlite_db_folder_path)

        sqlite_db_file_path = os.path.join(sqlite_db_folder_path, "sqlite.db")
        self.__create_file(sqlite_db_file_path)

        # Create __init__.py and models.py file in database folder
        init_file_path = os.path.join(database_folder_path, "__init__.py")
        self.__create_file(init_file_path)

        models_file_path = os.path.join(database_folder_path, "models.py")
        self.__create_file(models_file_path)

        # Create templates and static folders
        templates_folder_path = os.path.join(current_project_path, "templates")
        self.__create_directory(templates_folder_path)

        static_folder_path = os.path.join(current_project_path, "static")
        self.__create_directory(static_folder_path)

        css_folder_path = os.path.join(static_folder_path, "css")
        self.__create_directory(css_folder_path)

        js_folder_path = os.path.join(static_folder_path, "js")
        self.__create_directory(js_folder_path)

        # Create app.py file
        app_file_path = os.path.join(current_project_path, "app.py")
        self.__create_file(app_file_path)

        # Create requirements.txt file
        requirements_file_path = os.path.join(current_project_path, "requirements.txt")
        self.__create_file(requirements_file_path)

        # Initiate Virtual Environment
        is_windows = os.name == 'nt'
        is_unix = os.name == 'posix'

        if is_windows:
            os.system(f"python -m venv {current_project_path}/venv")
        elif is_unix:
            os.system(f"python3 -m venv {current_project_path}/venv")

    def write_models_py(self):
        all_model_classes = ModelClassUtils.get_model_classes_by_project_id(self.project_id)
        model_classes = "\n\n\n".join([model_class.code for model_class in all_model_classes])

        model_classes_writer = ModelClassesWriter(model_classes)
        organized_code = model_classes_writer.get_complete_code()

        project_name = ProjectUtils.get_project_by_id(self.project_id).name
        models_file_path = os.path.join(ALL_PROJECTS_PATH, f"{project_name}/database/models.py")

        with open(models_file_path, "w") as file:
            file.write(organized_code)

    def write_app_py(self):
        all_api_endpoints = APIEndpointCodeUtils.get_api_endpoint_codes_by_project_id(self.project_id)
        api_endpoints = "\n\n\n".join([api_endpoint.code for api_endpoint in all_api_endpoints])

        flask_app_writer = FlaskAppWriter(api_endpoints)
        organized_code = flask_app_writer.get_complete_code()

        project_name = ProjectUtils.get_project_by_id(self.project_id).name
        app_file_path = os.path.join(ALL_PROJECTS_PATH, f"{project_name}/app.py")

        with open(app_file_path, "w") as file:
            file.write(organized_code)

    def write_frontend_code(self):
        project_name = ProjectUtils.get_project_by_id(self.project_id).name
        frontend_pages = FrontendPageUtils.get_frontend_pages_by_project_id(self.project_id)

        for page in frontend_pages:
            frontend_code_writer = FrontendCodeWriter(page.name, page.html_code)
            html_code = frontend_code_writer.get_complete_html_code()

            html_path = os.path.join(ALL_PROJECTS_PATH, f"{project_name}/templates/{page.name}.html")
            with open(html_path, "w") as file:
                file.write(html_code)

            css_path = os.path.join(ALL_PROJECTS_PATH, f"{project_name}/static/css/{page.name}.css")
            with open(css_path, "w") as file:
                file.write(page.css_code)

            js_path = os.path.join(ALL_PROJECTS_PATH, f"{project_name}/static/js/{page.name}.js")
            with open(js_path, "w") as file:
                file.write(page.js_code)

    def write_requirements_txt(self):
        project_name = ProjectUtils.get_project_by_id(self.project_id).name
        requirements = ApplicationRequirementsUtils.get_application_requirements_by_project_id(self.project_id).requirements

        requirements_file_path = os.path.join(ALL_PROJECTS_PATH, f"{project_name}/requirements.txt")

        with open(requirements_file_path, "w") as file:
            file.write(requirements)

    def get_project_path(self):
        current_project_name = ProjectUtils.get_project_by_id(self.project_id).name
        current_project_path = os.path.join(ALL_PROJECTS_PATH, current_project_name)

        return current_project_path

    def __create_directory(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path)

    def __create_file(self, path: str):
        if not os.path.exists(path):
            open(path, 'w').close()
