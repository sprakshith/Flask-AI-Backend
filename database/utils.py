from database.models import *

session = get_session()


class ProjectUtils:

    @staticmethod
    def create_project(name):
        if session.query(Project).filter(Project.name == name).first():
            raise Exception(f'Project with name "{name}" already exists.')

        project = Project(name=name)
        session.add(project)
        session.commit()

        return project

    @staticmethod
    def get_project_by_id(project_id):
        project = session.query(Project).filter(Project.id == project_id).first()
        return project

    @staticmethod
    def get_project_by_name(name):
        project = session.query(Project).filter(Project.name == name).first()
        return project

    @staticmethod
    def get_all_projects():
        projects = session.query(Project).all()
        return projects

    @staticmethod
    def update_project(project_id, name):
        project = session.query(Project).filter(Project.id == project_id).first()
        project.name = name
        session.commit()

    @staticmethod
    def delete_project(project_id):
        project = session.query(Project).filter(Project.id == project_id).first()
        session.delete(project)
        session.commit()


class UserStoryUtils:

    @staticmethod
    def create_user_story(project_id, user_story_count, description):
        user_story = UserStoryUtils.get_user_story_by_project_id_and_user_story_count(project_id, user_story_count)

        if user_story:
            raise Exception(f'User story with Project Id: "{project_id}" and User Story Count: "{user_story_count}" already exists.')

        user_story = UserStory(project_id=project_id, user_story_count=user_story_count, description=description)
        session.add(user_story)
        session.commit()

        return user_story

    @staticmethod
    def get_user_story_by_id(user_story_id):
        user_story = session.query(UserStory).filter(UserStory.id == user_story_id).first()
        return user_story

    @staticmethod
    def get_user_story_by_project_id_and_user_story_count(project_id, user_story_count):
        user_story = session.query(UserStory).filter(UserStory.project_id == project_id, UserStory.user_story_count == user_story_count).first()
        return user_story

    @staticmethod
    def get_user_stories_by_project_id(project_id):
        user_stories = session.query(UserStory).filter(UserStory.project_id == project_id).all()
        return user_stories

    @staticmethod
    def update_user_story(user_story_id, description):
        user_story = session.query(UserStory).filter(UserStory.id == user_story_id).first()
        user_story.description = description
        session.commit()

    @staticmethod
    def delete_user_story(user_story_id):
        user_story = session.query(UserStory).filter(UserStory.id == user_story_id).first()
        session.delete(user_story)
        session.commit()


class SchemaDesignUtils:

    @staticmethod
    def create_schema_design(project_id, version, script):
        schema_design = SchemaDesignUtils.get_schema_design_by_project_id_and_version(project_id, version)

        if schema_design:
            raise Exception(f'Schema design with Project Id: "{project_id}" and Version: "{version}" already exists.')

        schema_design = SchemaDesign(project_id=project_id, version=version, script=script)
        session.add(schema_design)
        session.commit()

        return schema_design

    @staticmethod
    def get_schema_design_by_id(schema_design_id):
        schema_design = session.query(SchemaDesign).filter(SchemaDesign.id == schema_design_id).first()
        return schema_design

    @staticmethod
    def get_schema_design_by_project_id_and_version(project_id, version):
        schema_design = session.query(SchemaDesign).filter(SchemaDesign.project_id == project_id, SchemaDesign.version == version).first()
        return schema_design

    @staticmethod
    def get_latest_schema_design_by_project_id(project_id):
        schema_design = session.query(SchemaDesign).filter(SchemaDesign.project_id == project_id).order_by(SchemaDesign.version.desc()).first()
        return schema_design

    @staticmethod
    def get_schema_designs_by_project_id(project_id):
        schema_designs = session.query(SchemaDesign).filter(SchemaDesign.project_id == project_id).all()
        return schema_designs

    @staticmethod
    def update_schema_design(schema_design_id, script):
        schema_design = session.query(SchemaDesign).filter(SchemaDesign.id == schema_design_id).first()
        schema_design.script = script
        session.commit()

    @staticmethod
    def delete_schema_design(schema_design_id):
        schema_design = session.query(SchemaDesign).filter(SchemaDesign.id == schema_design_id).first()
        session.delete(schema_design)
        session.commit()


class ModelClassUtils:

    @staticmethod
    def create_model_class(project_id, script, code):
        model_class = ModelClass(project_id=project_id, script=script, code=code)
        session.add(model_class)
        session.commit()

        return model_class

    @staticmethod
    def get_model_class_by_id(model_class_id):
        model_class = session.query(ModelClass).filter(ModelClass.id == model_class_id).first()
        return model_class

    @staticmethod
    def get_model_classes_by_project_id(project_id):
        model_classes = session.query(ModelClass).filter(ModelClass.project_id == project_id).all()
        return model_classes

    @staticmethod
    def update_model_class(model_class_id, script, code):
        model_class = session.query(ModelClass).filter(ModelClass.id == model_class_id).first()
        model_class.script = script
        model_class.code = code
        session.commit()

    @staticmethod
    def delete_model_class(model_class_id):
        model_class = session.query(ModelClass).filter(ModelClass.id == model_class_id).first()
        session.delete(model_class)
        session.commit()


class APIEndpointSchemasUtils:

    @staticmethod
    def create_api_endpoint_schema(project_id, user_story_count, json_schema_design):
        api_endpoint_schema = APIEndpointSchemas(project_id=project_id, user_story_count=user_story_count, json_schema_design=json_schema_design)
        session.add(api_endpoint_schema)
        session.commit()

        return api_endpoint_schema

    @staticmethod
    def get_api_endpoint_schema_by_id(api_endpoint_schemas_id):
        api_endpoint_schema = session.query(APIEndpointSchemas).filter(APIEndpointSchemas.id == api_endpoint_schemas_id).first()
        return api_endpoint_schema

    @staticmethod
    def get_api_endpoint_schemas_by_project_id_and_user_story_count(project_id, user_story_count):
        api_endpoint_schemas = session.query(APIEndpointSchemas).filter(APIEndpointSchemas.project_id == project_id, APIEndpointSchemas.user_story_count == user_story_count).all()
        return api_endpoint_schemas

    @staticmethod
    def update_api_endpoint_schemas(api_endpoint_schemas_id, json_schema_design):
        api_endpoint_schemas = session.query(APIEndpointSchemas).filter(APIEndpointSchemas.id == api_endpoint_schemas_id).first()
        api_endpoint_schemas.json_schema_design = json_schema_design
        session.commit()

    @staticmethod
    def delete_api_endpoint_schemas(api_endpoint_schemas_id):
        api_endpoint_schemas = session.query(APIEndpointSchemas).filter(APIEndpointSchemas.id == api_endpoint_schemas_id).first()
        session.delete(api_endpoint_schemas)
        session.commit()


class APIEndpointCodeUtils:

    @staticmethod
    def create_api_endpoint_code(project_id, user_story_count, api_endpoint_schema_id, code):
        api_endpoint_code = APIEndpointCode(project_id=project_id, user_story_count=user_story_count, api_endpoint_schema_id=api_endpoint_schema_id, code=code)
        session.add(api_endpoint_code)
        session.commit()

        return api_endpoint_code

    @staticmethod
    def get_api_endpoint_code_by_id(api_endpoint_code_id):
        api_endpoint_code = session.query(APIEndpointCode).filter(APIEndpointCode.id == api_endpoint_code_id).first()
        return api_endpoint_code

    @staticmethod
    def get_api_endpoint_codes_by_project_id(project_id):
        api_endpoint_codes = session.query(APIEndpointCode).filter(APIEndpointCode.project_id == project_id).all()
        return api_endpoint_codes

    @staticmethod
    def get_api_endpoint_codes_by_project_id_and_user_story_count(project_id, user_story_count):
        api_endpoint_codes = session.query(APIEndpointCode).filter(APIEndpointCode.project_id == project_id, APIEndpointCode.user_story_count == user_story_count).all()
        return api_endpoint_codes

    @staticmethod
    def update_api_endpoint_code(api_endpoint_code_id, code):
        api_endpoint_code = session.query(APIEndpointCode).filter(APIEndpointCode.id == api_endpoint_code_id).first()
        api_endpoint_code.code = code
        session.commit()

    @staticmethod
    def delete_api_endpoint_code(api_endpoint_code_id):
        api_endpoint_code = session.query(APIEndpointCode).filter(APIEndpointCode.id == api_endpoint_code_id).first()
        session.delete(api_endpoint_code)
        session.commit()


class FrontendPageUtils:

    @staticmethod
    def create_frontend_page(project_id, name, purpose, html_code=None, css_code=None, js_code=None):
        frontend_page = FrontendPage(project_id=project_id, name=name, purpose=purpose, html_code=html_code, css_code=css_code, js_code=js_code)
        session.add(frontend_page)
        session.commit()

        return frontend_page

    @staticmethod
    def get_frontend_page_by_id(frontend_page_id):
        frontend_page = session.query(FrontendPage).filter(FrontendPage.id == frontend_page_id).first()
        return frontend_page

    @staticmethod
    def get_frontend_pages_by_project_id(project_id):
        frontend_pages = session.query(FrontendPage).filter(FrontendPage.project_id == project_id).all()
        return frontend_pages

    @staticmethod
    def update_frontend_page(frontend_page_id, name, purpose, html_code, css_code, js_code):
        frontend_page = session.query(FrontendPage).filter(FrontendPage.id == frontend_page_id).first()
        frontend_page.name = name
        frontend_page.purpose = purpose
        frontend_page.html_code = html_code
        frontend_page.css_code = css_code
        frontend_page.js_code = js_code
        session.commit()

    @staticmethod
    def delete_frontend_page(frontend_page_id):
        frontend_page = session.query(FrontendPage).filter(FrontendPage.id == frontend_page_id).first()
        session.delete(frontend_page)
        session.commit()


class ProjectStatusUtils:

    @staticmethod
    def check_for_project(project_id):
        return ProjectUtils.get_project_by_id(project_id)

    @staticmethod
    def get_current_status_and_next_step(project_id):
        project_status = "Below steps are already completed: \n\n"

        project = ProjectStatusUtils.check_for_project(project_id)
        if project:
            project_status = f"1. A project is created with the name: {project.name}.\n"

        user_stories = UserStoryUtils.get_user_stories_by_project_id(project.id)
        if user_stories:
            project_status += f"2. This project has a total of {len(user_stories)} user stories.\n"

        schema_design = SchemaDesignUtils.get_latest_schema_design_by_project_id(project.id)
        if schema_design:
            project_status += f"3. The latest schema design is version {schema_design.version}.\n"
        else:
            project_status += "3. No schema design is created yet.\n\n"
            project_status += "Do you want to proceed with creating a schema design? (Yes/No)"
            return project_status

        model_classes = ModelClassUtils.get_model_classes_by_project_id(project.id)
        if model_classes:
            project_status += f"4. This project has a total of {len(model_classes)} model classes.\n"
        else:
            project_status += "4. No model classes are created yet.\n\n"
            project_status += "Do you want to proceed with creating model classes? (Yes/No)"
            return project_status

        all_api_endpoint_schemas = []
        for user_story in user_stories:
            api_endpoint_schemas = APIEndpointSchemasUtils.get_api_endpoint_schemas_by_project_id_and_user_story_count(project.id, user_story.user_story_count)
            all_api_endpoint_schemas.extend(api_endpoint_schemas)

        if all_api_endpoint_schemas:
            project_status += f"5. This project has a total of {len(all_api_endpoint_schemas)} API endpoint schemas designed.\n"
        else:
            project_status += "5. No API endpoint schemas are designed yet.\n\n"
            project_status += "Do you want to proceed with designing API endpoint schemas? (Yes/No)"
            return project_status

        api_endpoint_codes = APIEndpointCodeUtils.get_api_endpoint_codes_by_project_id(project.id)
        if api_endpoint_codes:
            project_status += f"6. This project has a total of {len(api_endpoint_codes)} API endpoint codes generated.\n"
        else:
            project_status += "6. No API endpoint codes are generated yet.\n\n"
            project_status += "Do you want to proceed with generating API endpoint codes? (Yes/No)"
            return project_status

        frontend_pages = FrontendPageUtils.get_frontend_pages_by_project_id(project.id)
        if frontend_pages:
            project_status += f"7. This project has a total of {len(frontend_pages)} frontend pages designed and generated.\n"
            project_status += "Do you want to proceed with generating the project with the existing codes? (Yes/No)"
        else:
            project_status += "7. No frontend pages are designed and generated yet.\n\n"
            project_status += "Do you want to proceed with designing and generating frontend pages? (Yes/No)"

        return project_status


class ApplicationRequirementsUtils:

    @staticmethod
    def create_application_requirements(project_id, requirements):
        application_requirements = ApplicationRequirements(project_id=project_id, requirements=requirements)
        session.add(application_requirements)
        session.commit()

        return application_requirements

    @staticmethod
    def get_application_requirements_by_id(application_requirements_id):
        application_requirements = session.query(ApplicationRequirements).filter(ApplicationRequirements.id == application_requirements_id).first()
        return application_requirements

    @staticmethod
    def get_application_requirements_by_project_id(project_id):
        application_requirements = session.query(ApplicationRequirements).filter(ApplicationRequirements.project_id == project_id).first()
        return application_requirements
